"""Test codes for environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com
"""

import pytest

from env import ElevatorEnv


class TestElevatorEnvClass:
    def setup_method(self) -> None:
        self.lowest_floor = -10
        self.highest_floor = 10
        self.env = ElevatorEnv(floor_range=(self.lowest_floor, self.highest_floor))

    def test_make_valid_floors(self) -> None:
        """Check the env has valid floor information."""

        assert len(self.env.floors) == 20
        assert max(self.env.floors) == self.highest_floor
        assert min(self.env.floors) == self.lowest_floor
        assert 0 not in self.env.floors
