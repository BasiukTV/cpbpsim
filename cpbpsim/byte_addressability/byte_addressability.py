__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod

class AbstraByteAddressabilityPolicy(ABC):
    """
        This abstract class handles utilization of byte addressability properties of different storage tiers
        during data migration.
    """

    @abstractmethod
    def __init__(self, config_params=None, init_from_file=None):
        """Initialize the policy with the given policy config parameters or from a given file."""
        pass

    @abstractmethod
    def handle_migration(self, source, dest, pageID, tupleIDs, type):
        """Returns a destination storage tier of the data page when it's admitted from source storage tier."""
        pass

    @abstractmethod
    def persist_to_file(self, file_name):
        """Persists the state of the byte-addressability module to a file, from which it can be later recovered."""
        pass

class NoByteAddressabilityPolicy(AbstraByteAddressabilityPolicy):
    """
        This policy doesn't actually utilizes the byte addressability of the storage tiers and just performs the migration of entire pages.
    """

    def __init__(self, config_params=None, init_from_file=None):
        """Initialize the policy with the given policy config parameters or from a given file."""
        pass

    def handle_migration(self, source, dest, pageID, tupleIDs, type):
        """Returns a destination storage tier of the data page when it's admitted from source storage tier."""
        pass

    def persist_to_file(self, file_name):
        # Just create/open a file, but don't actually write anything to it.
        with open(file_name, 'w') as f:
            pass
