__author__ = "Taras Basiuk"

import os, logging
from collections import deque
from datetime import datetime

from slas.sla_penalty_function import AbstractSLAPenaltyFunction, AveragingPiecewiseLinearSLAPenaltyFunction
from data_migration_policy.data_migration_policy import AbstractDataMigrationPolicy, ProbabilityBasedDataMigrationPolicy
from data_admission_policy.data_admission_policy import AbstractDataAdmissionPolicy, EagerDataAdmissionPolicy, NeverDataAdmissionPolicy, Q2DataAdmissionPolicy
from data_eviction_policy.data_eviction_policy import AbstractDataEvictionPolicy, FIFODataEvictionPolicy, LRUEvictionPolicy
from monitoring.monitoring import TenantMetricsMonitor

class BufferPoolSimulator():

    def __init__(self, params, DAPs, DEPs, SLAs, DMPs, metadata={}, logger=logging.getLogger(__name__)):
        """
            Constructor for the BufferPoolSimulator.
            Expects:
                params - storage tier parameters dictionary, having free space, CPU_acess flag, and SLO costs
                DAPs - storage tier data admission policies
                DEPs - storage tier data eviction policies
                SLAs - Tenant service level agreements
                DMPs - Tenant data migration policies
                metadata - dictionary with page locations and dirty flags
                logger - initialized logger
        """

        # Validate the given parameters

        # Validate the storage tier parameters
        assert isinstance(params, dict), "params must be a dictionary. Got: {}".format(params)
        for tier in params:
            assert "free_space" in params[tier] and isinstance(params[tier]["free_space"], int), \
                "params['{}'] must have an integer mapping for 'free space'. Got: {}".format(tier, params[tier])
            assert "CPU_access" in params[tier] and isinstance(params[tier]["CPU_access"], bool), \
                "params['{}'] must have a boolean mapping for 'CPU_access'. Got: {}".format(tier, params[tier])
            assert "SLO_costs" in params[tier] and isinstance(params[tier]["SLO_costs"], dict), \
                "params['{}'] must have a dictionary mapping for 'SLO_costs'. Got: {}".format(tier, params[tier])

            for access_type in params[tier]["SLO_costs"]:
                assert isinstance(params[tier]["SLO_costs"][access_type], dict), \
                    "params['{}']['SLO_costs'][{}] must have a dictionary with SLO cost mappings. Got: {}".format(
                        tier, access_type, params[tier]["SLO_costs"][access_type])

                for slo_type in params[tier]["SLO_costs"][access_type]:
                    assert isinstance(params[tier]["SLO_costs"][access_type][slo_type], float), \
                        "params['{}']['SLO_costs'][{}][{}] must be a float. Got: {}".format(
                            tier, access_type, slo_type, params[tier]["SLO_costs"][access_type][slo_type])

        # Validate the data admission policies
        assert isinstance(DAPs, dict), "DAPs must be a dictionary. Got: {}".format(DAPs)
        for tier in params:
            assert tier in DAPs and isinstance(DAPs[tier], AbstractDataAdmissionPolicy), \
                "DAP for {} tier is not provided. Got: {}".format(tier, DAPs)

        # Validate the data eviction policies
        assert isinstance(DEPs, dict), "DEPs must be a dictionary. Got: {}".format(DEPs)
        for tier in params:
            assert tier in DEPs and isinstance(DEPs[tier], AbstractDataEvictionPolicy), \
                "DEP for {} tier is not provided. Got: {}".format(tier, DEPs)

        # Validate the tenant SLAs
        assert isinstance(SLAs, dict), "SLAs must be a dictionary. Got: {}".format(SLAs)
        for tenant in SLAs:
            assert isinstance(SLAs[tenant], AbstractSLAPenaltyFunction), \
                "SLA for {} tenant is not provided. Got: {}".format(tenant, SLAs)

        # Validate the tenant DMPs
        assert isinstance(DMPs, dict), "DMPs must be a dictionary. Got: {}".format(DMPs)
        for tenant in DMPs:
            assert isinstance(DMPs[tenant], AbstractDataMigrationPolicy), \
                "DMP for {} tenant is not provided. Got: {}".format(tenant, DMPs)

        # Validate page metadata
        assert isinstance(metadata, dict), "metadata must be a dictionary. Got: {}".format(metadata)
        for pageID in metadata:
            assert isinstance(metadata[pageID], tuple) and isinstance(metadata[pageID][0], str) and isinstance(metadata[pageID][1], bool), \
                "metadata must map pageIDs to tuples of strings and booleans. Got: {}".format(metadata[pageID])

        self.params = params
        self.DAPs = DAPs
        self.DEPs = DEPs
        self.SLAs = SLAs
        self.DMPs = DMPs
        self.metadata = metadata
        self.logger = logger
        self.monitor = TenantMetricsMonitor(logger)

        logger.info("Instantiating the Buffer Pool Simulator.")
        logger.debug("Storage tier parameters: {}".format(self.params))
        logger.debug("Page metadata: {}".format(self.metadata))
        logger.debug("Data Admission Policies: {}".format(self.DAPs))
        logger.debug("Data Eviction Policies: {}".format(self.DEPs))
        logger.debug("Tenant SLAs: {}".format(self.SLAs))
        logger.debug("Tenant DMPs: {}".format(self.DMPs))
        logger.debug("Tenant Metrics Monitor: {}".format(self.monitor))

    def sim(self, N, timestamps, pages, tenants, types, output_file=None, from_time=0, to_time=None, warmup=0):
        """
            Processes N samples of the data page access requests.
            Expects N timestamps, page IDs, tenant IDs, and access types.
            Returns SLA violation penalties accumulate for each tenant.
        """
        logger = self.logger
        logger.info("Starting to validate the simulation input data.")

        # Validate N, timestamps, pages, tenants, types
        assert isinstance(N, int) and N > 0, "N must be a positive integer, got: {}".format(N)
        assert isinstance(timestamps, list) and len(timestamps) == N, "timestamps must be a list of {} elements. Got: {}".format(N, timestamps)
        for t in timestamps:
            assert isinstance(t, int), "timestamps must only contain integers, got: {}".format(t)
        assert isinstance(pages, list) and len(pages) == N, "pages must be a list of {} elements. Got: {}".format(N, pages)
        for p in pages:
            assert isinstance(p, int), "pages must only contain integers, got: {}".format(p)
        assert isinstance(tenants, list) and len(tenants) == N, "tenants must be a list of {} elements. Got: {}".format(N, tenants)
        for t in tenants:
            assert isinstance(t, int), "tenants must only contain integers, got: {}".format(t)
        assert isinstance(types, list) and len(types) == N, "types must be a list of {} elements. Got: {}".format(N, types)
        for t in types:
            assert isinstance(t, str), "types must only contain strings, got: {}".format(t)

        # Validate output_file, warmup, from_time, to_time
        assert output_file == None or os.path.isfile(output_file), "Output file, if given, must be a valid path, got: {}".format(output_file)
        assert isinstance(warmup, int) and warmup >= 0, "warmup must be a non-negative integer. Got: {}".format(warmup)
        assert isinstance(from_time, int) and from_time >= 0, "from_time must be a non-negative integer. Got: {}".format(from_time)
        assert to_time == None or (isinstance(to_time, int) and to_time >= from_time), \
            "to_time, if given, must be a non-negative integer and no less than from_time. Got: {}".format(to_time)

        logger.info("Starting the simulation.")
        for i in range(N):
            time, pageID, tenantID, access_type = timestamps[i], pages[i], tenants[i], types[i]

            # Skip the request if its timestamp is below from_time or above to_time
            if time < from_time or (to_time != None and time > to_time):
                continue

            logger.debug("Page access request #{} - time:{}, pageID:{}, tenantID:{}, access_type:{}".format(
                i + 1, time, pageID, tenantID, access_type))

            # Retrieve the current storage tier the page ID belongs to
            # Check whether the page is new
            if pageID not in self.metadata:
                self.metadata[pageID] = ("SSD", False)
                self.params["SSD"]["free_space"] = self.params["SSD"]["free_space"] - 1
                logger.debug("Encountered pageID:{} for the first time. Assuming it's on SSD tier and not dirty. Free SSD space: {}.".format(
                    pageID, self.params["SSD"]["free_space"]))

            tier, dirty = self.metadata[pageID]
            logger.debug("Found pageID:{} on storage tier:{} dirty:{}".format(pageID, tier, dirty))

            data_access_chain = deque()
            if not self.DAPs[tier].should_admit(pageID) and self.params[tier]["CPU_access"]:
                # If the page should not be admitted to a different tier and the current tier is accessible by the CPU
                # Just add the page access request to the chain
                data_access_chain.appendleft((pageID, tier, access_type))
            else:
                # Find the new storage tier for the page admission
                new_tier = self.DMPs[tenantID].destination_on_admission_from(time, pageID, tier)
                while not self.params[new_tier]["CPU_access"]:
                    new_tier = self.DMPs[tenantID].destination_on_admission_from(time, pageID, new_tier)
                data_access_chain.appendleft((pageID, new_tier, access_type))
                logger.debug("pageID:{} will be admitted from {} to {} tier per DMP of tenantID:{}".format(
                    pageID, tier, new_tier, tenantID))

                # Remove the page from th residency with the DEP in the old tier
                self.DEPs[tier].update_residency(pageID, False)
                self.params[tier]["free_space"] = self.params[tier]["free_space"] + 1

                # Make sure the new tier has enough free space
                victim_page = pageID
                while True:
                    if self.params[new_tier]["free_space"] > 0:
                        self.params[new_tier]["free_space"] = self.params[new_tier]["free_space"] - 1
                        logger.debug("{} tier remaining free space: {}".format(new_tier, self.params[new_tier]["free_space"]))
                        break
                    else:
                        old_victim_page = victim_page
                        victim_page = self.DEPs[new_tier].evict()
                        old_tier = new_tier
                        new_tier = self.DMPs[tenantID].destination_on_eviction_from(time, victim_page, new_tier)
                        logger.debug("pageID:{} dirty:{} will be copied from {} to {} tier to make space for pageID:{}".format(
                            victim_page, self.metadata[victim_page][1], old_tier, new_tier, old_victim_page))
                        if not self.metadata[victim_page][1] and new_tier == "SSD":
                            # If the page is not dirty and the destination tier is "SSD", just update the metadata
                            self.metadata[victim_page] = ("SSD", False)
                            break
                        else:
                            # Victim page has to be migrated somewhere else
                            data_access_chain.appendleft((victim_page, new_tier, "copy"))

            # Process the data access chain
            logger.debug("Page access request #{} data access chain: {}".format(i + 1, data_access_chain))
            slo_val = 0
            for j in range(len(data_access_chain)):
                # Update the SLO costs
                d_pageID, d_tier, d_access_type = data_access_chain[j] # Destination pageID, tier and access type
                if time >= warmup:
                    slo_val += self.params[d_tier]["SLO_costs"][d_access_type][self.SLAs[tenantID].slo_type]
                if d_access_type == "copy":
                    # If the page was copied over, we need to add the slo cost of reading the page as well
                    s_pageID, s_tier, s_access_type = data_access_chain[j + 1]
                    if time >= warmup:
                        slo_val += self.params[s_tier]["SLO_costs"]["read"][self.SLAs[tenantID].slo_type]

                    # When the page is copied it has to become a resident of the destination storage tier
                    # For non-copy accesses page will become resident through record_access method with resident=True
                    self.DEPs[d_tier].update_residency(d_pageID, True)

                # Update the corresponding page metadata
                # First update the page tier
                self.metadata[d_pageID] = (d_tier, self.metadata[d_pageID][1])
                # If the dirty page arrived to SSD, it's no longer dirty
                if d_tier == "SSD" and self.metadata[d_pageID][1]:
                    logger.debug("pageID:{} arrived to SSD tier, so it's no longer dirty.".format(d_pageID))
                    self.metadata[d_pageID] = (self.metadata[d_pageID][0], False)
                if d_tier != "SSD" and d_access_type == "update":
                    logger.debug("pageID:{} updated while not on SSD tier, so it's now dirty.".format(d_pageID))
                    self.metadata[d_pageID] = (self.metadata[d_pageID][0], True)

            # Record SLO value satisfaction
            if time >= warmup:
                self.SLAs[tenantID].record_SLO(time, slo_val)

            # Record page access request for DAPs and DEPs
            for t in self.DAPs:
                self.DAPs[t].record_access(time, pageID, access_type)
            for t in self.DEPs:
                self.DEPs[t].record_access(time, pageID, t == self.metadata[pageID][0], access_type)

            # Record monitoring metrics
            if time >= warmup:
                self.monitor.record_metric(time, tenantID, tier, data_access_chain, slo_val)

        # Calculate the SLA penalty results
        penalties = {}
        for t in self.SLAs:
            logger.info("Evaluating SLA penalty for tenantID:{}".format(t))
            penalties[t] = self.SLAs[t].eval_penalty(warmup)

        # output results
        if output_file:
            with open(output_file, 'w') as f:
                f.write("tenantID,SLA_penalty\n")
                for t in penalties:
                    f.write("{},{}\n".format(t, penalties[t]))
        else:
            print("tenantID,SLA_penalty")
            for t in penalties:
                print("{},{}".format(t, penalties[t]))

        # Log the metrics
        self.monitor.log_aggregate_metrics(warmup)
        logger.info("Simulation finished.")

    def dump_state(self, dump_dir, logger):
        """The function to dump the state of the simulator into dump_dir once the simulation is finished."""
        logger.info("Starting to dump the state of the simulator into: {}".format(dump_dir))

        import json
        file_name = "{}tier_params.json".format(dump_dir)
        logger.info("Dumping the storage tier parameters into: {}".format(file_name))
        with open(file_name, 'w') as f:
            json.dump(self.params, f)

        file_name = "{}tier_metadata.json".format(dump_dir)
        logger.info("Dumping the storage tier metadata into: {}".format(file_name))
        with open(file_name, 'w') as f:
            json.dump(self.metadata, f)

        # Dumping the data admission policies
        os.makedirs("{}DAPs/".format(dump_dir), exist_ok=True)
        for dap in self.DAPs:
            typ = None
            if isinstance(self.DAPs[dap], EagerDataAdmissionPolicy):
                typ = "EAG"
            elif isinstance(self.DAPs[dap], NeverDataAdmissionPolicy):
                typ = "NEV"
            elif isinstance(self.DAPs[dap], Q2DataAdmissionPolicy):
                typ = "2Q"
            else:
                raise ValueError("Unknown data admission policy name: {}".format(self.DAPs[dap]))

            file_name = "{}DAPs/{}_{}_DAP.json".format(dump_dir, dap, typ)
            logger.info("Dumping the DAP for {} tier into: {}".format(dap, file_name))
            self.DAPs[dap].persist_to_file(file_name)

        # Dumping the data eviction policies
        os.makedirs("{}DEPs/".format(dump_dir), exist_ok=True)
        for dep in self.DEPs:
            typ = None
            if isinstance(self.DEPs[dep], LRUEvictionPolicy):
                typ = "LRU"
            elif isinstance(self.DEPs[dep], FIFODataEvictionPolicy):
                typ = "FIFO"
            else:
                raise ValueError("Unknown data eviction policy name: {}".format(self.DEPs[dep]))

            file_name = "{}DEPs/{}_{}_DEP.json".format(dump_dir, dep, typ)
            logger.info("Dumping the DEP for {} tier into: {}".format(dep, file_name))
            self.DEPs[dep].persist_to_file(file_name)

        # Dumping the data migration policies
        os.makedirs("{}DMPs/".format(dump_dir), exist_ok=True)
        for dmp in self.DMPs:
            typ = None
            if isinstance(self.DMPs[dmp], ProbabilityBasedDataMigrationPolicy):
                typ = "PROB"
            else:
                raise ValueError("Unknown data migration policy name: {}".format(self.DMPs[dmp]))

            file_name = "{}DMPs/{}_{}_DMP.json".format(dump_dir, dmp, typ)
            logger.info("Dumping the DMP for {} tenant into: {}".format(dmp, file_name))
            self.DMPs[dmp].persist_to_file(file_name)

        # Dumping the tenant SLA policies
        os.makedirs("{}SLAs/".format(dump_dir), exist_ok=True)
        for sla in self.SLAs:
            typ = None
            if isinstance(self.SLAs[sla], AveragingPiecewiseLinearSLAPenaltyFunction):
                typ = "APWL"
            else:
                raise ValueError("Unknown SLA policy name: {}".format(self.SLAs[sla]))

            file_name = "{}SLAs/{}_{}_SLA.json".format(dump_dir, sla, typ)
            logger.info("Dumping the SLA for {} tenant into: {}".format(sla, file_name))
            self.SLAs[sla].persist_to_file(file_name)

