"""Elevator Environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com

References:
    - gym.Env: https://github.com/openai/gym/blob/master/gym/core.py
"""

from typing import Dict, List, Set, Tuple

import gym

Floor = int
Direction = int  # -1: go down, 1: go up


class ElevatorEnv(gym.Env):
    """Elevator gym environment."""

    def __init__(
        self,
        floor_range: Tuple[int, int],
        max_people: int = 100,
    ) -> None:

        self.base_floor = 1
        self.max_people = max_people

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


class Passenger:
    """Passenger."""

    def __init__(self, target: int) -> None:
        """Initialize."""
        self.target = target

    def get_direction(self, floor: Floor) -> Direction:
        """Get direction of the passenger."""
        if floor < self.target:
            return 1
        if floor > self.target:
            return -1
        raise RuntimeError(
            "Passenger's current floor and target floor should be different."
        )
