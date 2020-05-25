__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod
from collections import deque
from heapq import heappush, heappop

class AbstractDataEvictionPolicy(ABC):
    """Abstract class for data eviction policies."""

    @abstractmethod
    def __init__(self, storage_params=None, config_params=None, init_from_file=None):
        """Initialize the policy with the given storage tier parameters and policy config parameters."""
        pass

    @abstractmethod
    def record_access(self, timestamp, pageID, resident, type=None):
        """Allow the policy to record the pageID access of a given type to justify the future eviction decisions."""
        pass

    @abstractmethod
    def evict(self):
        """Returns pageID to evict from a current storage tier to a different tier."""
        pass

    @abstractmethod
    def update_residency(self, pageID, resident):
        """Updates the pageID residency with this policy."""
        pass

    @abstractmethod
    def persist_to_file(self, file_name):
        """Persists the state of the policy to a file, from which it can be later recovered."""
        pass

class LRUEvictionPolicy(AbstractDataEvictionPolicy):
    """Implementation of the AbstractDataEvictionPolicy which uses an LRU algorithm."""

    def __init__(self, storage_params=None, config_params=None, init_from_file=None):

        if init_from_file:
            raise NotImplementedError

        # Priority queue (heap queue) which will make it easy to find least recently referenced page
        self.priority_queue = []

        # Because updating the priority queues items is hard will keep the dictionary to track their true last reference
        self.last_page_reference = {}

        # Keep track of the pages actually resident with this policy (subject to eviction)
        self.page_residency = set()

    def record_access(self, timestamp, pageID, resident, type=None):
        """Allow the policy to record the pageID access to justify the future eviction decisions."""

        # If pageID is not yet resident, but should be, add it to the priority queue
        if resident and pageID not in self.page_residency:
            heappush(self.priority_queue, (timestamp, pageID))
            self.page_residency.add(pageID)

        # Add/Update latest page reference
        self.last_page_reference[pageID] = timestamp

    def evict(self):
        """Returns pageID to evict from a corresponding storage tier to a different storage tier."""

        # Get a first pageID eviction candidate per priority queue
        candidate_timestamp, candidate_pageID = heappop(self.priority_queue)

        # It's possible that candidate's last reference timestamp was updated while it was in the queue
        # or the page lost residency with the policy
        while candidate_timestamp != self.last_page_reference[candidate_pageID] or candidate_pageID not in self.page_residency:

            # If the page is resident but outdated, re-enqueue the candidate with the updated timestamp
            if candidate_pageID in self.page_residency:
                heappush(self.priority_queue, (self.last_page_reference[candidate_pageID], candidate_pageID))

            # Get a new candidate
            candidate_timestamp, candidate_pageID = heappop(self.priority_queue)

        # Remove the corresponding page_residency entry
        self.page_residency.remove(candidate_pageID)

        # return the victim page ID
        return candidate_pageID

    def update_residency(self, pageID, resident):
        # If the page is not yet a resident, add add it the priority queue
        if pageID not in self.page_residency and resident:
            heappush(self.priority_queue, (self.last_page_reference[pageID], pageID))
            self.page_residency.add(pageID)
        # If the page is already a resident remove it from residency
        elif pageID in self.page_residency and not resident:
            self.page_residency.add(pageID)

    def persist_to_file(self, file_name):
        raise NotImplementedError

    def __str__(self):
        return "LRU-EvictionPolicy - Priority Queue: {}, Last Page Reference: {}, Page Residency: {}".format(
            self.priority_queue, self.last_page_reference, self.page_residency)

    def __repr__(self):
        return str(self)

class FIFODataEvictionPolicy(AbstractDataEvictionPolicy):
    """Implementation of the AbstractDataEvictionPolicy which uses a FIFO algorithm."""

    def __init__(self, storage_params=None, config_params=None, init_from_file=None):

        if init_from_file:
            raise NotImplementedError

        # FIFO queue determining the order of page evictions
        self.fifo_queue = deque()

        # Keep track of the pages actually resident with this policy (subject to eviction)
        self.page_residency = set()

    def record_access(self, timestamp, pageID, resident, type=None):
        # If the page is not in the FIFO queue yet, add it
        if resident and pageID not in self.page_residency:
            self.fifo_queue.append(pageID)
            self.page_residency.add(pageID)

    def evict(self):
        # Pop a victim pageID from the FIFO queue, update page_residency set and return the victim
        victim_pageID = self.fifo_queue.popleft()

        # If the page is not resident anymore, get a new victim
        while victim_pageID not in self.page_residency:
            victim_pageID = self.fifo_queue.popleft()

        # Remove the page residency
        self.page_residency.remove(victim_pageID)

        return victim_pageID

    def update_residency(self, pageID, resident):
        # If the page not yet resident, add the page the FIFO queue
        if resident and pageID not in self.page_residency:
            self.fifo_queue.append(pageID)
            self.page_residency.add(pageID)
        # If the page is resident but should not be, update the residency set
        elif not resident and pageID in self.page_residency:
            self.page_residency.remove(pageID)

    def persist_to_file(self, file_name):
        raise NotImplementedError

    def __str__(self):
        return "FIFO-EvictionPolicy - FIFO Queue: {}, Page Residency: {}".format(self.fifo_queue, self.page_residency)

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    # Testing Space
    """
    lru_dep = LRUEvictionPolicy()
    lru_dep.record_access(0, 1)
    lru_dep.record_access(10, 2)
    lru_dep.record_access(20, 3)
    lru_dep.record_access(30, 2)
    print(lru_dep)
    print(lru_dep.evict(), lru_dep.evict(), lru_dep.evict())
    """
    pass
