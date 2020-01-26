__author__ = "Taras Basiuk"

if __name__ == "__main__":

    DEFAULT_OUTPUT_FILE = "../data_sets/page_access_sequence.csv"
    DEFAULT_OUTPUT_FILE_OVERWRITE = False

    DEFAULT_TENANTS = 5
    DEFAULT_DURATION = 1800
    DEFAULT_ACESS_RATE = 1.0
    DEFAULT_ACESS_DISTRIBUTION = "NOR_20"
    DEFAULT_DATA_SIZE = 100
    DEFAULT_READ_FRACTION = 0.9

    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''
        This tool generates the multi-tenant page access sequence to be used by a buffer pool simulator.

        Output CSV format (sorted by timestamp in ascending order):
            header1,header2,header3...
            timestamp(ms),tenantID,pageID,access_type(read/update)
            timestamp(ms),tenantID,pageID,access_type(read/update)
            ...

        Notes:
            -Page IDs are disjoint between tenants.
            -Page access timestamps follow uniform distribution for the sequence duration according to the tenant page access rate.
        ''')

    parser.add_argument('-O', '--output', type=str, default=DEFAULT_OUTPUT_FILE,
        help='Output file name. Default: {}'.format(DEFAULT_OUTPUT_FILE))
    parser.add_argument('--overwrite', action='store_const', const=True, default=DEFAULT_OUTPUT_FILE_OVERWRITE,
        help='Allows for the output file overwrite. Default: {}'.format(DEFAULT_OUTPUT_FILE_OVERWRITE))

    parser.add_argument('-N', '--tenants', type=int, default=DEFAULT_TENANTS,
        help='Number of tenants causing page accesses. Default: {}'.format(DEFAULT_TENANTS))
    parser.add_argument('-T', '--time', type=int, default=DEFAULT_DURATION,
        help='Time duration of the generated sequence (in seconds). Default: {}'.format(DEFAULT_DURATION))
    parser.add_argument('-R', '--access-rate', type=float, nargs='+', default=[DEFAULT_ACESS_RATE] * DEFAULT_TENANTS,
        help='Page access rate for each tenant (in accesses per second). Default: {} for each tenant.'.format(DEFAULT_ACESS_RATE))
    parser.add_argument('-D', '--access-distribution', type=str, nargs='+', default=[DEFAULT_ACESS_DISTRIBUTION] * DEFAULT_TENANTS,
        help="""Page access distribution for each tenant. 
                Options are 'UNI' (for uniform), 'PAR_X' for Pareto distribution with X alpha parameter, 
                'NOR_X' for normal (Gaussian) distribution with X standard deviations (as percentage of available pages). 
                Default: {} for each tenant.""".format(DEFAULT_ACESS_DISTRIBUTION))
    parser.add_argument('-S', '--data-size', type=int, nargs='+', default=[DEFAULT_DATA_SIZE] * DEFAULT_TENANTS,
        help='Data size for each tenant in total pages on disk. Default: {} for each tenant.'.format(DEFAULT_DATA_SIZE))
    parser.add_argument('-F', '--read-fraction', type=float, nargs='+', default=[DEFAULT_READ_FRACTION] * DEFAULT_TENANTS,
        help='Read accesses fraction for each tenant. Default: {} for each tenant.'.format(DEFAULT_READ_FRACTION))

    # Parsed arguments validation
    args = parser.parse_args()
    if args.tenants != len(args.access_rate):
        print("Error! Expected {} tenant access rates. Got {}. Exiting!".format(args.tenants, len(args.access_rate)))
    elif args.tenants != len(args.data_size):
        print("Error! Expected {} tenant data sizes. Got {}. Exiting!".format(args.tenants, len(args.data_size)))
    elif args.tenants != len(args.read_fraction):
        print("Error! Expected {} tenant read fractions. Got {}. Exiting!".format(args.tenants, len(args.read_fraction)))
    elif args.tenants != len(args.access_distribution):
        print("Error! Expected {} tenant access distributions. Got {}. Exiting!".format(args.tenants, len(args.access_distribution)))
    else:
        invalid_access_distribution = False
        for ad in args.access_distribution:
            if ad == "UNI":
                continue
            distribution_type, param = ad.split('_')
            if distribution_type in {"PAR", "NOR"} and param.isdigit():
                continue

            print("Error! Unexpected tenant access distribution {}. Expecting UNI, PAR_X, NOR_X. Exiting!".format(ad))
            invalid_access_distribution = True
            break

        if not invalid_access_distribution:
            # Check that the file can be opened
            with open(args.output, 'w' if args.overwrite else 'x') as output_file:
                output_file.write("timestamp,pageID,tenantID,access_type\n")

                import random

                result = []
                first_page_id = 0 # Counter which helps to make tenant page IDs disjoint

                for t in range(args.tenants):

                    # Calculate/extract desired number of samples, page access distribution type, data size and read fraction
                    samples = int(args.time * args.access_rate[t])
                    distribution_type, param = args.access_distribution[t], None
                    if distribution_type != "UNI":
                        distribution_type, param = args.access_distribution[t].split('_')
                        param = int(param)
                    data_size = args.data_size[t]
                    read_fraction = args.read_fraction[t]
                    print("For tenant #{}, generating {} samples with {} distribution for {} pages and {} fraction of reads."
                        .format(t + 1, samples,
                            "uniform" if distribution_type == "UNI" else
                            "normal (sigma={})".format((param * data_size) // 100) if distribution_type == "NOR" else
                            "Pareto (alpha={})".format(param),
                            data_size, read_fraction))

                    # For each sample
                    for s in range(samples):
                        pageID = None # Generate accessed pageID according to the chosen distribution
                        if distribution_type == "UNI":
                            pageID = int(random.uniform(first_page_id, first_page_id + data_size))
                        elif distribution_type == "NOR":
                            # Set the mean of the distribution to the ID of the page in the middle of allowed range,
                            # and calculate the standard deviation to be a number of page IDs corresponding to the given percentage of the range.
                            pageID = int(random.gauss(first_page_id + (data_size // 2), (param * data_size) // 100))
                            # Normal distribution is unbounded, so we retry when the page ID is outside of expected range
                            while pageID < first_page_id or pageID >= first_page_id + data_size:
                                pageID = int(random.gauss(first_page_id + (data_size // 2), (param * data_size) // 100))
                        elif distribution_type == "PAR":
                            rand_var = random.paretovariate(param)
                            # Pareto distribution is unbounded, so we retry when generated random variable is over 11
                            while rand_var > 11.0:
                                rand_var = random.paretovariate(param)

                            # Convert the generated random variable to the page ID, first page ID in range being most likely
                            pageID = first_page_id + int(((rand_var - 1) / 10) * data_size)

                        # Generate the timestamps and write versus read using uniform distribution
                        result.append((int(1000 * args.time * random.random()), pageID, t + 1, 'read' if random.random() <= read_fraction else 'update'))

                    first_page_id += data_size # Shift the first allowed page in the range for the next tenant

                print("Sorting samples according to their timestamps.")

                from operator import itemgetter
                result = sorted(result, key=itemgetter(0))

                print("Writing out sorted samples to the file: {}".format(args.output))
                for s in result:
                    output_file.write("{},{},{},{}\n".format(s[0], s[1], s[2], s[3]))

                print("Done. Exiting!")

