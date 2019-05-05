from pathlib import Path
from shooting_exercise import RandomBall
from rlbot.matchconfig.match_config import PlayerConfig, Team

def make_default_playlist():
    exercises = [
        RandomBall("Shooting Bot Normal"),
    ]
    for exercise in exercises:
        path_to_bot = Path(__file__).absolute().parent.parent / "dependablebot" / "dependablebot.cfg"
        exercise.match_config.player_configs = [
            PlayerConfig.bot_config(path_to_bot, Team.BLUE)
        ]
    return exercises
