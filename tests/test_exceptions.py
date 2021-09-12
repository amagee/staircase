import operator

import pytest

from staircase import Stairs
from staircase.core.ops.common import DifferentClosedValuesError


def s1(closed="left"):
    int_seq1 = Stairs(initial_value=0, closed=closed)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


@pytest.mark.parametrize(
    ("left", "right", "ok"),
    [
        (Stairs(start=0, closed="left"), 1, True),
        (Stairs(start=0, closed="right"), 1, True),
        (1, Stairs(start=0, closed="left"), True),
        (1, Stairs(start=0, closed="right"), True),
        (Stairs(closed="left"), 1, True),
        (Stairs(closed="right"), 1, True),
        (1, Stairs(closed="left"), True),
        (1, Stairs(closed="right"), True),
        (s1(closed="left"), s1(closed="right"), False),
        (s1(closed="right"), s1(closed="left"), False),
    ],
)
@pytest.mark.parametrize(
    "op",
    [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
        operator.eq,
        operator.ne,
        operator.lt,
        operator.gt,
        operator.le,
        operator.ge,
        operator.and_,
        operator.or_,
        operator.xor,
    ],
)
def test_binary_operation_closed_matching(left, right, op, ok):
    """
    A binary operation should throw a a `DifferentClosedValuesError` if:

    1. Both arguments are `Stairs` objects, and
    2. The arguments have different `closed` values, and
    3. Both arguments have a nonzero number of steps.

    For all our defined operations, test that the exception is thrown under the
    above conditions but not if the arguments are ok.
    """
    if ok:
        op(left, right)
    else:
        with pytest.raises(DifferentClosedValuesError):
            op(left, right)
