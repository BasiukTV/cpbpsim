__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod

class AbstractDataAdmissionPolicy(ABC):
    """Abstract class for data admission policies."""

    @abstractmethod
    def __init__(self, storage_params=None, config_params=None, init_from_file=None):
        """Initialize the policy with the given storage tier parameters and policy config parameters."""
        pass

    @abstractmethod
    def record_access(self, timestamp, pageID, type):
        """Allow the policy to record the pageID access to justify the future admission decisions."""
        pass

    @abstractmethod
    def should_admit(self, pageID):
        """Returns a decision on whether to admit (promote) given pageID to a different (higher) storage layer."""
        pass

    @abstractmethod
    def persist_to_file(self, file_name):
        """Persists the state of the policy to a file, from which it can be later recovered."""
        pass

class EagerDataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy whose decision is to always admit (promote)."""

    def __init__(self, storage_params=None, config_params=None, init_from_file=None):
        pass

    def record_access(self, timestamp, pageID, type=None):
        pass

    def should_admit(self, pageID):
        return True

    def persist_to_file(self, file_name):
        # Just create/open a file, but don't actually write anything to it
        with open(file_name, 'w') as f:
            pass

    def __str__(self):
        return "EagerDataAdmissionPolicy"

    def __repr__(self):
        return str(self)

class NeverDataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy whose decision is to never admit (promote)."""

    def __init__(self, storage_params=None, config_params=None, init_from_file=None):
        pass

    def record_access(self, timestamp, pageID, type=None):
        pass

    def should_admit(self, pageID):
        return False

    def persist_to_file(self, file_name):
        # Just create/open a file, but don't actually write anything to it
        with open(file_name, 'w') as f:
            pass

    def __str__(self):
        return "NeverDataAdmissionPolicy"

    def __repr__(self):
        return str(self)

class Q2DataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy based on the 2Q algorithm."""

    def __init__(self, storage_params=None, config_params=None, init_from_file=None):

        if init_from_file:
            # If the file is given, populate the "seen before" set with page IDs in it
            import json
            with open(init_from_file) as f:
                self.Q1 = set(json.load(f))
        else:
            # Initialize the "seen before" set pages as an empty set
            self.Q1 = set()

    def record_access(self, timestamp, pageID, type):
        # Add the page to the "seen before" set
        self.Q1.add(pageID)

    def should_admit(self, pageID):
        # If the page was seen before, it should be admitted(promoted)
        if pageID in self.Q1:
            self.Q1.remove(pageID) # reset the seen before set
            return True

        # Page was not seen before, should not be admitted
        return False

    def persist_to_file(self, file_name):
        """Simply saves the contents of 'seen before' set into the given file in JSON array format. """

        import json
        with open(file_name, 'w') as f:
            json.dump(list(self.Q1), f)

    def __str__(self):
        return "2QDataAdmissionPolicy - Q1 queue: {}".format(self.Q1)

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    # Testing Space
    """
    Q2_dap = Q2DataAdmissionPolicy()
    Q2_dap.record_access(0, 1, "read")
    print(Q2_dap)
    print(Q2_dap.should_admit(1))
    Q2_dap.record_access(1, 2, "read")
    Q2_dap.record_access(2, 3, "update")
    Q2_dap.persist_to_file("test.json")
    Q2_dap = Q2DataAdmissionPolicy(init_from_file="test.json")
    print(Q2_dap.should_admit(1))
    print(Q2_dap)
    """
    pass
