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

    def test_generate_passenger_method(self) -> None:
        """Check the env generate valid passenger."""
        self.env.generate_passenger()
        # reduce people (all poeple are located on the base floor at init.)
        assert self.env.floor_to_people[self.env.base_floor] == self.env.max_people - 1
        # add passenger to base floor (direction of the new passenger is random)
        assert (
            len(self.env.floor_to_passengers[self.env.base_floor][1])
            + len(self.env.floor_to_passengers[self.env.base_floor][-1])
            == 1
        )


class TestPassenger:
    def setup_class(self) -> None:
        self.floors = [-1, 1, 2, 3]

    def test_init_passenger(self) -> None:
        """Check Passenger's initialization."""
        passenger = Passenger(begin_floor=1, floors=self.floors)
        assert passenger.begin_floor == 1

    def test_direction_property(self) -> None:
        """Check Passenger's direction property."""
        # from 1 to 10 -> Going Up
        passenger = Passenger(begin_floor=1, floors=self.floors)
        passenger.target_floor = 10
        assert passenger.direction == 1
        # from 10 to 1 -> Going Down
        passenger = Passenger(begin_floor=10, floors=self.floors)
        passenger.target_floor = 1
        assert passenger.direction == -1
        # from 1 to 1 -> Raise RuntimeError
        passenger = Passenger(begin_floor=1, floors=self.floors)
        passenger.target_floor = 1
        with pytest.raises(RuntimeError):
            passenger.direction
