import math
import time
import random
import numpy as np
from Util import *
from States import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

# Helpful links
# https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
# https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data

last_loc, last_vel = [0,0,0], [0,0,0]
last_ball_loc, last_ball_vel = [0,0,0], [0,0,0]

class DependableBot(BaseAgent):

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.me = obj()
        self.ball = obj()
        self.players = []
        self.start = time.time()
        self.activeBoosts = []
        self.index = 0

        self.state = driveToBall()
        self.state.val = 2
        self.controller = dependableController

        self.startJump = time.time()
        self.lastHitBall = time.time()

    def nextState(self):
        if self.state.val == DEFEND:
            if self.state.expired:
                if self.me.boost < 20:
                    self.state = collectBoost()
                    self.badSwitch()
                else:
                    self.state = driveToBall()
                    self.badSwitch()
        elif self.state.val == COLLECT_BOOST:
            if self.me.boost > 60:
                self.state = driveToBall()
                self.badSwitch()
        elif self.state.val == DRIVE_TO_BALL:
            if distance2D(self.me.location.data, self.ball.location.data) < 400:
                self.state = takeShot()
                self.badSwitch()
        elif self.state.val == PUSH_BALL:
            if self.me.location.data[1]*sign(self.team) < self.ball.location.data[1]*sign(self.team):
                if self.me.boost < 20:
                    self.state = collectBoost()
                    self.badSwitch()
                else:
                    self.state = defend()
                    self.badSwitch()
        elif self.state.val == TAKE_SHOT:
            if self.me.location.data[1]*sign(self.team) < self.ball.location.data[1]*sign(self.team) or distance2D(self.me.location.data, self.ball.location.data) > 600:
                if self.me.boost < 20:
                    self.state = collectBoost()
                    self.badSwitch()
                else:
                    self.state = defend()
                    self.badSwitch()
        else:
            self.state = defend()
            self.badSwitch()

    def switchToRandomState(self):
        rand = random.randint(0,4)
        if rand == 0:
            self.state = defend()
        elif rand == 1:
            self.state = collectBoost()
        elif rand == 2:
            self.state = driveToBall()
        elif rand == 3:
            self.state = pushBall()
        elif rand == 4:
            self.state = takeShot()

    def switchEarly(self):
        if False:
            switchToRandomState()

    def badSwitch(self):
        if False:
            switchToRandomState()

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.preprocess(game)
        self.nextState()
        self.switchEarly()

        ball_location = Vector2(game.game_ball.physics.location.x, game.game_ball.physics.location.y)
        my_car = game.game_cars[self.index]
        car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
            action_display = "turn left"
        else:
            turn = 1.0
            action_display = "turn right"

        if my_car.jumped or my_car.double_jumped:
            action_display += "\njump"

        # Comment this out to not display debugging
        draw_debug(self.renderer, my_car, game.game_ball, action_display)

        return self.state.execute(self)

    def preprocess(self, game):
        # Game Tick Packet data found at link below
        # https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
        self.players = []
        car = game.game_cars[self.index]

        global last_loc, last_vel, last_ball_loc, last_ball_vel

        def badPacket(val):
            rand = random.randint(1, 100)
            if rand <= 1:
                return random.uniform(-9999, 9999)
            return val

        self.me.location.data = [badPacket(car.physics.location.x), badPacket(car.physics.location.y), badPacket(car.physics.location.z)]
        self.me.velocity.data = [badPacket(car.physics.velocity.x), badPacket(car.physics.velocity.y), badPacket(car.physics.velocity.z)]
        self.me.rotation.data = [car.physics.rotation.pitch, car.physics.rotation.yaw, car.physics.rotation.roll]
        self.me.rvelocity.data = [car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z]
        self.me.matrix = rotator_to_matrix(self.me)
        self.me.boost = car.boost

        ball = game.game_ball.physics

        self.ball.location.data = [badPacket(ball.location.x), badPacket(ball.location.y), badPacket(ball.location.z)]
        self.ball.velocity.data = [badPacket(ball.velocity.x), badPacket(ball.velocity.y), badPacket(ball.velocity.z)]
        self.ball.rotation.data = [ball.rotation.pitch, ball.rotation.yaw, ball.rotation.roll]
        self.ball.rvelocity.data = [ball.angular_velocity.x, ball.angular_velocity.y, ball.angular_velocity.z]

        # x-bounds: +/-4096 uu
        # y-bounds: +/-6300 uu
        # ceiling: 2044 uu
        # pkt rate: 10 pkts/s = 1 pkt/100 ms
        # max velocity: 2300 uu/s = 230 uu/ms

        current_loc = self.me.location.data
        current_vel = self.me.velocity.data
        vel = np.array(self.me.velocity.data)
        vel_mag = np.linalg.norm(vel)

        if (-4096 <= current_loc[0] <= 4096) and (-6300 <= current_loc[1] <= 6300) and (0 <= current_loc[2] <= 2044):
            if all(abs(current_loc[i] - last_loc[i]) <= vel_mag for i in range(0, 3)):
                last_loc = self.me.location.data
            else:
                self.me.location.data = last_loc
        else:
            self.me.location.data = last_loc

        if all(abs(v) <= 2300 for v in current_vel):
            last_vel = self.me.velocity.data
        else:
            self.me.velocity.data = last_vel

        current_ball_loc = self.ball.location.data
        current_ball_vel = self.ball.velocity.data
        ball_vel = np.array(self.ball.velocity.data)
        ball_vel_mag = np.linalg.norm(ball_vel)

        if (-4096 <= current_ball_loc[0] <= 4096) and (-6300 <= current_ball_loc[1] <= 6300) and (0 <= current_ball_loc[2] <= 2044):
            if all(abs(current_ball_loc[i] - last_ball_loc[i]) <= ball_vel_mag for i in range(0, 3)):
                last_ball_loc = self.ball.location.data
            else:
                self.ball.location.data = last_ball_loc
        else:
            self.ball.location.data = last_ball_loc

        if all(abs(v) <= 2300 for v in current_ball_vel):
            last_ball_vel = self.ball.velocity.data
        else:
            self.ball.velocity.data = last_ball_vel

        self.ball.local_location = to_local(self.ball,self.me)

        # collects info for all other cars in match, updates objects in self.players accordingly
        for i in range(game.num_cars):
            if i != self.index:
                car = game.game_cars[i]
                temp = obj()
                temp.index = i
                temp.team = car.team
                temp.location.data = [car.physics.location.x, car.physics.location.y, car.physics.location.z]
                temp.velocity.data = [car.physics.velocity.x, car.physics.velocity.y, car.physics.velocity.z]
                temp.rotation.data = [car.physics.rotation.pitch, car.physics.rotation.yaw, car.physics.rotation.roll]
                temp.rvelocity.data = [car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z]
                temp.boost = car.boost
                flag = False
                for item in self.players:
                    if item.index == i:
                        item = temp
                        flag = True
                        break
                if not flag:
                    self.players.append(temp)

        self.activeBoosts = [None] * 6
        self.activeBoosts[0] = game.game_boosts[18].is_active
        self.activeBoosts[1] = game.game_boosts[15].is_active
        self.activeBoosts[2] = game.game_boosts[30].is_active
        self.activeBoosts[3] = game.game_boosts[4].is_active
        self.activeBoosts[4] = game.game_boosts[29].is_active
        self.activeBoosts[5] = game.game_boosts[3].is_active

# Debugging render stuff

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction


def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)

def draw_debug(renderer, car, ball, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.end_rendering()