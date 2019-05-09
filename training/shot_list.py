from math import pi
from dataclasses import dataclass, field
from typing import Optional, Mapping, Union
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.training.training import Pass, Fail
from rlbottraining.training_exercise import TrainingExercise
from rlbottraining.training_exercise import Playlist
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.grading.grader import Grader
from rlbottraining.grading.event_detector import PlayerEventType
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.common_graders.timeout import FailOnTimeout, PassOnTimeout
from shooting_exercise import DependableExercise
import time

@dataclass
class ShotTest0(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 0: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 17),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

@dataclass
class ShotTest1(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 1: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 17),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest2(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 2: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(2500, -2500, 17),
                        rotation=Rotator(0, 3 * pi / 4, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest3(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 3: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(-2500, -2500, 17),
                        rotation=Rotator(0, pi / 4, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest4(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 4: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(3000, 0, 17),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest5(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 5: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(-3000, 0, 17),
                        rotation=Rotator(0, 0, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest6(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 6: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(2500, 2500, 17),
                        rotation=Rotator(0, 5 * pi / 4, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest7(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 7: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(-2500, 2500, 17),
                        rotation=Rotator(0, 7 * pi / 4, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest8(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 8: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(3000, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 17),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest9(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 9: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(-3000, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 17),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest10(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 10: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(3000, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest11(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 11: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(-3000, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest12(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 12: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(3000, -4000, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest13(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 13: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(-3000, -4000, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest14(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 14 %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(900, -4000, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class ShotTest15(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        print("Time at shot 15: %s", (time.time()))
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(-900, -4000, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 4000, 17),
                        rotation=Rotator(0, 3 * pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )