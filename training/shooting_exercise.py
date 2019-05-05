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

class DependableGrader(CompoundGrader):
    def __init__(self, timeout_seconds=120.0, ally_team=0):
        super().__init__([
            PassOnGoalForAllyTeam(ally_team),
            FailOnTimeout(timeout_seconds),
        ])

@dataclass
class DependableExercise(TrainingExercise):
    grader: Grader = field(default_factory=DependableGrader)

@dataclass
class RandomBall(DependableExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 300),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

class WrongGoalFail(Fail):
    def __repr__(self):
        return f'{super().__repr__()}: Ball went into the wrong goal.'

@dataclass
class PassOnGoalForAllyTeam(Grader):
    """
    Terminates the Exercise when any goal is scored.
    Returns a Pass iff the goal was for ally_team,
    otherwise returns a Fail.
    """
    ally_team: int  # The team ID, as in game_datastruct.PlayerInfo.team
    init_score: Optional[Mapping[int, int]] = None  # team_id -> score

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Union[Pass, WrongGoalFail]]:
        score = {
            team.team_index: team.score
            for team in tick.game_tick_packet.teams
        }
        # Initialize or re-initialize due to some major change in the tick packet.
        if (
            self.init_score is None
            or score.keys() != self.init_score.keys()
            or any(score[t] < self.init_score[t] for t in self.init_score)
        ):
            self.init_score = score
            return

        scoring_team_id = None
        for team_id in self.init_score:
            if self.init_score[team_id] < score[team_id]:  # team score value has increased
                assert scoring_team_id is None, "Only one team should score per tick."
                scoring_team_id = team_id

        if scoring_team_id is not None:
            return Pass() if scoring_team_id == self.ally_team else WrongGoalFail()