if __name__ == "__main__":

    # Default values
    DEFAULT_TIER_PARAMS_FILE = "data_sets/tier_params.csv"
    DEFAULT_TIER_DAPS_FILE = "data_sets/tier_daps.csv"
    DEFAULT_TIER_DEPS_FILE = "data_sets/tier_deps.csv"
    DEFAULT_TENANT_SLAS_FILE = "data_sets/tenant_slas.csv"
    DEFAULT_TENANT_DMPS_FILE = "data_sets/tenant_dmps.csv"
    DEFAULT_PAS_FILE = "data_sets/page_access_sequence.csv"

    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_LOG_FILE = "logs/bp_simulator_{}.log".format(datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))

    # Parse given arguments
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''
            This tool simulates the operation of a DBMS buffer pool manager which supports:
                - Multi-tenancy with SLA violation penalty functions
                - Three tier SSD-NVM-RAM storage architecture.

            INPUT:
                - TODO

            OUTPUT:
                - SLA violation penalty accrued by each tenant.
        ''')

    parser.add_argument('-ID', '--init-dir', type=str, default=None,
        help='''Directory from which the simulator state will be initialized.

                The directory contents are expected to be generated by the dumping
                of the simulator state affter the previous simulation (see -SD option).

                If this option is provided, all of the below options will be ignored:
                    -P, -A, -E, -T, -D.
                They will be read in from the directory.''')
    parser.add_argument('-P', '--tier-params', type=str, default=DEFAULT_TIER_PARAMS_FILE,
        help="""Input file with the storage tier parameters. Expected contents:
                    header1,header2,header3,...
                    name1, free_space1, CPU_access_flag1, access_type11, SLO11, cost11, access_type12, SLO12, cost12, ...
                    name2, free_space2, CPU_access_flag2, access_type21, SLO21, cost21, access_type22, SLO22, cost22, ...
                    ...
                Default: {}"""
            .format(DEFAULT_TIER_PARAMS_FILE))
    parser.add_argument('-A', '--tier-daps', type=str, default=DEFAULT_TIER_DAPS_FILE,
        help="""Input file with the tier data admission policies. Expected contents:
                    header1,header2,header3,...
                    tier1, policy1, policy_param11, policy_param12 ...
                    tier2, policy2, policy_param21, policy_param22 ...
                    ...
                Default: {}"""
            .format(DEFAULT_TIER_DAPS_FILE))
    parser.add_argument('-E', '--tier-deps', type=str, default=DEFAULT_TIER_DEPS_FILE,
        help="""Input file with the tier data eviction policies. Expected contents:
                    header1,header2,header3,...
                    tier1, policy1, policy_param11, policy_param12 ...
                    tier2, policy2, policy_param21, policy_param22 ...
                    ...
                Default: {}"""
            .format(DEFAULT_TIER_DEPS_FILE))
    parser.add_argument('-T', '--tenant-slas', type=str, default=DEFAULT_TENANT_SLAS_FILE,
        help="""Input file with tenant SLA parameters. Expected contents:
                    header1,header2,header3,...
                    tenantID1,slo_type1,eval_period1,sla_func_type1,param11,param12,param13,...
                    tenantID2,slo_type2,eval_period2,sla_func_type2,param21,param22,param23,...
                    ...
                Default: {}""".format(DEFAULT_TENANT_SLAS_FILE))
    parser.add_argument('-D', '--tenant-dmps', type=str, default=DEFAULT_TENANT_DMPS_FILE,
        help="""Input file with tenant data migration policies. Expected contents:
                    header1,header2,header3,...
                    tenantID1,stage0,stage1, ... ,admit0to0,admit0to1, ... ,evict0to0,evict0to1,...
                    tenantID2,stage0,stage1, ... ,admit0to0,admit0to1, ... ,evict0to0,evict0to1,...
                Default: {}""".format(DEFAULT_TENANT_DMPS_FILE))
    parser.add_argument('-F', '--pas-file', type=str, default=DEFAULT_PAS_FILE,
        help="""Input file with page access sequence (PAS). Expected contents:
                    timestamp(ms),tenantID,pageID,access_type(R/W)
                    timestamp(ms),tenantID,pageID,access_type(R/W)
                Default: {}""".format(DEFAULT_PAS_FILE))
    parser.add_argument('-OF', '--output-file', type=str, default=None,
        help='If given, the simulation results will be stored in the output file.')
    parser.add_argument('-W', '--warmup', type=int, default=0,
        help='Warmup timestamp in ms. SLA violation penalties and metrics collection will not be in effect before the warmup expires. Default: 0')
    parser.add_argument('-FT', '--from-time', type=int, default=0,
        help='Simulation start timestamp in ms. Page access requests before the from-time will not be processed. Default: 0')
    parser.add_argument('-TT', '--to-time', type=int, default=None,
        help='Simulation end timestamp in ms. Page access requests after the to-time will not be processed. Default: None')
    parser.add_argument('-LL', '--log-level', type=str, default=DEFAULT_LOG_LEVEL, choices=["INFO", "DEBUG"],
        help='Logging level. Default: {}'.format(DEFAULT_LOG_LEVEL))
    parser.add_argument('-LF', '--log-file', type=str, default=DEFAULT_LOG_FILE,
        help='Log file. Default: {}'.format(DEFAULT_LOG_FILE))
    parser.add_argument('-SD', '--sim-state-dump-dir', type=str, default=None,
        help='Directory where (if given) the state of the simulator will be saved after the simulation.')
    args = parser.parse_args()

    # Start validating input parameters

    # Read in the logger parameters and instantiate the logger
    log_level = logging.INFO if args.log_level == "INFO" else logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    handler = logging.FileHandler(args.log_file, mode='a')
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    storage_tier_params = {} # Container for all storage tier parameters
    page_metadata = {} # Start with cold buffer pool
    data_admission_policies = {}
    data_eviction_policies = {}
    tenant_dmps = {}
    tenant_slas = {}

    # If initializing from files
    if args.init_dir == None:
        # Read in and validate storage tier parameters
        assert os.path.isfile(args.tier_params), "Storage tier parameters file value must be a valid path. Got: {}".format(args.tier_params)
        with open(args.tier_params) as f:
            f.readline() # Skip the headers line
            params = f.readline().strip() # Read in the first meaningful line
            while params:
                params = params.split(',')
                assert len(params) >= 6 and len(params) % 3 == 0, \
                    "Number of storage tier parameters must be at least 6 and divisible by 3. Got: {}".format(params)

                name, free_space, CPU_acess, SLO_costs = params[0], int(params[1]), bool(params[2]), {}
                for i in range(3, len(params), 3):
                    acces_type, SLO_type , SLO_cost = params[i], params[i + 1], float(params[i + 2])
                    if acces_type not in SLO_costs:
                        SLO_costs[acces_type] = {}
                    SLO_costs[acces_type][SLO_type] = SLO_cost

                storage_tier_params[name] = {"free_space" : free_space, "CPU_access" : CPU_acess, "SLO_costs" : SLO_costs}
                params = f.readline().strip() # Read in the next line

        # Read in and validate data admission policies tier parameters
        assert os.path.isfile(args.tier_daps), "Storage tier data admission policies file value must be a valid path. Got: {}".format(args.tier_daps)
        with open(args.tier_daps) as f:
            f.readline() # Skip the headers line
            dap = f.readline().strip()
            while dap:
                dap = dap.split(',')
                assert len(dap) >= 2, "Number of tier data admission policy must be at least 2. Got: {}".format(dap)
                tier, policy = dap[0], dap[1]

                if policy == "EAG":
                    data_admission_policies[tier] = EagerDataAdmissionPolicy()
                elif policy == "NEV":
                    data_admission_policies[tier] = NeverDataAdmissionPolicy()
                elif policy == "2Q":
                    data_admission_policies[tier] = Q2DataAdmissionPolicy()
                else:
                    raise ValueError("Unknown data admission policy name: {}".format(policy))

                dap = f.readline().strip()

        # Read in and validate data admission policies tier parameters
        assert os.path.isfile(args.tier_deps), "Storage tier data admission policies file value must be a valid path. Got: {}".format(args.tier_daps)
        with open(args.tier_deps) as f:
            f.readline() # Skip the headers line
            dep = f.readline().strip()
            while dep:
                dep = dep.split(',')
                assert len(dep) >= 2, "Number of tier data admission policy must be at least 2. Got: {}".format(dep)
                tier, policy = dep[0], dep[1]

                if policy == "LRU":
                    data_eviction_policies[tier] = LRUEvictionPolicy()
                elif policy == "FIFO":
                    data_eviction_policies[tier] = FIFODataEvictionPolicy()
                else:
                    raise ValueError("Unknown data eviction policy type: {}".format(policy))

                dep = f.readline().strip()

        # Read in and validate tenant SLAs
        assert os.path.isfile(args.tenant_slas), "Tenant SLAs file value must be a valid path. Got: {}".format(args.tenant_slas)
        with open(args.tenant_slas) as f:
            f.readline() # Skip the headers line
            tenant = f.readline().strip()
            while tenant:
                tenant = tenant.split(',')
                assert len(tenant) >= 4, "number of tenant SLA parameters must be at least 4. Got: {}".format(tenant)

                tenant_id, slo_type, eval_period, sla_func_type = int(tenant[0]), tenant[1], int(tenant[2]), tenant[3]

                if sla_func_type == "APWL":
                    assert len(tenant) >= 6 and len(tenant) % 3 == 0, \
                        "number of tenant SLA parameters must be at least 6 and divisible by 3. Got: {}".format(tenant)

                    baseline_slope = float(tenant[4])
                    baseline_intercept = float(tenant[5])

                    intervals = {}
                    for i in range(6, len(tenant), 3):
                        interval_start = float(tenant[i])
                        interval_slope = float(tenant[i + 1])
                        interval_intercept = float(tenant[i + 2])

                        intervals[interval_start] = (interval_slope, interval_intercept)

                        tenant_slas[tenant_id] = AveragingPiecewiseLinearSLAPenaltyFunction(
                            logger,
                            slo_type = slo_type,
                            eval_period = eval_period,
                            mapping_func = {"baseline_slope": baseline_slope, "baseline_intercept" : baseline_intercept, "intervals": intervals})
                else:
                    raise ValueError("Unknown SLA penalty function type: {}".format(sla_func_type))

                tenant = f.readline().strip()

        # Read in and validate tenant DMPs
        assert os.path.isfile(args.tenant_dmps), "Tenant DMPs file value must be a valid path. Got: {}".format(args.tenant_dmps)
        with open(args.tenant_dmps) as f:
            f.readline() # Skip the headers line
            dmp = f.readline().strip()
            while dmp:
                dmp = dmp.split(',')
                assert len(dmp) >= 5, "Tenant DMP must contain at least 5 parameters Got: {}".format(dmp)

                tenant_id, dmp_type, tiers_num = int(dmp[0]), dmp[1], int(dmp[2])

                assert tenant_id in tenant_slas, \
                    "Found tenant ID for which there's no SLA: {}".format(tenant_id)

                assert len(dmp) >= 3 + tiers_num, "Tenant DMP must contain at least {} parameters Got: {}".format(3 + tiers_num, dmp)
                dmp_tiers = dmp[3:3 + tiers_num] # Read in data migration policy tiers

                if dmp_type == "PROB":
                    assert len(dmp) >= 3 + tiers_num, "Tenant Probability Based DMP must contain at least {} parameters Got: {}".format(
                        3 + tiers_num + (2 * tiers_num * tiers_num), dmp)

                    # Prepare square data admission and eviction matrices
                    admission_matrix = []
                    eviction_matrix = []
                    for i in range(tiers_num):
                        admission_matrix.append(list(map(float, dmp[
                            3 + tiers_num + (i * tiers_num) : 3 + (2 * tiers_num) + (i * tiers_num)])))
                        eviction_matrix.append(list(map(float, dmp[
                            3 + tiers_num + (tiers_num**2) + (i * tiers_num) : 3 + (2 * tiers_num) + (tiers_num**2) + (i * tiers_num)])))

                    # Instantiate ProbabilityBasedDataMigrationPolicy
                    tenant_dmps[tenant_id] = ProbabilityBasedDataMigrationPolicy(
                        {"tiers" : dmp_tiers, "data_admission_matrix" : admission_matrix, "data_eviction_matrix" : eviction_matrix})
                else:
                    raise ValueError("Unknown DMP type: {}".format(dmp_type))

                dmp = f.readline().strip()
    else:
        # If we're initializing the simulator from the directory of dumped state
        assert os.path.isdir(args.init_dir), "Given simulator initialization directory is invalid: {}".format(args.init_dir)

        import json

        # Reading in the storage tier parameters from the initialization directory
        storage_tier_params_file = "{}tier_params.json".format(args.init_dir)
        assert os.path.isfile(storage_tier_params_file), "Was not able to find the storage tier parameters file at: {}".format(storage_tier_params_file)
        with open(storage_tier_params_file) as f:
            storage_tier_params = json.load(f)

        # Reading in the page metadata from the initialization directory
        page_metadata_file = "{}tier_metadata.json".format(args.init_dir)
        assert os.path.isfile(page_metadata_file), "Was not able to find the storage tier metadata file at: {}".format(page_metadata_file)
        with open(page_metadata_file) as f:
            page_metadata = dict(map(lambda kv: (int(kv[0]), (kv[1][0], kv[1][1])), json.load(f).items()))

        # Reading in the data admission policies from the initialization directory
        data_admission_policies_dir = "{}DAPs/".format(args.init_dir)
        assert os.path.isdir(data_admission_policies_dir), \
            "Was not able to find the data admission policies directory at: {}".format(data_admission_policies_dir)
        # Iterate through the files in the DAPs directory
        for f in os.listdir(data_admission_policies_dir):
            file_name, extension = f.split('.')
            assert extension == "json", "Was expecting file name of TIER_TYPE_DAP.json format, got: {}".format(f)

            tier, typ, dap = file_name.split('_')
            assert dap == "DAP", "Was expecting file name of TIER_TYPE_DAP.json format, got: {}".format(f)

            dap_file_path = "{}{}".format(data_admission_policies_dir, f)
            if typ == "EAG":
                data_admission_policies[tier] = EagerDataAdmissionPolicy(init_from_file=dap_file_path)
            elif typ == "NEV":
                data_admission_policies[tier] = NeverDataAdmissionPolicy(init_from_file=dap_file_path)
            elif typ == "2Q":
                data_admission_policies[tier] = Q2DataAdmissionPolicy(init_from_file=dap_file_path)
            else:
                raise ValueError("Unknown data admission policy type: {}".format(typ))

        # Reading in the data eviction policies from the initialization directory
        data_eviction_policies_dir = "{}DEPs/".format(args.init_dir)
        assert os.path.isdir(data_eviction_policies_dir), \
            "Was not able to find the data eviction policies directory at: {}".format(data_eviction_policies_dir)
        # Iterate through the files in the DAPs directory
        for f in os.listdir(data_eviction_policies_dir):
            file_name, extension = f.split('.')
            assert extension == "json", "Was expecting file name of TIER_TYPE_DEP.json format, got: {}".format(f)

            tier, typ, dep = file_name.split('_')
            assert dep == "DEP", "Was expecting file name of TIER_TYPE_DEP.json format, got: {}".format(f)

            dep_file_path = "{}{}".format(data_eviction_policies_dir, f)
            if typ == "LRU":
                data_eviction_policies[tier] = LRUEvictionPolicy(init_from_file=dep_file_path)
            elif typ == "FIFO":
                data_eviction_policies[tier] = FIFODataEvictionPolicy(init_from_file=dep_file_path)
            else:
                raise ValueError("Unknown data eviction policy type: {}".format(typ))

        # Reading in the data migration policies from the initialization directory
        data_migration_policies_dir = "{}DMPs/".format(args.init_dir)
        assert os.path.isdir(data_migration_policies_dir), \
            "Was not able to find the data migration policies directory at: {}".format(data_migration_policies_dir)
        # Iterate through the files in the DAPs directory
        for f in os.listdir(data_migration_policies_dir):
            file_name, extension = f.split('.')
            assert extension == "json", "Was expecting file name of TIER_TYPE_DMP.json format, got: {}".format(f)

            tenant, typ, dmp = file_name.split('_')
            assert dmp == "DMP", "Was expecting file name of TIER_TYPE_DMP.json format, got: {}".format(f)

            dmp_file_path = "{}{}".format(data_migration_policies_dir, f)
            if typ == "PROB":
                tenant_dmps[int(tenant)] = ProbabilityBasedDataMigrationPolicy(init_from_file=dmp_file_path)
            else:
                raise ValueError("Unknown data migration policy type: {}".format(typ))

        # Reading in the SLA policies from the initialization directory
        tenant_sla_policies_dir = "{}SLAs/".format(args.init_dir)
        assert os.path.isdir(tenant_sla_policies_dir), \
            "Was not able to find the tenant SLA policies directory at: {}".format(tenant_sla_policies_dir)
        # Iterate through the files in the DAPs directory
        for f in os.listdir(tenant_sla_policies_dir):
            file_name, extension = f.split('.')
            assert extension == "json", "Was expecting file name of TENANT_TYPE_SLA.json format, got: {}".format(f)

            tenant, typ, sla = file_name.split('_')
            assert sla == "SLA", "Was expecting file name of TENANT_TYPE_SLA.json format, got: {}".format(f)

            sla_file_path = "{}{}".format(tenant_sla_policies_dir, f)
            if typ == "APWL":
                tenant_slas[int(tenant)] = AveragingPiecewiseLinearSLAPenaltyFunction(logger=logger, init_from_file=sla_file_path)
            else:
                raise ValueError("Unknown tenant SLA policy type: {}".format(typ))

    # Validate the page access sequence file
    assert os.path.isfile(args.pas_file), "Page access sequence file value must be a valid path. Got: {}".format(args.pas_file)

    # Validate the simulator state dump directory if given
    assert args.sim_state_dump_dir == None or os.path.isdir(args.sim_state_dump_dir), \
        "Simulator state dump directory (if given) must be a valid path. Got: {}".format(args.sim_state_dump_dir)

    # Instantiate the BP simulator
    bpsim = BufferPoolSimulator(
        params=storage_tier_params,
        DAPs=data_admission_policies,
        DEPs=data_eviction_policies,
        SLAs=tenant_slas,
        DMPs=tenant_dmps,
        metadata=page_metadata,
        logger=logger)

    # Read in the page access requests
    N, timestamps, pages, tenants, types = 0, [], [], [], []
    with open(args.pas_file) as f:
        f.readline() # Skip the headers line

        page_access_request = f.readline().strip()
        while page_access_request:
            timestamp, page, tenant, typ = page_access_request.split(',')
            timestamp, page, tenant = int(timestamp), int(page), int(tenant)

            # We filter out requests by their timestamp (although the same is done during the simulation)
            if timestamp >= args.from_time and (args.to_time == None or timestamp <= args.to_time):
                N += 1
                timestamps.append(timestamp)
                pages.append(page)
                tenants.append(tenant)
                types.append(typ)

            page_access_request = f.readline().strip()

    # Run the simulation
    try:
        bpsim.sim(N, timestamps, pages, tenants, types, args.output_file, args.from_time, args.to_time, args.warmup)
    except Exception as e:
        logger.error("Buffer Pool Simulator crashed.")
        logger.error("Storage tier parameters: {}".format(bpsim.params))
        logger.error("Data Admission Policies: {}".format(bpsim.DAPs))
        logger.error("Data Eviction Policies: {}".format(bpsim.DEPs))
        logger.error("Tenant SLAs: {}".format(bpsim.SLAs))
        logger.error("Tenant DMPs: {}".format(bpsim.DMPs))

        raise e

    # Dump the simulator state if requested:
    if args.sim_state_dump_dir != None:
        bpsim.dump_state(args.sim_state_dump_dir, logger)
