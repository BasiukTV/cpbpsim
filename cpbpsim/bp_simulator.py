__author__ = "Taras Basiuk"

import os, logging, heapq
from collections import deque
from datetime import datetime

try: # Imports when the tool run by itself
    from slas.sla_penalty_function import AbstractSLAPenaltyFunction, AveragingPiecewiseLinearSLAPenaltyFunction
    from data_migration_policy.data_migration_policy import AbstractDataMigrationPolicy, ProbabilityBasedDataMigrationPolicy, NaiveDataMigrationPolicy, ThreeTierBufferDataMigrationPolicy
    from data_admission_policy.data_admission_policy import AbstractDataAdmissionPolicy, EagerDataAdmissionPolicy, NeverDataAdmissionPolicy, Q2DataAdmissionPolicy
    from data_eviction_policy.data_eviction_policy import AbstractDataEvictionPolicy, FIFODataEvictionPolicy, LRUEvictionPolicy, NeverDataEvictionPolicy
    from byte_addressability.byte_addressability import AbstraByteAddressabilityPolicy, NoByteAddressabilityPolicy
    from monitoring.monitoring import TenantMetricsMonitor
except ImportError: # Import when the tool is used as a dependency
    from cpbpsim.slas.sla_penalty_function import AbstractSLAPenaltyFunction, AveragingPiecewiseLinearSLAPenaltyFunction
    from cpbpsim.data_migration_policy.data_migration_policy import AbstractDataMigrationPolicy, ProbabilityBasedDataMigrationPolicy, NaiveDataMigrationPolicy, ThreeTierBufferDataMigrationPolicy
    from cpbpsim.data_admission_policy.data_admission_policy import AbstractDataAdmissionPolicy, EagerDataAdmissionPolicy, NeverDataAdmissionPolicy, Q2DataAdmissionPolicy
    from cpbpsim.data_eviction_policy.data_eviction_policy import AbstractDataEvictionPolicy, FIFODataEvictionPolicy, LRUEvictionPolicy, NeverDataEvictionPolicy
    from cpbpsim.byte_addressability.byte_addressability import AbstraByteAddressabilityPolicy, NoByteAddressabilityPolicy
    from cpbpsim.monitoring.monitoring import TenantMetricsMonitor

