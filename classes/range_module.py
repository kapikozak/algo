import bisect
from itertools import chain

class RangeModule:

    def __init__(self):
        self.intervals = []

    def add_range(self, left: int, right: int) -> None:
        lo = bisect.bisect_left(self.intervals, left, key=lambda x: x[1])
        hi = bisect.bisect_right(self.intervals, right, key=lambda x: x[0]) - 1

        if lo != len(self.intervals):
            left = min(self.intervals[lo][0], left)

        if hi != -1:
            right = max(self.intervals[hi][1], right)

        self.intervals = list(chain(
            self.intervals[:lo],
            [[left, right]],
            self.intervals[hi + 1:]
        ))

    def query_range(self, left: int, right: int) -> bool:
        ip = bisect.bisect_right(self.intervals, left, key=lambda x: x[0]) - 1
        return not (ip == -1 or right > self.intervals[ip][1])

    def remove_range(self, left: int, right: int) -> None:
        lo = bisect.bisect_right(self.intervals, left, key=lambda x: x[1])
        hi = bisect.bisect_left(self.intervals, right, key=lambda x: x[0]) - 1

        if lo > hi:
            return

        self.intervals = list(chain(
            self.intervals[:lo],
            [[self.intervals[lo][0], left]] if left > self.intervals[lo][0] else [],
            [[right, self.intervals[hi][1]]] if self.intervals[hi][1] > right else [],
            self.intervals[hi + 1:]
        ))
