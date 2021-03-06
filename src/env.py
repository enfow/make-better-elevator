"""Elevator Environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com

References:
    - gym.Env: https://github.com/openai/gym/blob/master/gym/core.py
"""

import random
from typing import Dict, List, Set, Tuple

import gym
import numpy as np

Floor = float
Direction = int  # -1: go down, 1: go up
Velocity = float  # velocity of the elevator

BASE_FLOOR = 1


class ElevatorEnv(gym.Env):
    """Elevator gym environment."""

    def __init__(
        self,
        floor_range: Tuple[int, int],
        max_people: int = 100,
        num_elevator: int = 1,
    ) -> None:

        assert max_people >= 1
        assert num_elevator >= 1
        self.max_people = max_people
        self.num_elevator = num_elevator

        self.floors: List[Floor] = [
            i for i in range(floor_range[0], floor_range[1] + 1, 1) if i != 0
        ]
        # number of passegeners waiting for the elevator
        self.floor_to_passengers: Dict[Floor, Dict[Direction, Set["Passenger"]]] = {
            floor: self.get_empty_floor() for floor in self.floors
        }
        # number of people on each floor
        self.floor_to_people: Dict[Floor, int] = {floor: 0 for floor in self.floors}
        # init elevator
        self.elevators: List["Elevator"] = [
            Elevator(self.floors) for _ in range(self.num_elevator)
        ]

        self.reset()

    def step(self, action: np.ndarray) -> None:
        """step.
        Notes:
            - action: target floors for each elevator.
            - if the action is 0, then the target floor does not changed.
            - so the action space is "number of floors" + 1(for 0)
        """
        assert len(action) == self.num_elevator

        for idx, action_for_each_elevator in enumerate(action):
            self.elevators[idx].step(action_for_each_elevator)

    def reset(self) -> None:
        """reset the env.
        Notes:
            - the number of passanger is 0.
            - all of the elevators are located on the first floor.
        """
        # reset floor informations
        for floor in self.floors:
            self.floor_to_passengers[floor] = self.get_empty_floor()
            self.floor_to_people[floor] = 0
        self.floor_to_people[1] = self.max_people
        # reset elevators
        for elevator in self.elevators:
            elevator.reset()

    def render(self, mode="human") -> None:
        """render."""
        raise NotImplementedError

    def get_empty_floor(self) -> Dict[Direction, Set["Passenger"]]:
        """Get empty floor."""
        return {1: set(), -1: set()}

    def generate_passenger(self) -> None:
        """Generate new passenger."""
        not_empty_floors = set()
        for floor, people in self.floor_to_people.items():
            if people > 0:
                not_empty_floors.add(floor)
        current_floor = random.sample(not_empty_floors, k=1)[0]
        # reduce current floor's number of people
        self.floor_to_people[current_floor] -= 1
        # create and append new pessenger
        new_passenger = Passenger(begin_floor=current_floor, floors=self.floors)
        self.floor_to_passengers[current_floor][new_passenger.direction].add(
            new_passenger
        )


class Elevator:
    """Elevator."""

    def __init__(self, floors: List[Floor]) -> None:
        """Initialize."""
        self.floors = floors
        self.target_to_passengers: Dict[Floor, Set["Passenger"]] = {
            floor: set() for floor in self.floors
        }
        self.current_floor: Floor = BASE_FLOOR
        self.target_floor: Floor = BASE_FLOOR
        self.velocity: Velocity = 0.0

        self.reset()

        self.valid_velocity: Set[Velocity] = {-1.0, -0.5, 0.0, 0.5, 1.0}

    def reset(self) -> None:
        """Reset the elevator."""
        self.target_to_passengers = {floor: set() for floor in self.floors}
        self.current_floor = BASE_FLOOR
        self.target_floor = BASE_FLOOR
        self.velocity = 0.0

    def step(self, action: int) -> None:
        """Do the elevator thing."""
        if action != 0:
            self.target_floor = action
        self.update_current_state()

    def update_current_state(self) -> None:
        """Get the location and the movement of the elevator.

        Notes:
            - the speed of the elevator is 1 except the start and finish step(0.5).
            - e.g. the movement of the elevator when it go from 1 to 4:
                1 -> 1.5 -> 2.5 -> 3.5 -> 4
        """
        # when it should go up.
        if self.current_floor < self.target_floor:
            # when it is not max.
            if self.velocity != 1.0:
                self.velocity += 0.5
            self.current_floor += self.velocity
        # when it should go down
        elif self.current_floor > self.target_floor:
            # when it is not max.
            if self.velocity != -1.0:
                self.velocity -= 0.5
            self.current_floor += self.velocity
        # check validity
        if self.velocity not in self.valid_velocity:
            raise RuntimeError("Invalid velocity")

    def update_target_floor(self, new_target: Floor) -> None:
        """Update target floor.

        Notes:
            - To change the target_floor, it should be far enough from the current
            elevator location(more than current velocity + 0.5).
            - e.g. if current velocity is 1. at third floor, target can be changed
            as 5, but it can not be changed as 4.
        """
        if new_target > self.current_floor + self.velocity + 0.5:
            self.target_floor = new_target

    def get_on_elevator(self, passengers: Set["Passenger"]) -> None:
        """Get on the elevator."""
        for passenger in passengers:
            self.target_to_passengers[passenger.target_floor].add(passenger)

    def get_off_elevator(self) -> int:
        """Get off the elevator.

        Returns:
            (int) number of passengers getting off.
        """
        num_passengers = len(self.target_to_passengers[self.current_floor])
        self.target_to_passengers[self.current_floor].clear()
        return num_passengers


class Passenger:
    """Passenger."""

    def __init__(self, begin_floor: Floor, floors: List[Floor]) -> None:
        """Initialize."""
        self.begin_floor: Floor = begin_floor
        self.target_floor: Floor = self.get_target_floor(floors)

    def get_target_floor(self, floors: List[Floor]) -> Floor:
        """Get target floor."""
        target_floor = random.sample(
            [floor for floor in floors if floor != self.begin_floor], k=1
        )[0]
        return target_floor

    @property
    def direction(self) -> Direction:
        """Get direction of the passenger."""
        if self.begin_floor < self.target_floor:
            return 1
        if self.begin_floor > self.target_floor:
            return -1
        raise RuntimeError(
            "Passenger's current floor and target floor should be different."
        )
