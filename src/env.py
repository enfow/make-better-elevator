"""Elevator Environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com

References:
    - gym.Env: https://github.com/openai/gym/blob/master/gym/core.py
"""

from typing import List, Tuple

import gym


class ElevatorEnv(gym.Env):
    """Elevator gym environment."""

    def __init__(
        self,
        floor_range: Tuple[int, int],
    ) -> None:

        self.base_floor = 1
        self.floors: List[int] = [
            i for i in range(floor_range[0], floor_range[1] + 1, 1) if i != 0
        ]

    def step(self, action) -> None:
        pass

    def reset(self) -> None:
        pass

    def render(self, mode="human") -> None:
        pass
