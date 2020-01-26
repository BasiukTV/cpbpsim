__author__ = "Taras Basiuk"

from abc import ABC, abstractmethod
from bisect import bisect_left

class AbstractSLAPenaltyFunction(ABC):
    """Abstract class for SLA violation penalty functions."""

    @abstractmethod
    def __init__(self, slo_type, eval_period, mapping_func, logger):
        """Initialize the function with the given SLO type, evaluation period and mapping function."""
        pass

    @abstractmethod
    def record_SLO(self, timestamp, slo_val):
        """Record the SLO satisfaction level during given timestamp."""
        pass

    @abstractmethod
    def eval_penalty(self, from_time):
        """Evaluate the SLA violation penalty corresponding to recorded SLO values starting form given time."""
        pass

class AveragingPiecewiseLinearSLAPenaltyFunction(AbstractSLAPenaltyFunction):
    """Implementation of the AbstractSLAPenaltyFunction based on the piecewise linear mapping function."""

    def __init__(self, slo_type, eval_period, mapping_func, logger):
        """
            Constructor whose mapping function has baseline_slope and baseline_intercept float values
            which are used for the range from minus infinity to the first (smallest) given interval starting point.

            Also mapping function has a dictionary of intervals, where keys are float interval starting points,
            and values are pairs of linear slopes and intercepts to be used for the corresponding interval.

            Finally, SLO type string and evaluation period integer are expected.
        """

        # Validates the constructor arguments
        assert isinstance(slo_type, str), "slo_type must be a string. Got: {}".format(slo_type)
        assert isinstance(eval_period, int), "eval_period must be an integer. Got: {}".format(eval_period)
        assert isinstance(mapping_func, dict), "mapping_func must be a dictionary. Got: {}".format(mapping_func)

        # Validate the mapping_func contents
        assert "intervals" in mapping_func, "mapping function dictionary is expected to contain 'intervals'"
        intervals = mapping_func["intervals"]
        assert isinstance(intervals, dict), "intervals must be a dictionary. Got: {}".format(intervals)
        assert all(list(map(lambda a: isinstance(a, float), list(intervals.keys())))), \
            "intervals keys must all be float numbers. Got: {}".format(list(intervals.keys()))
        assert all(list(map(lambda a: isinstance(a, tuple) and isinstance(a[0], float) and isinstance(a[1], float), list(intervals.values())))), \
            "intervals values must all be pairs of float numbers. Got: {}".format(list(intervals.values()))

        assert "baseline_slope" in mapping_func, "mapping function dictionary is expected to contain 'baseline_slope'"
        baseline_slope = mapping_func["baseline_slope"]
        assert isinstance(baseline_slope, float), "baseline_slope must be a float. Got: {}".format(baseline_slope)

        assert "baseline_intercept" in mapping_func, "mapping function dictionary is expected to contain 'baseline_intercept'"
        baseline_intercept = mapping_func["baseline_intercept"]
        assert isinstance(baseline_intercept, float), "baseline_intercept must be a float. Got: {}".format(baseline_intercept)

        # Stores the constructor arguments and prepares a sorted list of interval starting points
        self.slo_type = slo_type
        self.eval_period = eval_period
        self.intervals = intervals
        self.starting_points = sorted(list(intervals.keys()))
        self.baseline_slope = baseline_slope
        self.baseline_intercept = baseline_intercept
        self.logger = logger

        # Prepare a list of SLO recording timestamps and a dictionary of corresponding SLO values
        self.slo_record_timestamps = []
        self.slo_recordings = {}

    def __str__(self):
        return "AdditivePiecewiseLinearSLAPenaltyFunction(slo_type={}, eval_period={}, base_slope={}, base_intercept={}, intervals={}, slo_recordings={})".format(
            self.slo_type, self.eval_period, self.baseline_slope, self.baseline_intercept, self.intervals, self.slo_recordings)

    def __repr__(self):
        return str(self)

    def record_SLO(self, timestamp, slo_val):
        """Record the SLO satisfaction level during given timestamp."""
        self.slo_record_timestamps.append(timestamp)
        self.slo_recordings[timestamp] = slo_val

    def eval_penalty(self, from_time):
        """
            Evaluates the penalty corresponding to the recorded SLO values from a given timestamp.

            Recoded SLO values are added withing the evaluation period.
            Summed value of the SLO parameter is mapped to the SLA penalty
            by finding the corresponding interval and evaluating it there or using the
            baseline slope and intercept if the value is smaller then the first interval starting point.

            Penalty values are then averaged up and returned.
        """
        sla_penalties = [0] # Initialize SLA penalties with a 0

        slo_avg = [] # SLO parameter average accumulated during the current evaluation period
        slo_avgs = [] # SLO avgs accumulated during all evaluation periods
        current_eval_period = from_time # Starting time-stamp of the current evaluation period

        # Find a spot from where to inspect the SLO records
        i = bisect_left(self.slo_record_timestamps, from_time)
        # Iterate through the remaining SLO recordings
        while i < len(self.slo_record_timestamps):
            # If next time-stamp belongs to the new evaluation period, wrap up the current one
            if current_eval_period + self.eval_period <= self.slo_record_timestamps[i]:
                slo_avgs.append(sum(slo_avg) / len(slo_avg) if slo_avg else 0)
                slo_avg = []
                current_eval_period = from_time + (self.eval_period * ((self.slo_record_timestamps[i] - from_time) // self.eval_period))

            slo_avg.append(self.slo_recordings[self.slo_record_timestamps[i]]) # Add to the already accumulated SLO value
            i += 1

        # Average out the left-overs
        slo_avgs.append(sum(slo_avg) / len(slo_avg) if slo_avg else 0)

        sla_penalties = [] # List holding SLA penalties for SLO values during the evaluation periods
        for slo_avg in slo_avgs:
            #Find a piecewise-linear interval of the mapping function on which the slo_avg should be evaluated
            i = bisect_left(self.starting_points, slo_avg)
            penalty = (
                # Evaluate on the baseline if i == 0, else evaluate on the interval
                self.baseline_slope * slo_avg) + self.baseline_intercept if i == 0 \
                    else (self.intervals[self.starting_points[i - 1]][0] * slo_avg) + self.intervals[self.starting_points[i - 1]][1]

            sla_penalties.append(penalty)

        # Sort averaged out SLO costs during the evaluation period, and log the percentiles
        slo_avgs = sorted(slo_avgs)
        percentiles = {}
        for p in range(0, 100, 1):
            percentiles["p{}".format(p)] = slo_avgs[int((p * len(slo_avgs)) / 100)]
        percentiles["p100"] = slo_avgs[-1]
        self.logger.info("Averaged SLO costs during an evaluation period percentiles: {}".format(percentiles))

        # Return the total SLA penalties accumulated since the from_time
        return sum(sla_penalties)

if __name__ == "__main__":
    # If executed, the file will evaluate the given penalty function on a given range of SLO parameter values

    # Default values
    DEFAULT_SLO_TYPE = "latency"
    DEFAULT_EVAL_PERIOD = 100 # 100 ms
    DEFAULT_BASELINE_SLOPE = 0.0
    DEFAULT_BASELINE_INTERCEPT = 0.0

    # Parse given arguments
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''This tool outputs a list of evaluations in given range for a given piecewise linear SLA violation penalty function.''')

    parser.add_argument('-T', '--slo-type', type=str, default=DEFAULT_SLO_TYPE,
        help='SLO type. Default: {}'.format(DEFAULT_SLO_TYPE))
    parser.add_argument('-P', '--eval-period', type=int, default=DEFAULT_EVAL_PERIOD,
        help='SLA evaluation period. Default: {}'.format(DEFAULT_EVAL_PERIOD))
    parser.add_argument('-B', '--baseline', type=float, nargs=2, default=[DEFAULT_BASELINE_SLOPE, DEFAULT_BASELINE_INTERCEPT],
        help='Baseline SLA penalty function slope and intercept. Default: {} {}'.format(DEFAULT_BASELINE_SLOPE, DEFAULT_BASELINE_INTERCEPT))
    parser.add_argument('-I', '--intervals', type=float, nargs='+', default=[],
        help='SLA penalty function intervals: [start_1, slope_1, intercept_1, start_2, slope_2, intercept_2, ...]. Default: None')
    parser.add_argument('-R', '--slo-val-records', type=float, nargs='+', default=[],
        help='SLO value records: [timestamp_1, value_1, timestamp_2, value_2, ...]. Default: None')
    args = parser.parse_args()

    # Validate the given parameters
    assert len(args.intervals) % 3 == 0, "Number of arguments to define intervals should be divisible by 3. Got: {}".format(len(args.intervals))
    assert len(args.intervals) % 2 == 0, "Number of arguments to define SLO value records should be divisible by 2. Got: {}".format(len(args.intervals))

    # Prepare the intervals dictionary
    intervals = {}
    for i in range(0, len(args.intervals), 3):
        intervals[args.intervals[i]] = (args.intervals[i + 1], args.intervals[i + 2])

    # Instantiate the function
    sla = AveragingPiecewiseLinearSLAPenaltyFunction(args.slo_type, args.eval_period,
        {"intervals" : intervals, "baseline_slope" : args.baseline[0], "baseline_intercept" : args.baseline[1]})

    # Evaluate the SLA on the sequence of SLO value records
    for i in range(0, len(args.slo_val_records), 2):
        sla.record_SLO(args.slo_val_records[i], args.slo_val_records[i + 1])

    # Return the result
    print(sla.eval_penalty(0))
