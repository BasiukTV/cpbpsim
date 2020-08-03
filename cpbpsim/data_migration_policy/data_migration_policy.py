__author__ = "Taras Basiuk"

import random
from abc import ABC, abstractmethod

class AbstractDataMigrationPolicy(ABC):
    """
        This abstract class sets requirements for data migration policies whose purpose is to
        decide the destination of a data page upon its admission/eviction from its current storage tier.
    """

    @abstractmethod
    def __init__(self, config_params=None, init_from_file=None):
        """Initialize the policy with the given policy config parameters."""
        pass

    @abstractmethod
    def destination_on_admission_from(self, timestamp, pageID, source):
        """Returns a destination storage tier of the data page when it's admitted from source storage tier."""
        pass

    @abstractmethod
    def destination_on_eviction_from(self, timestamp, pageID, source):
        """Returns a destination storage tier of the data page when it's evicted from source storage tier."""
        pass

    @abstractmethod
    def persist_to_file(self, file_name):
        """Persists the state of the policy to a file, from which it can be later recovered."""
        pass

class NaiveDataMigrationPolicy(AbstractDataMigrationPolicy):
    """
        This policy simply admits data from SSD to NVM and then to RAM,
        and it evicts data from RAM to NVM and then to RAM.
    """

    def __init__(self, config_params=None, init_from_file=None):
        """If init_from_file is give, check that it exists, but that's it."""
        with open(init_from_file) as _:
            pass

    def destination_on_admission_from(self, timestamp, pageID, source):
        """If source is SSD return NVM, if source is NVM return RAM."""
        if source == "SSD":
            return "NVM"
        elif source == "NVM":
            return "RAM"
        elif source == "RAM":
            return "RAM"
        else:
            raise ValueError("Unexpected source data tier: {}".format(source))

    def destination_on_eviction_from(self, timestamp, pageID, source):
        """If source is NVM return SSD, if source is RAM return NVM."""
        if source == "SSD":
            return "SSD"
        elif source == "NVM":
            return "SSD"
        elif source == "RAM":
            return "NVM"
        else:
            raise ValueError("Unexpected source data tier: {}".format(source))

    def persist_to_file(self, file_name):
        """Just make an empty file, there's nothing else to persist."""
        with open(file_name, 'w') as _:
            pass

class ThreeTierBufferDataMigrationPolicy(AbstractDataMigrationPolicy):
    """
        This policy acts like naive DMP for admissions.

        But, upon the every first eviction from RAM page is migrated to SSD, but it's ID is recorded.
        Upon the every second eviction from RAM page is migrated to NVM and it's ID record cleared.
        Upon eviction from NVM the page is always migrated to SSD.
    """

    def __init__(self, config_params=None, init_from_file=None):
        """This constructor initializes a set to record page IDs."""

        self.record = set()

        if init_from_file:
            # If the file is given, simply populate the record set with its contents.
            import json
            with open(init_from_file) as f:
                self.record = set(json.load(f))

    def destination_on_admission_from(self, timestamp, pageID, source):
        """If source is SSD return NVM, if source is NVM return RAM."""
        if source == "SSD":
            return "NVM"
        elif source == "NVM":
            return "RAM"
        elif source == "RAM":
            return "RAM"
        else:
            raise ValueError("Unexpected source data tier: {}".format(source))

    def destination_on_eviction_from(self, timestamp, pageID, source):
        """If source is NVM return SSD, if source is RAM return NVM."""
        if source == "SSD":
            return "SSD"
        elif source == "NVM":
            return "SSD"
        elif source == "RAM":
            if pageID in self.record:
                self.record.remove(pageID)
                return "NVM"
            else:
                self.record.add(pageID)
                return "SSD"
        else:
            raise ValueError("Unexpected source data tier: {}".format(source))

    def persist_to_file(self, file_name):
        """Just save the record of Page IDs to a given file."""
        import json
        with open(file_name, 'w') as f:
            json.dump(list(self.record), f)

