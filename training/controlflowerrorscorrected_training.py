from pathlib import Path
from shooting_exercise import RandomBall
from shot_list import *
from rlbot.matchconfig.match_config import PlayerConfig, Team

def make_default_playlist():
    exercises = [
        ShotTest1("Shot 1"),
        ShotTest2("Shot 2"),
        ShotTest3("Shot 3"),
        ShotTest4("Shot 4"),
        ShotTest5("Shot 5"),
        ShotTest6("Shot 6"),
        ShotTest7("Shot 7"),
        ShotTest8("Shot 8"),
        ShotTest9("Shot 9"),
        ShotTest10("Shot 10"),
        ShotTest11("Shot 11"),
        ShotTest12("Shot 12"),
        ShotTest13("Shot 13"),
        ShotTest14("Shot 14"),
        ShotTest15("Shot 15"),
    ]
    for exercise in exercises:
        path_to_bot = Path(__file__).absolute().parent.parent / "controlflowerrorsbotcorrected" / "controlflowerrorsbotcorrected.cfg"
        exercise.match_config.player_configs = [
            PlayerConfig.bot_config(path_to_bot, Team.BLUE)
        ]
    return exercises
