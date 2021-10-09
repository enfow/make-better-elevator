"""Test codes for environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com
"""

import pytest

from env import ElevatorEnv, Passenger


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

    def test_initial_passangers(self) -> None:
        """Check the env has correct info about the passangers at init time."""
        for floor in self.env.floors:
            assert floor in self.env.floor_to_passengers
            assert floor in self.env.floor_to_people
            assert self.env.floor_to_passengers[floor] == 0
            assert self.env.floor_to_people[floor] == 0


class TestPassenger:
    def test_passenger(self) -> None:
        passenger = Passenger(target=10)
        assert passenger.target == 10
        