class ProbabilityBasedDataMigrationPolicy(AbstractDataMigrationPolicy):
    """
        This data migration policy determines the data page destination according to the preset probabilities
        and a uniform distribution of a random variable
    """

    def __init__(self, config_params=None, init_from_file=None):
        if init_from_file:
            # If the file is given, populate the tiers, tier_index, data_admission_matrix and data_eviction_matrix from the file.
            import json
            with open(init_from_file) as f:
                persisted_state = json.load(f)
                self.tiers = persisted_state['tiers']
                self.tier_index = persisted_state['tier_index']
                self.data_admission_matrix = persisted_state['data_admission_matrix']
                self.data_eviction_matrix = persisted_state['data_eviction_matrix']
        else:
            # Unpacking expected config_params
            assert "tiers" in config_params, "config_params is expected to contain 'tiers'"
            tiers = config_params["tiers"]
            assert "data_admission_matrix" in config_params, "config_params is expected to contain 'data_admission_matrix'"
            data_admission_matrix = config_params["data_admission_matrix"]
            assert "data_eviction_matrix" in config_params, "config_params is expected to contain 'data_eviction_matrix'"
            data_eviction_matrix = config_params["data_eviction_matrix"]

            # Input parameters validation
            assert isinstance(tiers, list) and all(list(map(lambda a: isinstance(a, str), tiers))), \
                "tiers must be a list of strings. Got: {}".format(tiers)

            assert isinstance(data_admission_matrix, list), "data_admission_matrix must be a list. Got: {}".format(data_admission_matrix)
            assert isinstance(data_eviction_matrix, list), "data_eviction_matrix must be a list. Got: {}".format(data_admission_matrix)

            assert len(tiers) == len(data_admission_matrix), \
                "data admission matrix must have one sublist per tiers entry. Got: {}".format(data_admission_matrix)
            assert len(tiers) == len(data_eviction_matrix), \
                "data eviction matrix must have one sublist per tiers entry. Got: {}".format(data_eviction_matrix)

            assert all(list(map(lambda a: isinstance(a, list) and len(a) == len(tiers) and \
                all(list(map(lambda b: isinstance(b, float), a))) and \
                sum(a) - 1.0 < 10 ** -6, data_admission_matrix))), \
                "All data_admission_matrix values must be lists with one float value per tier adding up to a 1.0 Got: {}".format(data_admission_matrix)

            assert all(list(map(lambda a: isinstance(a, list) and len(a) == len(tiers) and \
                all(list(map(lambda b: isinstance(b, float), a))) and \
                sum(a) - 1.0 < 10 ** -6, data_eviction_matrix))), \
                "All data_eviction_matrix values must be lists with one float value per tier adding up to a 1.0 Got: {}".format(data_eviction_matrix)

            # Populate the member variables
            self.tiers = tiers
            self.tier_index = {}
            for i in range(len(tiers)):
                self.tier_index[tiers[i]] = i

            self.data_admission_matrix = data_admission_matrix
            self.data_eviction_matrix = data_eviction_matrix

    def __str__(self):
        return "ProbabilityBasedDataMigrationPolicy(tiers={}, data_admission_matrix={}, data_eviction_matrix={})".format(
            self.tiers, self.data_admission_matrix, self.data_eviction_matrix)

    def __repr__(self):
        return str(self)

    def destination_on_admission_from(self, timestamp, pageID, source):
        """Returns a destination storage tier of the data page when it's admitted from given storage tier."""
        r = random.random()
        tier_index = self.tier_index[source]
        cutoff = 0.0
        for i in range(len(self.tiers)):
            cutoff += self.data_admission_matrix[tier_index][i]

            if cutoff > r:
                return self.tiers[i]

        return self.tiers[-1]


    def destination_on_eviction_from(self, timestamp, pageID, source):
        """Returns a destination storage tier of the data page when it's evicted from given storage tier."""
        r = random.random()
        tier_index = self.tier_index[source]
        cutoff = 0.0
        for i in range(len(self.tiers)):
            cutoff += self.data_eviction_matrix[tier_index][i]

            if cutoff > r:
                return self.tiers[i]

        return self.tiers[-1]

    def persist_to_file(self, file_name):
        """We save the contents of the tiers, tier_index, data_admission_matrix and data_eviction_matrix to the file."""

        import json
        with open(file_name, 'w') as f:
            json.dump({
                'tiers': self.tiers,
                'tier_index': self.tier_index,
                'data_admission_matrix': self.data_admission_matrix,
                'data_eviction_matrix' : self.data_eviction_matrix
            }, f)

