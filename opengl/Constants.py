import numpy as np

UP: np.ndarray = np.array((0.0, 1.0))
"""One unit step in the positive Y direction."""

DOWN: np.ndarray = np.array((0.0, -1.0))
"""One unit step in the negative Y direction."""

RIGHT: np.ndarray = np.array((1.0, 0.0))
"""One unit step in the positive X direction."""

LEFT: np.ndarray = np.array((-1.0, 0.0))

ZERO: np.ndarray = np.array((0.0, 0.0))


ABOVE = 1
BELOW = 2
TO_THE_LEFT = 3
TO_THE_RIGHT = 4
TO_THE_CENTER = 5


UP: np.ndarray = np.array((0.0, 1.0))
"""One unit step in the positive Y direction."""

DOWN: np.ndarray = np.array((0.0, -1.0))
"""One unit step in the negative Y direction."""

RIGHT: np.ndarray = np.array((1.0, 0.0))
"""One unit step in the positive X direction."""

LEFT: np.ndarray = np.array((-1.0, 0.0))


LEFT_ARROW = 80
RIGHT_ARROW = 79
UP_ARROW = 82
DOWN_ARROW = 81