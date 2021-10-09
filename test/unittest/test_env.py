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
            assert floor in self.env.floor_to_people
            if floor == self.env.base_floor:
                assert self.env.floor_to_people[floor] == self.env.max_people
            else:
                assert self.env.floor_to_people[floor] == 0

        for floor in self.env.floors:
            assert floor in self.env.floor_to_passengers
            assert len(self.env.floor_to_passengers[floor][-1]) == 0
            assert len(self.env.floor_to_passengers[floor][1]) == 0


class TestPassenger:
    def test_passenger(self) -> None:
        passenger = Passenger(target=10)
        assert passenger.target == 10

    def test_get_direction_method(self) -> None:
        # from 1 to 10 -> Going Up
        passenger = Passenger(target=10)
        current_floor = 1
        assert passenger.get_direction(current_floor) == 1
        # from 10 to 1 -> Going Down
        passenger = Passenger(target=1)
        current_floor = 10
        assert passenger.get_direction(current_floor) == -1
        # from 1 to 1 -> Raise RuntimeError
        passenger = Passenger(target=1)
        current_floor = 1
        with pytest.raises(RuntimeError):
            passenger.get_direction(current_floor)
