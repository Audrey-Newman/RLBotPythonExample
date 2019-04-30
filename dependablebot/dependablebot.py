import math
import time
from Util import *
from States import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

#helpful links
#https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
#https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data

class DependableBot(BaseAgent):

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.me = obj()
        self.ball = obj()
        self.players = []
        self.start = time.time()
        self.activeBoosts = []
        self.index = 0

        self.state = defend()
        self.state.val = 0
        self.controller = dependableController

    def nextState(self):
        if self.state.val == DEFEND:
            if self.state.expired:
                if self.me.boost < 20:
                    self.state = collectBoost()
                else:
                    self.state = driveToBall()
        elif self.state.val == COLLECT_BOOST:
            if self.me.boost > 60:
                self.state = driveToBall()
        elif self.state.val == DRIVE_TO_BALL:
            if distance2D(self.me.location.data, self.ball.location.data) < 400:
                self.state = pushBall()
        elif self.state.val == PUSH_BALL:
            if self.me.location.data[1]*sign(self.team) < self.ball.location.data[1]*sign(self.team):
                self.state = defend()
        else:
            self.state = defend()

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.preprocess(game)
        self.nextState()
        return self.state.execute(self)

    def preprocess(self, game):
        #Game Tick Packet data found at link below
        #https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
        self.players = []
        car = game.game_cars[self.index]
        self.me.location.data = [car.physics.location.x, car.physics.location.y, car.physics.location.z]
        self.me.velocity.data = [car.physics.velocity.x, car.physics.velocity.y, car.physics.velocity.z]
        self.me.rotation.data = [car.physics.rotation.pitch, car.physics.rotation.yaw, car.physics.rotation.roll]
        self.me.rvelocity.data = [car.physics.angular_velocity.x, car.physics.angular_velocity.y, car.physics.angular_velocity.z]
        self.me.matrix = rotator_to_matrix(self.me)
        self.me.boost = car.boost

        ball = game.game_ball.physics
        self.ball.location.data = [ball.location.x, ball.location.y, ball.location.z]
        self.ball.velocity.data = [ball.velocity.x, ball.velocity.y, ball.velocity.z]
        self.ball.rotation.data = [ball.rotation.pitch, ball.rotation.yaw, ball.rotation.roll]
        self.ball.rvelocity.data = [ball.angular_velocity.x, ball.angular_velocity.y, ball.angular_velocity.z]

        self.ball.local_location = to_local(self.ball,self.me)

        #collects info for all other cars in match, updates objects in self.players accordingly
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

'''
Can use draw functions to help debug here

def draw_debug(renderer, car, ball, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.end_rendering()
'''