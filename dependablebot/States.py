import math
import time
from rlbot.agents.base_agent import  SimpleControllerState
from Util import *

'''
class defend:
	def __init__(self):

	def execute(self, agent):

		return dependableController(agent, target_location, target_speed)
'''
class collectBoost:
	def __init__(self):
		self.expired = False

	def conditionsMet(self, agent):
		if agent.me.boost < 20:
			return True
		return False

	def execute(self, agent):
		closest_boost = -1
		closest_distance = 99999
		target_speed = 2300
		while closest_boost == -1:
			for i in range(1,len(boosts)):
				#if distance2D(boosts[i], agent.me) < closest_distance and (distance2D(boosts[i], agent.me) / target_speed) > agent.timers[i]:
				if distance2D(boosts[i], agent.me) < closest_distance and agent.activeBoosts[i] == True:
					closest_boost = i
					closest_distance = distance2D(boosts[i], agent.me)

		target_location = boosts[closest_boost]

		if not self.conditionsMet(agent):
			self.expired = True

        # TODO check for other states to be ready (those that take priority over boost)

		return dependableController(agent, target_location, target_speed)

class driveToBall:
	def __init__(self):
		self.expired = False

	def conditionsMet(self, agent):
		defense = sign(agent.me.location.data[1]) == sign(agent.team)
		ball_between_me_and_goal = False

		if agent.ball.location.data[1]*sign(agent.team) > agent.me.location.data[1]*sign(agent.team):
			ball_between_me_and_goal = True

		if distance2D(agent.ball, agent.me) >= 1000 or (defense and ball_between_me_and_goal):
			return True
		return False

	def execute(self, agent):
		approachDistance = 1000
		if distance2D(agent.ball, agent.me) < 1100:
			target_speed = 400
		elif distance2D(agent.ball, agent.me) < 1500:
			target_speed = 800
		else:
			target_speed = 1600

		ballLocation = agent.ball.location
		goalCenter = Vector3([0 , 5100*-sign(agent.team), 200])
		ballGoalAngle = angle2(ballLocation, goalCenter)
		xlocation = approachDistance * sign(agent.team) * math.cos(ballGoalAngle)
		ylocation = approachDistance * sign(agent.team) * math.sin(ballGoalAngle)
		target_location = ballLocation - Vector3([xlocation, ylocation, 0])

		if not self.conditionsMet(agent):
			self.expired = True
		
		return dependableController(agent, target_location, target_speed)

'''
class takeShot:
	def __init__(self):
		self.expired = False

	def execute(self, agent):

		return dependableController(agent, target_location, target_speed)
'''

class pushBall:
	def __init__(self):
		self.expired = False

	def conditionsMet(self, agent):
		if distance2D(agent.ball, agent.me) < 1000:
			return True
		return False

	def execute(self, agent):
		target_speed = 1200

		goal = Vector3([0,-sign(agent.team)*FIELD_LENGTH/2,100])
		left_post = Vector3([-sign(agent.team)*700 , 5100*-sign(agent.team), 200])
		right_post = Vector3([sign(agent.team)*700, 5100*-sign(agent.team), 200])

		ball_left = angle2(agent.ball, left_post)
		ball_right = angle2(agent.ball, right_post)
		bot_left = angle2(agent.me, left_post)
		bot_right = angle2(agent.me, right_post)

		if bot_left > ball_left and bot_right > ball_right:
			# agent.renderer.begin_rendering()
			# agent.renderer.draw_string_2d(20, 20, 3, 3, "right post", agent.renderer.black())
			# agent.renderer.end_rendering()
			goal = right_post
		elif bot_left < ball_left and bot_right < ball_right:
			goal = left_post

		ball_to_goal = (goal - agent.ball.location).normalize()

		target_distance = cap(distance2D(agent.ball.location, agent.me)/2, 0, 500)

		target_location = agent.ball.location - Vector3([(ball_to_goal.data[0]*target_distance),(ball_to_goal.data[1]*target_distance),0])

		if driveToBall().conditionsMet(agent):
			self.expired = True

		colorRed = cap(int( (2300/2300) * 255),0,255)
		colorBlue =cap(255-colorRed,0,255)

		agent.renderer.begin_rendering()
		agent.renderer.draw_line_3d(agent.ball.location.data, target_location.data, agent.renderer.create_color(255, colorRed, 0, colorBlue))
		agent.renderer.end_rendering()

		return dependableController(agent, target_location, target_speed)

def dependableController(agent, target_location, target_speed):
	controller_state = SimpleControllerState()

	location = toLocal(target_location,agent.me)
	angle = math.atan2(location.data[1],location.data[0])

	speed = velocity2D(agent.me)

	#steering
	controller_state.steer = steer(angle)

	#throttle
	if target_speed > speed:
		controller_state.throttle = 1.0
		if target_speed > 1400 and agent.start > 2.2 and speed < 2250:
			controller_state.boost = True
		else:
			controller_state.boost = False
	elif target_speed < speed:
		controller_state.throttle = 0
		controller_state.boost = False

	#dodging
	time_difference = time.time() - agent.start
	if time_difference > 2.2 and distance2D(target_location,agent.me) > (velocity2D(agent.me)*2.5) and abs(angle) < 1.3 and agent.me.location.data[2] < 100:
		agent.start = time.time()
	elif time_difference <= 0.1:
		controller_state.jump = True
		controller_state.pitch = -1
	elif time_difference >= 0.1 and time_difference <= 0.15:
		controller_state.jump = False
		controller_state.pitch = -1
	elif time_difference > 0.15 and time_difference < 1:
		controller_state.jump = True
		controller_state.yaw = controller_state.steer
		controller_state.pitch = -1

	return controller_state