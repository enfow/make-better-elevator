"""Elevator Environment.

Author: Kyeongmin Woo
Email: wgm0601@gmail.com

References:
    - gym.Env: https://github.com/openai/gym/blob/master/gym/core.py
"""

from typing import Dict, List, Tuple

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
        # number of passegeners waiting for the elevator 
        self.floor_to_passengers: Dict[int, int] = {floor: 0 for floor in self.floors}
        # number of people on each floor
        self.floor_to_people: Dict[int, int] = {floor: 0 for floor in self.floors}

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
        self.floor_to_passengers = {floor: 0 for floor in self.floors}
        self.floor_to_people = {floor: 0 for floor in self.floors}

    def render(self, mode="human") -> None:
        """render."""
        raise NotImplementedError


class Passenger:
    """Passenger."""

    def __init__(self, target: int) -> None:
        self.target = target
