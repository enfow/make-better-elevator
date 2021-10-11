"""Test codes for environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com
"""

import pytest

from env import BASE_FLOOR, Elevator, ElevatorEnv, Passenger


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
            if floor == BASE_FLOOR:
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
        assert self.env.floor_to_people[BASE_FLOOR] == self.env.max_people - 1
        # add passenger to base floor (direction of the new passenger is random)
        assert (
            len(self.env.floor_to_passengers[BASE_FLOOR][1])
            + len(self.env.floor_to_passengers[BASE_FLOOR][-1])
            == 1
        )


class TestElevator:
    def setup_method(self) -> None:
        self.floors = [-3, -2, -1, 1, 2, 3, 4, 5]
        self.elevator = Elevator(self.floors)

    def test_init_elevator(self) -> None:
        """Check the elevlator's Initialization."""
        for floor in self.floors:
            assert len(self.elevator.target_to_passengers[floor]) == 0
        assert 0 not in self.elevator.target_to_passengers
        self.elevator.current_floor == BASE_FLOOR
        self.elevator.target_floor== BASE_FLOOR
        self.elevator.velocity == 0.

    ##############################################################
    #   Test Codes for Elevator.update_current_state() method    #
    #   - when it goes up from first floor to fourth floor       #
    #     =>  1. -> 1.5 -> 2.5 -> 3.5 -> 4.                      #
    #   - when it goes down from fourth floor to first floor     #
    #     =>  4. -> 3.5 -> 2.5 -> 1.5 -> 1.                      #
    ##############################################################

    def test_update_current_state_with_velocity_pos1(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 1.
        self.elevator.target_floor = 4.
        self.elevator.velocity = 1.

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 2.  # add 1
        assert self.elevator.target_floor == 4.  # same
        assert self.elevator.velocity == 1.  # same

    def test_update_current_state_with_velocity_neg1(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 4.
        self.elevator.target_floor = 1.
        self.elevator.velocity = -1.

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 3.  # subtract -1
        assert self.elevator.target_floor == 1.  # same
        assert self.elevator.velocity == -1.  # same

    def test_update_current_state_with_velocity_pos05(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 1.
        self.elevator.target_floor = 4.
        self.elevator.velocity = 0.5

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 2.  # add 1  (velocity 0.5 -> 1)
        assert self.elevator.target_floor == 4.  # same
        assert self.elevator.velocity == 1.  # same

    def test_update_current_state_with_velocity_neg05(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 4.
        self.elevator.target_floor = 1.
        self.elevator.velocity = -0.5

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 3.  # subtract -1  (velocity -0.5 -> -1.)
        assert self.elevator.target_floor == 1.  # same
        assert self.elevator.velocity == -1.  # same

    def test_update_current_state_with_velocity_0_go_up(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 1.
        self.elevator.target_floor = 4.
        self.elevator.velocity = 0.

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 1.5  # add 0.5
        assert self.elevator.target_floor == 4.  # same
        assert self.elevator.velocity == 0.5  # same

    def test_update_current_state_with_velocity_0_go_down(self) -> None:
        """Check the location and velocity logic."""
        self.elevator.current_floor = 4.
        self.elevator.target_floor = 1.
        self.elevator.velocity = 0.

        self.elevator.update_current_state()
        
        assert self.elevator.current_floor == 3.5  # subtract 0.5
        assert self.elevator.target_floor == 1.  # same
        assert self.elevator.velocity == -0.5  # same

    def test_get_on_and_off_method(self) -> None:
        """Check the situation of passengers getting on the elevator."""
        n_passengers = 3
        current_floor, target_floor = 1, 3
        # create passengers getting on the elevator on the first floor
        passengers = [
            Passenger(begin_floor=current_floor, floors=self.floors)
            for _ in range(n_passengers)
        ]
        # set all passengers target floor as 3
        for passenger in passengers:
            passenger.target_floor = target_floor
        # get on the elevator
        self.elevator.get_on_elevator(passengers)
        assert len(self.elevator.target_to_passengers[target_floor]) == 3
        # move the elevator to target floor
        self.elevator.current_floor = target_floor
        # get off the elevator
        num_passengers_getting_off = self.elevator.get_off_elevator()
        assert len(self.elevator.target_to_passengers[target_floor]) == 0
        assert num_passengers_getting_off == n_passengers


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
