__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod

class AbstractDataAdmissionPolicy(ABC):
    """Abstract class for data admission policies."""

    @abstractmethod
    def __init__(self, storage_params=None, config_params=None):
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

class EagerDataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy whose decision is to always admit (promote)."""

    def __init__(self, storage_params=None, config_params=None):
        pass

    def record_access(self, timestamp, pageID, type=None):
        pass

    def should_admit(self, pageID):
        return True

    def __str__(self):
        return "EagerDataAdmissionPolicy"

    def __repr__(self):
        return str(self)

class NeverDataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy whose decision is to never admit (promote)."""

    def __init__(self, storage_params=None, config_params=None):
        pass

    def record_access(self, timestamp, pageID, type=None):
        pass

    def should_admit(self, pageID):
        return False

    def __str__(self):
        return "NeverDataAdmissionPolicy"

    def __repr__(self):
        return str(self)

class Q2DataAdmissionPolicy(AbstractDataAdmissionPolicy):
    """Implementation of the AbstractDataAdmissionPolicy based on the 2Q algorithm."""

    def __init__(self, storage_params=None, config_params=None):
        # Initialize the "seen before" set pages
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

    def __str__(self):
        return "2QDataAdmissionPolicy - Q1 queue: {}".format(self.Q1)

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    # Testing Space
    """
    eager_dap = EagerDataAdmissionPolicy()
    eager_dap.record_access(0, 1)
    print(eager_dap)
    print(eager_dap.should_admit(1))
    """
    pass