class BufferPoolSimulator():

    def __init__(self, workers, tier_params, DAPs, DEPs, SLAs, DMPs, BAP, metadata={}, busy_workers_heapq=[], logger=logging.getLogger(__name__)):
        """
            Constructor for the BufferPoolSimulator.
            Expects:
                workers - number of storage workers capable of simultaneously processing page access requests
                tier_params - storage tier parameters dictionary, having free space, CPU_acess flag, and SLO costs
                DAPs - storage tier data admission policies
                DEPs - storage tier data eviction policies
                SLAs - Tenant service level agreements
                DMPs - Tenant data migration policies
                BAP - Byte-addressability policy
                metadata - dictionary with page locations and dirty flags
                busy_workers_heapq - heapq queue holding timestamps of release time of currently busy workers
                logger - initialized logger
        """

        # Validate the given parameters

        assert isinstance(workers, int) and workers > 0, "workers must be a positive integer. Got: {}".format(workers)
        assert isinstance(busy_workers_heapq, list) and len(busy_workers_heapq) <= workers, \
            "busy_workers_heapq must be a heapq with no more than workers entries. Got: {}".format(busy_workers_heapq)

        # Validate the storage tier parameters
        assert isinstance(tier_params, dict), "tier_params must be a dictionary. Got: {}".format(tier_params)
        for tier in tier_params:
            assert "free_space" in tier_params[tier] and isinstance(tier_params[tier]["free_space"], int), \
                "tier_params['{}'] must have an integer mapping for 'free space'. Got: {}".format(tier, tier_params[tier])
            assert "CPU_access" in tier_params[tier] and isinstance(tier_params[tier]["CPU_access"], bool), \
                "tier_params['{}'] must have a boolean mapping for 'CPU_access'. Got: {}".format(tier, tier_params[tier])
            assert "SLO_costs" in tier_params[tier] and isinstance(tier_params[tier]["SLO_costs"], dict), \
                "tier_params['{}'] must have a dictionary mapping for 'SLO_costs'. Got: {}".format(tier, tier_params[tier])

            for access_type in tier_params[tier]["SLO_costs"]:
                assert isinstance(tier_params[tier]["SLO_costs"][access_type], dict), \
                    "tier_params['{}']['SLO_costs'][{}] must have a dictionary with SLO cost mappings. Got: {}".format(
                        tier, access_type, tier_params[tier]["SLO_costs"][access_type])

                for slo_type in tier_params[tier]["SLO_costs"][access_type]:
                    assert isinstance(tier_params[tier]["SLO_costs"][access_type][slo_type], float), \
                        "tier_params['{}']['SLO_costs'][{}][{}] must be a float. Got: {}".format(
                            tier, access_type, slo_type, tier_params[tier]["SLO_costs"][access_type][slo_type])

        # Validate the data admission policies
        assert isinstance(DAPs, dict), "DAPs must be a dictionary. Got: {}".format(DAPs)
        for tier in tier_params:
            assert tier in DAPs and isinstance(DAPs[tier], AbstractDataAdmissionPolicy), \
                "DAP for {} tier is not provided. Got: {}".format(tier, DAPs)

        # Validate the data eviction policies
        assert isinstance(DEPs, dict), "DEPs must be a dictionary. Got: {}".format(DEPs)
        for tier in tier_params:
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

        assert isinstance(BAP, AbstraByteAddressabilityPolicy), \
                "BAP must be an instance of AbstraByteAddressabilityPolicy. Got: {}".format(BAP)

        # Validate page metadata
        assert isinstance(metadata, dict), "metadata must be a dictionary. Got: {}".format(metadata)
        for pageID in metadata:
            assert isinstance(metadata[pageID], tuple) and isinstance(metadata[pageID][0], str) and isinstance(metadata[pageID][1], bool), \
                "metadata must map pageIDs to tuples of strings and booleans. Got: {}".format(metadata[pageID])

        self.workers = workers
        self.tier_params = tier_params
        self.DAPs = DAPs
        self.DEPs = DEPs
        self.SLAs = SLAs
        self.DMPs = DMPs
        self.BAP = BAP

        heapq.heapify(busy_workers_heapq)
        self.busy_workers_heapq = busy_workers_heapq

        self.metadata = metadata
        self.logger = logger
        self.monitor = TenantMetricsMonitor(logger)

        logger.info("Instantiating the Buffer Pool Simulator.")
        logger.debug("Workers: {}, Busy workers heap queue: {}".format(self.workers, self.busy_workers_heapq))
        logger.debug("Storage tier parameters: {}".format(self.tier_params))
        logger.debug("Page metadata: {}".format(self.metadata))
        logger.debug("Data Admission Policies: {}".format(self.DAPs))
        logger.debug("Data Eviction Policies: {}".format(self.DEPs))
        logger.debug("Tenant SLAs: {}".format(self.SLAs))
        logger.debug("Tenant DMPs: {}".format(self.DMPs))
        logger.debug("Byte Addressability Policy: {}".format(self.BAP))
        logger.debug("Tenant Metrics Monitor: {}".format(self.monitor))

    def init_from_dir(init_dir, logger=logging.getLogger(__name__)):
        assert os.path.isdir(init_dir), "Given simulator initialization directory is invalid: {}".format(args.init_dir)

        import json

        # Container for all parameters
        workers = None
        busy_workers_heapq = []
        storage_tier_params = {}
        page_metadata = {}
        data_admission_policies = {}
        data_eviction_policies = {}
        byte_addressability_policy = None
        tenant_dmps = {}
        tenant_slas = {}

        # Read in the number of storage workers and current busy workers heap queue
        bpsim_params_file = "{}bpsim_params.json".format(init_dir)
        assert os.path.isfile(bpsim_params_file), "Was not able to find the bp simulator parameters file at: {}".format(bpsim_params_file)
        with open(bpsim_params_file) as f:
            bpsim_params = json.load(f)
            workers = bpsim_params['workers']
            busy_workers_heapq = bpsim_params['busy_workers_heapq']
            heapq.heapify(busy_workers_heapq)

        # Reading in the storage tier parameters from the initialization directory
        storage_tier_params_file = "{}tier_params.json".format(init_dir)
        assert os.path.isfile(storage_tier_params_file), "Was not able to find the storage tier parameters file at: {}".format(storage_tier_params_file)
        with open(storage_tier_params_file) as f:
            storage_tier_params = json.load(f)

        # Reading in the page metadata from the initialization directory
        page_metadata_file = "{}tier_metadata.json".format(init_dir)
        assert os.path.isfile(page_metadata_file), "Was not able to find the storage tier metadata file at: {}".format(page_metadata_file)
        with open(page_metadata_file) as f:
            page_metadata = dict(map(lambda kv: (int(kv[0]), (kv[1][0], kv[1][1])), json.load(f).items()))

        # Reading in the byte addressability policy from the initialization directory
        byte_addressability_dir = "{}BAPs/".format(init_dir)
        assert os.path.isdir(byte_addressability_dir), \
            "Was not able to find the byte addressability policy directory at: {}".format(byte_addressability_dir)
        byte_addressability_files = os.listdir(byte_addressability_dir)
        assert len(byte_addressability_files) == 1, \
            "Was only expecting single byte addressability file in the {} directory. Got: {}".format(byte_addressability_dir, byte_addressability_files)

        f = byte_addressability_files[0]
        file_name, extension = f.split('.')
        assert extension == "json", "Was expecting file name of TYPE_BAP.json format, got: {}".format(f)
        typ, bap = file_name.split('_')
        assert bap == "BAP", "Was expecting file name of TYPE_BAP.json format, got: {}".format(f)
        bap_file_path = "{}{}".format(byte_addressability_dir, f)
        if typ == "NO":
            byte_addressability_policy = NoByteAddressabilityPolicy(init_from_file=bap_file_path)
        else:
            raise ValueError("Unknown byte addressability policy type: {}".format(typ))

        # Reading in the data admission policies from the initialization directory
        data_admission_policies_dir = "{}DAPs/".format(init_dir)
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
        data_eviction_policies_dir = "{}DEPs/".format(init_dir)
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
            elif typ == "NEV":
                data_eviction_policies[tier] = NeverDataEvictionPolicy(init_from_file=dep_file_path)
            else:
                raise ValueError("Unknown data eviction policy type: {}".format(typ))

        # Reading in the data migration policies from the initialization directory
        data_migration_policies_dir = "{}DMPs/".format(init_dir)
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
            elif typ == "NAI":
                tenant_dmps[int(tenant)] = NaiveDataMigrationPolicy(init_from_file=dmp_file_path)
            elif typ == "3TB":
                tenant_dmps[int(tenant)] = ThreeTierBufferDataMigrationPolicy(init_from_file=dmp_file_path)
            else:
                raise ValueError("Unknown data migration policy type: {}".format(typ))

        # Reading in the SLA policies from the initialization directory
        tenant_sla_policies_dir = "{}SLAs/".format(init_dir)
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

        # Instantiate and return the BP simulator
        return BufferPoolSimulator(
            workers = workers,
            tier_params=storage_tier_params,
            DAPs=data_admission_policies,
            DEPs=data_eviction_policies,
            SLAs=tenant_slas,
            DMPs=tenant_dmps,
            BAP = byte_addressability_policy,
            busy_workers_heapq = busy_workers_heapq,
            metadata=page_metadata,
            logger=logger)

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

        logger.info("Starting the simulation. Number of requests to process: {}".format(N))
        progress_percentile = 0.05
        for i in range(N):

            if (i + 1) > N * progress_percentile:
                logger.info("Processed {} requests. Or at least: {}%".format(i + 1, int(progress_percentile * 100)))
                progress_percentile = progress_percentile + 0.05

            time, pageID, tenantID, access_type = timestamps[i], pages[i], tenants[i], types[i]

            # Skip the request if its timestamp is below from_time or above to_time
            if time < from_time or (to_time != None and time > to_time):
                continue

            logger.debug("Page access request #{} - time:{}, pageID:{}, tenantID:{}, access_type:{}".format(
                i + 1, time, pageID, tenantID, access_type))

            # Free up workers
            time_micro = time * 1000 # Convert the timestamp into microseconds

            # Free up all the workers who are finished by the current timestamps
            while len(self.busy_workers_heapq) > 0 and self.busy_workers_heapq[0] <= time_micro:
                heapq.heappop(self.busy_workers_heapq)

            # If there aren't any free workers available, wait for the first one to become available
            # If SLO is latency, add waiting for the free worker to the SLO
            slo_val = 0
            wait_until = time_micro
            worker_waiting = 0
            if len(self.busy_workers_heapq) >= self.workers:
                wait_until = heapq.heappop(self.busy_workers_heapq)
                worker_waiting = wait_until - time_micro

                if self.SLAs[tenantID].slo_type == "latency":
                    slo_val += worker_waiting * 1000 # Latency SLO is recorded in nano seconds
                    logger.debug("Had to wait for a free storage worker for {} microseconds.".format(worker_waiting))

            # Retrieve the current storage tier the page ID belongs to
            # Check whether the page is new
            if pageID not in self.metadata:
                self.metadata[pageID] = ("SSD", False)
                self.tier_params["SSD"]["free_space"] = self.tier_params["SSD"]["free_space"] - 1
                logger.debug("Encountered pageID:{} for the first time. Assuming it's on SSD tier and not dirty. Free SSD space: {}.".format(
                    pageID, self.tier_params["SSD"]["free_space"]))

            tier, dirty = self.metadata[pageID]
            logger.debug("Found pageID:{} on storage tier:{} dirty:{}".format(pageID, tier, dirty))

            data_access_chain = deque()
            if not self.DAPs[tier].should_admit(pageID) and self.tier_params[tier]["CPU_access"]:
                # If the page should not be admitted to a different tier and the current tier is accessible by the CPU
                # Just add the page access request to the chain
                data_access_chain.appendleft((pageID, tier, access_type))
            else:
                # Find the new storage tier for the page admission
                new_tier = self.DMPs[tenantID].destination_on_admission_from(time, pageID, tier)
                while not self.tier_params[new_tier]["CPU_access"]:
                    new_tier = self.DMPs[tenantID].destination_on_admission_from(time, pageID, new_tier)

                # This is the final part of the chain, actually servicing the request
                data_access_chain.appendleft((pageID, new_tier, access_type))

                # Before we can service the page we need to read it from its source tier
                # and copy it over to it's new destination tier
                data_access_chain.appendleft((pageID, new_tier, "copy"))
                data_access_chain.appendleft((pageID, tier, "read"))

                logger.debug("pageID:{} will be admitted from {} to {} tier per DMP of tenantID:{}".format(
                    pageID, tier, new_tier, tenantID))

                # Remove the page from the residency with the DEP in the old tier
                self.DEPs[tier].update_residency(pageID, False)
                if tier != "SSD":
                    self.tier_params[tier]["free_space"] = self.tier_params[tier]["free_space"] + 1
                    logger.debug("{} tier remaining free space: {}".format(tier, self.tier_params[tier]["free_space"]))

                # Make sure the new tier has enough free space
                victim_page = pageID
                while True:
                    if self.tier_params[new_tier]["free_space"] > 0:
                        self.tier_params[new_tier]["free_space"] = self.tier_params[new_tier]["free_space"] - 1
                        logger.debug("{} tier remaining free space: {}".format(new_tier, self.tier_params[new_tier]["free_space"]))
                        break
                    else:
                        old_victim_page = victim_page
                        victim_page = self.DEPs[new_tier].evict()
                        old_tier = new_tier
                        new_tier = self.DMPs[tenantID].destination_on_eviction_from(time, victim_page, new_tier)
                        logger.debug("pageID:{} dirty:{} will be copied from {} to {} tier to make space for pageID:{}".format(
                            victim_page, self.metadata[victim_page][1], old_tier, new_tier, old_victim_page))
                        if not self.metadata[victim_page][1] and new_tier == "SSD":
                            # If the victim page is not dirty and the destination tier is "SSD",
                            # just update the metadata to point to its new location,
                            # But we don't need to copy it over as SSD already contains its clean copy
                            self.metadata[victim_page] = ("SSD", False)
                            break
                        else:
                            # Victim page has to actually be migrated, first we read it from it's old tier
                            # and then copy it over to its new tier
                            data_access_chain.appendleft((victim_page, new_tier, "copy"))
                            data_access_chain.appendleft((victim_page, old_tier, "read"))

            # Process the data access chain
            logger.debug("Page access request #{} data access chain: {}".format(i + 1, data_access_chain))
            wait_until *= 1000 # Convert worker busy until time to nanoseconds
            for j in range(len(data_access_chain)):
                # Update the SLO costs
                d_pageID, d_tier, d_access_type = data_access_chain[j] # Destination pageID, tier and access type
                if time >= warmup:
                    slo_val += self.tier_params[d_tier]["SLO_costs"][d_access_type][self.SLAs[tenantID].slo_type]
                    wait_until = int(wait_until + self.tier_params[d_tier]["SLO_costs"][d_access_type]["latency"])
                if d_access_type == "copy":
                    # When the page is copied over it has to become a resident of the destination storage tier
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

            # Block the worker until the page processing is finished (convert wait_until to microseconds again)
            heapq.heappush(self.busy_workers_heapq, wait_until // 1000)

            # Record page access request for DAPs and DEPs
            for t in self.DAPs:
                self.DAPs[t].record_access(time, pageID, access_type)
            for t in self.DEPs:
                self.DEPs[t].record_access(time, pageID, t == self.metadata[pageID][0], access_type)

            # Record monitoring metrics
            if time >= warmup:
                self.monitor.record_metric(time, tenantID, tier, data_access_chain, slo_val, worker_waiting)

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

        file_name = "{}bpsim_params.json".format(dump_dir)
        logger.info("Dumping the BP simulator parameters into: {}".format(file_name))
        with open(file_name, 'w') as f:
            json.dump({'workers': self.workers, 'busy_workers_heapq': self.busy_workers_heapq}, f)

        file_name = "{}tier_params.json".format(dump_dir)
        logger.info("Dumping the storage tier parameters into: {}".format(file_name))
        with open(file_name, 'w') as f:
            json.dump(self.tier_params, f)

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
            elif isinstance(self.DEPs[dep], NeverDataEvictionPolicy):
                typ = "NEV"
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
            elif isinstance(self.DMPs[dmp], NaiveDataMigrationPolicy):
                typ = "NAI"
            elif isinstance(self.DMPs[dmp], ThreeTierBufferDataMigrationPolicy):
                typ = "3TB"
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

        # Dumping byte addressability policy
        os.makedirs("{}BAPs/".format(dump_dir), exist_ok=True)
        typ = None
        if isinstance(self.BAP, NoByteAddressabilityPolicy):
            typ = "NO"
        else:
            raise ValueError("Unknown byte addressability policy name: {}".format(self.BAP))

        file_name = "{}BAPs/{}_BAP.json".format(dump_dir, typ)
        logger.info("Dumping the byte addressability policy tenant into: {}".format(file_name))
        self.BAP.persist_to_file(file_name)

if __name__ == "__main__":

    # Default values
    DEFAULT_WORKERS = 10

    DEFAULT_TIER_PARAMS_FILE = "data_sets/tier_params.csv"
    DEFAULT_TIER_DAPS_FILE = "data_sets/tier_daps.csv"
    DEFAULT_TIER_DEPS_FILE = "data_sets/tier_deps.csv"
    DEFAULT_TENANT_SLAS_FILE = "data_sets/tenant_slas.csv"
    DEFAULT_TENANT_DMPS_FILE = "data_sets/tenant_dmps.csv"
    DEFAULT_BAP_FILE = "data_sets/byte_addressability.csv"
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
                    -P, -A, -E, -T, -D, -B.
                They will be read in from the directory.''')
    parser.add_argument('-WS', '--workers', type=int, default=DEFAULT_WORKERS,
        help='Number of storage workers capable of simultaneously processing page access requests. Default: {}'.format(DEFAULT_WORKERS))
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
    parser.add_argument('-B', '--byte-addressability', type=str, default=DEFAULT_BAP_FILE,
        help="""Input file with byte addressability policy. Expected contents:
                    header1,header2,header3,...
                    bapType1,param0,param1,...
                Default: {}""".format(DEFAULT_BAP_FILE))
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

    cpbpsim = None
    # If initializing from separate files
    if args.init_dir == None:
        storage_tier_params = {} # Container for all storage tier parameters
        page_metadata = {} # Start with cold buffer pool
        data_admission_policies = {}
        data_eviction_policies = {}
        tenant_dmps = {}
        byte_addressability_policy = None
        tenant_slas = {}

        assert args.workers > 0, "Number of storage workers must be positive. Got: {}".format(args.workers)

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
                elif policy == "NEV":
                    data_eviction_policies[tier] = NeverDataEvictionPolicy()
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
                elif dmp_type == "NAI":
                    raise ValueError("NaiveDataMigrationPolicy instantiation from the CLI is not supported yet.")
                elif dmp_type == "3TB":
                    raise ValueError("ThreeTierBufferDataMigrationPolicy instantiation from the CLI is not supported yet.")
                else:
                    raise ValueError("Unknown DMP type: {}".format(dmp_type))

                dmp = f.readline().strip()

        # Read in and validate byte addressability policy
        assert os.path.isfile(args.byte_addressability), "Byte addressability policy file value must be a valid path. Got: {}".format(args.byte_addressability)
        with open(args.byte_addressability) as f:
            f.readline() # Skip the headers line
            bap_params = f.readline().strip().split(',')

            assert len(bap_params) >= 1, "Byte addressability policy must contain at least one parameter. Got: {}".format(bap_params)

            bap_type = bap_params[0]

            if bap_type == "NO":
                byte_addressability_policy = NoByteAddressabilityPolicy()
            else:
                raise ValueError("Unknown byte addressability policy type: {}".format(bap_type))

        # Instantiate the BP simulator
        bpsim = BufferPoolSimulator(
            workers = args.workers,
            tier_params=storage_tier_params,
            DAPs=data_admission_policies,
            DEPs=data_eviction_policies,
            SLAs=tenant_slas,
            DMPs=tenant_dmps,
            BAP=byte_addressability_policy,
            metadata=page_metadata,
            logger=logger)
    else:
        # If we're initializing the simulator from the directory of dumped state
        bpsim = BufferPoolSimulator.init_from_dir(args.init_dir, logger)

    # Validate the page access sequence file
    assert os.path.isfile(args.pas_file), "Page access sequence file value must be a valid path. Got: {}".format(args.pas_file)

    # Validate the simulator state dump directory if given
    assert args.sim_state_dump_dir == None or os.path.isdir(args.sim_state_dump_dir), \
        "Simulator state dump directory (if given) must be a valid path. Got: {}".format(args.sim_state_dump_dir)

    # Read in the page access requests
    N, timestamps, pages, tenants, types = 0, [], [], [], []
    with open(args.pas_file) as f:

        file_size = os.path.getsize(args.pas_file)

        # If we have to start with the timestamp more than a minute away and the file is larger than 100MB, we should quickly seek to it
        page_access_request = None
        if args.from_time > 60000 and file_size > 100 * 1024 * 1024:

            seek_to = file_size // 2
            seek_step = seek_to // 2
            f.seek(seek_to)
            f.readline() # Assuming we landed in the middle of some line, get to the end of it
            page_access_request = f.readline().strip() # Read the first normal line
            timestamp = int(page_access_request.split(',')[0])

            # We need to land within a minute of from_time but no longer than that
            while not (timestamp <= args.from_time and timestamp + 60000 >= args.from_time):
                if timestamp <= args.from_time:
                    # We didn't go far enough
                    seek_to += seek_step
                else:
                    # We overshot, need to back-off a bit
                    seek_to -= seek_step

                seek_step = seek_step // 2
                f.seek(seek_to)
                f.readline()
                page_access_request = f.readline().strip()
                timestamp = int(page_access_request.split(',')[0])

        else:
            f.readline() # Otherwise, just skip the headers line
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

            # Stop processing the file once the to_time timestamps is reached
            if args.to_time != None and timestamp > args.to_time:
                break

            page_access_request = f.readline().strip()

    # Run the simulation
    try:
        bpsim.sim(N, timestamps, pages, tenants, types, args.output_file, args.from_time, args.to_time, args.warmup)
    except Exception as e:
        logger.error("Buffer Pool Simulator crashed.")
        logger.error("Storage tier parameters: {}".format(bpsim.tier_params))
        logger.error("Data Admission Policies: {}".format(bpsim.DAPs))
        logger.error("Data Eviction Policies: {}".format(bpsim.DEPs))
        logger.error("Tenant SLAs: {}".format(bpsim.SLAs))
        logger.error("Tenant DMPs: {}".format(bpsim.DMPs))
        logger.error("Byte Addressability Policy: {}".format(bpsim.BAP))

        raise e

    # Dump the simulator state if requested:
    if args.sim_state_dump_dir != None:
        bpsim.dump_state(args.sim_state_dump_dir, logger)
