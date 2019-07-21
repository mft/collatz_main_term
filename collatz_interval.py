"""
"Collatz" main term conjecture

Let f(x) = x - (-1)^{ceil(x)} * x/2,
then for any positive number t there exists k such that f^k(t) in (0, 1].

This program tests given interval whether it satisfies the conjecture or not.
"""

import fractions
import math
from intervals.interval import (
    coerce_interval,
    AbstractInterval,
)

class FractionInterval(AbstractInterval):
    type = fractions.Fraction

    @coerce_interval
    def __mul__(self, other):
        end_points_candidates = [
            self.lower * other.lower, self.lower * other.upper,
            self.upper * other.lower, self.upper * other.upper
        ]
        bounds = [min(end_points_candidates), max(end_points_candidates)]

        if bounds[0] == bounds[1]:
            if self.is_closed and other.is_closed:
                return type(self).closed(*bounds)
            # empty
            return type(self).open_closed(*bounds)

        inc_candidates = [
            self.lower_inc and other.lower_inc,
            self.lower_inc and other.upper_inc,
            self.upper_inc and other.lower_inc,
            self.upper_inc and other.upper_inc
        ]
        lower_inc = True
        upper_inc = True
        for bound, inc in zip(end_points_candidates, inc_candidates):
            if bound == bounds[0]:
                lower_inc = lower_inc and inc
            if bound == bounds[1]:
                upper_inc = upper_inc and inc

        return type(self)(
            bounds,
            lower_inc=lower_inc,
            upper_inc=upper_inc
        )

    def is_contained_in(self, other):
        """
        tell whether the interval is contained in the other
        """
        return ((
            self.lower == other.lower and (not self.lower_inc or other.lower_inc) or
            self.lower > other.lower
        ) and (
            self.upper == other.upper and (not self.upper_inc or other.upper_inc) or
            self.upper < other.upper
        ))


def prove_interval(interval, verbose=0):
    """
    for open-closed fraction interval, prove Collatz main term conjecture.

    if verbose, print every step,
    if verbose is more than 2, print every sub steps,
    """
    proven = FractionInterval.open_closed(0, 1)
    unproven = break_at_integer(interval)
    if verbose:
        i = 0
        print(i, unproven)
    while unproven:
        applied_intervals = [the_function(interval) for interval in unproven]
        if verbose > 1:
            print("applied", applied_intervals)
        broken_intervals = []
        for interval in applied_intervals:
            broken_intervals.extend(break_at_integer(interval))
        if verbose > 1:
            print("broken", broken_intervals)
        merged_intervals = []
        used = False
        for interval0, interval1 in zip(broken_intervals, broken_intervals[1:]):
            if used:
                used = False
                continue
            if interval0.upper == interval1.lower and interval1.lower.denominator != 1:
                merged_intervals.append(interval0 | interval1)
                used = True
            else:
                merged_intervals.append(interval0)
        if not used:
            merged_intervals.append(broken_intervals[-1])
        if verbose > 1:
            print("merged", merged_intervals)
        unproven = [interval for interval in merged_intervals if not interval.is_contained_in(proven)]
        if verbose:
            i += 1
            print(i, unproven)

    return True


def the_function(interval):
    """
    apply the Collats main term function on interval

    the given interval has to be broken at integer.
    assuming the given interval is open-closed.
    """
    if math.ceil(interval.upper) % 2:
        return interval * type(interval).closed(
            fractions.Fraction(3, 2),
            fractions.Fraction(3, 2)
        )
    else:
        return interval * type(interval).closed(
            fractions.Fraction(1, 2),
            fractions.Fraction(1, 2)
        )


def break_at_integer(interval):
    """
    break the given open-closed fraction interval at every integer
    """
    unproven = []
    lower_ceil = math.ceil(interval.lower) if interval.lower < math.ceil(interval.lower) else interval.lower + 1
    while lower_ceil != math.ceil(interval.upper):
        unproven.append(
            FractionInterval.open_closed(interval.lower, lower_ceil)
        )
        interval = FractionInterval.open_closed(lower_ceil, interval.upper)
        lower_ceil += 1
    if interval:
        unproven.append(interval)

    return unproven

            