if __name__ == "__main__":

    # Default values
    DEFAULT_TIERS = ["SSD", "NVM", "RAM"]
    DEFAULT_ADMISSION_MATRIX = [0.0, 0.5, 0.5, 0.0, 0.1, 0.9, 0.0, 0.0, 1.0]
    DEFAULT_EVICTION_MATRIX = [1.0, 0.0, 0.0, 0.9, 0.1, 0.0, 0.5, 0.5, 0.0]

    DEFAULT_ADMISSION_EVALUATIONS = ["SSD", 1000, "NVM", 1000, "RAM", 1000]
    DEFAULT_EVICTION_EVALUATIONS = ["SSD", 1000, "NVM", 1000, "RAM", 1000]

    # Simple testing space
    """
    bps = ProbabilityBasedDataMigrationPolicy({
        "tiers": DEFAULT_TIERS,
        "data_admission_matrix" : [[0.0, 0.5, 0.5], [0.0, 0.1, 0.9], [0.0, 0.0, 1.0]],
        "data_eviction_matrix" : [[1.0, 0.0, 0.0], [0.9, 0.1, 0.0], [0.5, 0.5, 0.0]]})
    print(bps)
    bps.persist_to_file('test.json')
    bps = ProbabilityBasedDataMigrationPolicy(init_from_file='test.json')
    print(bps)
    
    ttbdmp = ThreeTierBufferDataMigrationPolicy()
    print(ttbdmp.destination_on_eviction_from(0, 1, "RAM"))
    print(ttbdmp.destination_on_eviction_from(0, 1, "RAM"))
    print(ttbdmp.destination_on_eviction_from(0, 2, "RAM"))
    print(ttbdmp.destination_on_eviction_from(0, 3, "RAM"))
    ttbdmp.persist_to_file('test.json')
    ttbdmp = ThreeTierBufferDataMigrationPolicy(init_from_file='test.json')
    print(ttbdmp.destination_on_eviction_from(0, 1, "RAM"))
    print(ttbdmp.destination_on_eviction_from(0, 2, "RAM"))
    """

    # Parse given arguments
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''
            This tool evaluates the probability based data migration policy for a given
            number of admissions and evictions from the given buffer pool storage tiers.
        ''')

    parser.add_argument('-T', '--tiers', type=str, nargs='+', default=DEFAULT_TIERS,
        help='Buffer pool storage tiers. Format: [name_1, name_2, name_3...] Default: {}'.format(DEFAULT_TIERS))
    parser.add_argument('-A', '--admission-matrix', type=float, nargs='+', default=DEFAULT_ADMISSION_MATRIX,
        help='Flattened square matrix for probabilities of data page migration upon admission from the row tier to column tier. ' + 
        'Format: [prob_0_to_0, prob_0_to_1, prob_0_to_2, prob_1_to_0, ...] Default: {}'.format(DEFAULT_ADMISSION_MATRIX))
    parser.add_argument('-E', '--eviction-matrix', type=float, nargs='+', default=DEFAULT_EVICTION_MATRIX,
        help='Flattened square matrix for probabilities of data page migration upon eviction from the row tier to column tier. ' + 
        'Format: [prob_0_to_0, prob_0_to_1, prob_0_to_2, prob_1_to_0, ...] Default: {}'.format(DEFAULT_EVICTION_MATRIX))
    parser.add_argument('-AE', '--admission-evaluations', type=str, nargs='+', default=DEFAULT_ADMISSION_EVALUATIONS,
        help='Number if admissions to evaluate. Format: [tier1, number1, tier2, number2, ...] Default: {}'.format(DEFAULT_ADMISSION_EVALUATIONS))
    parser.add_argument('-EE', '--eviction-evaluations', type=str, nargs='+', default=DEFAULT_EVICTION_EVALUATIONS,
        help='Number if evictions to evaluate. Format: [tier1, number1, tier2, number2, ...] Default: {}'.format(DEFAULT_EVICTION_EVALUATIONS))
    args = parser.parse_args()

    # Validate given parameters
    assert len(args.admission_matrix) == len(args.tiers) ** 2, \
        "admission_matrix must be flatten square matrix of order {}. Got: {}".format(len(args.tiers), args.admission_matrix)
    assert len(args.eviction_matrix) == len(args.tiers) ** 2, \
        "eviction_matrix must be flatten square matrix of order {}. Got: {}".format(len(args.tiers), args.eviction_matrix)

    unflattened_admission_matrix = []
    unflattened_eviction_matrix = []
    for i in range(len(args.tiers)):
        unflattened_admission_matrix.append(args.admission_matrix[i * len(args.tiers):(i + 1) * len(args.tiers)])
        unflattened_eviction_matrix.append(args.eviction_matrix[i * len(args.tiers):(i + 1) * len(args.tiers)])

    assert len(args.admission_evaluations) % 2 == 0, \
        "admission_evaluations must contain even number of parameters. Got: {}".format(len(args.admission_evaluations))
    assert len(args.eviction_evaluations) % 2 == 0, \
        "admission_evaluations must contain even number of parameters. Got: {}".format(len(args.eviction_evaluations))

    for i in range(0, len(args.admission_evaluations), 2):
        assert args.admission_evaluations[i] in args.tiers, \
            "Unexpected tier name encountered: {} Expected one of: {}".format(args.admission_evaluations[i], args.tiers)
        assert args.admission_evaluations[i + 1].isdigit() and int(args.admission_evaluations[i + 1]) > 0, \
            "Unexpected number of admission evaluations encountered: {} Expected positive integer.".format(args.admission_evaluations[i + 1])

        args.admission_evaluations[i + 1] = int(args.admission_evaluations[i + 1])

    for i in range(0, len(args.eviction_evaluations), 2):
        assert args.eviction_evaluations[i] in args.tiers, \
            "Unexpected tier name encountered: {} Expected one of: {}".format(args.eviction_evaluations[i], args.tiers)
        assert args.eviction_evaluations[i + 1].isdigit() and int(args.eviction_evaluations[i + 1]) > 0, \
            "Unexpected number of eviction evaluations encountered: {} Expected positive integer.".format(args.eviction_evaluations[i + 1])

        args.eviction_evaluations[i + 1] = int(args.eviction_evaluations[i + 1])

    # Instantiate the data migration policy
    bps = ProbabilityBasedDataMigrationPolicy({
        "tiers": args.tiers,
        "data_admission_matrix" : unflattened_admission_matrix,
        "data_eviction_matrix" : unflattened_eviction_matrix})

    # Start the data admission evaluation
    for i in range(0, len(args.admission_evaluations), 2):
        for j in range(args.admission_evaluations[i + 1]):
            print("admit,{},{}".format(args.admission_evaluations[i], bps.destination_on_admission_from(args.admission_evaluations[i])))

    # Start the data admission evaluation
    for i in range(0, len(args.eviction_evaluations), 2):
        for j in range(args.eviction_evaluations[i + 1]):
            print("evict,{},{}".format(args.eviction_evaluations[i], bps.destination_on_eviction_from(args.eviction_evaluations[i])))
