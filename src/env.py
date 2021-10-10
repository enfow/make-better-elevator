"""Elevator Environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com

References:
    - gym.Env: https://github.com/openai/gym/blob/master/gym/core.py
"""

import random
from typing import Dict, List, Set, Tuple

import gym

Floor = int
Direction = int  # -1: go down, 1: go up

BASE_FLOOR = 1


class ElevatorEnv(gym.Env):
    """Elevator gym environment."""

    def __init__(
        self,
        floor_range: Tuple[int, int],
        max_people: int = 100,
        num_elevator: int = 1,
    ) -> None:

        self.max_people = max_people
        self.num_elevator = num_elevator

        self.floors: List[int] = [
            i for i in range(floor_range[0], floor_range[1] + 1, 1) if i != 0
        ]
        # number of passegeners waiting for the elevator
        self.floor_to_passengers: Dict[Floor, Dict[Direction, Set["Passenger"]]] = {
            floor: self.get_empty_floor() for floor in self.floors
        }
        # number of people on each floor
        self.floor_to_people: Dict[Floor, int] = {floor: 0 for floor in self.floors}

        self.reset()

    def step(self, action) -> None:
        """step.
        Notes:
            - action: target floor for each elevator.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """reset the env.
        Notes:
            - the number of passanger is 0.
            - all of the elevators are located on the first floor.
        """
        self.floor_to_passengers = {
            floor: self.get_empty_floor() for floor in self.floors
        }
        self.floor_to_people = {floor: 0 for floor in self.floors}
        self.floor_to_people[1] = self.max_people

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
        self.target_to_passengers: Dict[Floor, Set["Passenger"]] = {
            floor: set() for floor in floors
        }
        self.current_floor = BASE_FLOOR

    def get_on(self, passengers: Set["Passenger"]):
        """Get on the elevator."""
        for passenger in passengers:
            self.target_to_passengers[passenger.target_floor].add(passenger)

    def get_off(self) -> int:
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
