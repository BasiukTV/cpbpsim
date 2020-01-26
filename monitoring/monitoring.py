__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod

class AbstractMetricsMonitor(ABC):
    """Abstract for monitoring the operation of the buffer pool simulator"""

    @abstractmethod
    def __init__(self, logger):
        """Initialize the monitor with the given logger."""
        pass

    @abstractmethod
    def record_metric(self, timestamp, tenant, page_tier, data_access_chain, slo_val):
        """Record the timestamp, tenant, page_tier, data_access_chain and slo_val related metrics."""
        pass

    @abstractmethod
    def log_aggregate_metrics(self, from_time):
        """Log the aggregated metrics compiled since from_time."""
        pass

class TenantMetricsMonitor(AbstractMetricsMonitor):
    """Implementation of AbstractMetricsMonitor which aggregates the metrics from the tenant perspective."""

    def __init__(self, logger):
        """Initialize the monitor with the given logger.."""

        self.logger = logger

        # Dictionaries for timestamped tenant metrics on page_tier, lengths of data_access_chain, and slo_val
        self.tier_metrics = {}
        self.data_access_chain_metrics = {}
        self.slo_val_metrics = {}

    def record_metric(self, timestamp, tenant, page_tier, data_access_chain, slo_val):
        """Record the timestamp, tenant, page_tier, data_access_chain and slo_val related metrics."""
        if tenant not in self.tier_metrics:
            self.tier_metrics[tenant] = {}
            self.data_access_chain_metrics[tenant] = {}
            self.slo_val_metrics[tenant] = {}

        self.tier_metrics[tenant][timestamp] = page_tier
        self.data_access_chain_metrics[tenant][timestamp] = len(data_access_chain)
        self.slo_val_metrics[tenant][timestamp] = slo_val

    def log_aggregate_metrics(self, from_time):
        # For every tenant
        for tenant in self.tier_metrics:
            # Calculate the probabilities of tenant page being found at different tiers
            total_count = 0
            tier_count = {}
            for timestamp in self.tier_metrics[tenant]:
                if timestamp < from_time:
                    continue

                total_count += 1
                tier = self.tier_metrics[tenant][timestamp]
                if tier not in tier_count:
                    tier_count[tier] = 1
                else:
                    tier_count[tier] = tier_count[tier] + 1

            # Convert tier counts into percentages
            for tier in tier_count:
                tier_count[tier] = tier_count[tier] / total_count

            self.logger.info("tenantID:{} page tier placement probabilities: {}".format(tenant, tier_count))

            # Calculate the percentiles and average of data_access_chain lengths resulting from a page access request
            chain_lengths = []
            for timestamp in self.data_access_chain_metrics[tenant]:
                if timestamp < from_time:
                    continue

                chain_lengths.append(self.data_access_chain_metrics[tenant][timestamp])
            chain_lengths = sorted(chain_lengths)

            self.logger.info("tenantID:{} average data access chain length: {}".format(tenant, sum(chain_lengths) / total_count))

            percentiles = {}
            for p in range(0, 100, 5):
                percentiles["p{}".format(p)] = chain_lengths[int((p * total_count) / 100)]
            percentiles["p100"] = chain_lengths[-1]
            self.logger.info("tenantID:{} data access chain length percentiles: {}".format(tenant, percentiles))

            # Calculate the percentiles and average of SLO cost values resulting from a page access request
            slo_values  = []
            for timestamp in self.slo_val_metrics[tenant]:
                if timestamp < from_time:
                    continue

                slo_values.append(self.slo_val_metrics[tenant][timestamp])
            slo_values = sorted(slo_values)

            self.logger.info("tenantID:{} average SLO cost: {}".format(tenant, sum(slo_values) / total_count))

            percentiles = {}
            for p in range(0, 100, 1):
                percentiles["p{}".format(p)] = slo_values[int((p * total_count) / 100)]
            percentiles["p100"] = slo_values[-1]
            self.logger.info("tenantID:{} data SLO cost percentiles: {}".format(tenant, percentiles))

    def __str__(self):
        return "TenantMetricsMonitor - Tier Metrics: {}, Data Access Chain Metrics: {}, SLO Value Metrics: {}".format(
            self.tier_metrics, self.data_access_chain_metrics, self.slo_val_metrics)

    def __repr__(self):
        return str(self)
