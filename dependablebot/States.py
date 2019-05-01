import math
import time
from rlbot.agents.base_agent import  SimpleControllerState
from Util import *


class defend:
	def __init__(self):
		self.expired = False
		self.val = DEFEND

	def execute(self, agent):
		xlocation = cap(agent.ball.location.data[0]*.8, -900, 900)
		target_location = Vector3([xlocation, 5100*sign(agent.team), 200])
		target_speed = 1399
		if distance2D(target_location, agent.me.location.data) < 1500:
			self.expired = True
		elif (agent.me.location.data[1]+5120)*-sign(agent.team) < 0.75*(agent.ball.location.data[1]+5120)*-sign(agent.team):
			self.expired = True

		return dependableController(agent, target_location, target_speed)

class collectBoost:
	def __init__(self):
		self.expired = False
		self.val = COLLECT_BOOST

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

		return dependableController(agent, target_location, target_speed)

class driveToBall:
	def __init__(self):
		self.expired = False
		self.val = DRIVE_TO_BALL

	def execute(self, agent):
		ballDistance = distance2D(agent.me, agent.ball)
		approachDistance = ballDistance * 0.7
		target_speed = 1600

		# ballLocation = agent.ball.location
		# goalCenter = Vector3([0 , 5100*-sign(agent.team), 200])
		# ballGoalAngle = angle2(ballLocation, goalCenter)
		# xlocation = approachDistance * sign(agent.team) * math.cos(ballGoalAngle)
		# ylocation = approachDistance * sign(agent.team) * math.sin(ballGoalAngle)
		# target_location = ballLocation - Vector3([xlocation, ylocation, 0])

		goal = Vector3([0,-sign(agent.team)*FIELD_LENGTH/2,100])
		ball_to_goal = (goal - agent.ball.location).normalize()
		target_location = agent.ball.location - Vector3([(ball_to_goal.data[0]*approachDistance),(ball_to_goal.data[1]*approachDistance),0])
		
		return dependableController(agent, target_location, target_speed)


class takeShot:
	def __init__(self):
		self.expired = False
		self.val = TAKE_SHOT

	def execute(self, agent):
		target_location = agent.me.location
		target_speed = 1
		return dependableController(agent, target_location, target_speed)


class pushBall:
	def __init__(self):
		self.expired = False
		self.val = PUSH_BALL

	def execute(self, agent):
		ball_height = agent.ball.location.data[2]
		ball_distance = distance2D(agent.me, agent.ball)
		ball_on_wall = ballOnWall(agent)

		if ball_height > 110 and ball_distance < 400 and not ball_on_wall:
			target_speed = velocity2D(agent.ball)
		else:
			target_speed = cap(velocity2D(agent.ball) + 200, 1600, 2300)

		goal = Vector3([0,-sign(agent.team)*FIELD_LENGTH/2,100])

		# ballLocation = agent.ball.location
		# ballGoalAngle = angle2(ballLocation, goal)
		# xlocation = 100 * sign(agent.team) * math.cos(ballGoalAngle)
		# ylocation = 100 * sign(agent.team) * math.sin(ballGoalAngle)
		# target_location = ballLocation - Vector3([xlocation, ylocation, 0])

		ball_to_goal = (goal - agent.ball.location).normalize()
		target_distance = 100
		target_location = agent.ball.location - Vector3([(ball_to_goal.data[0]*target_distance),(ball_to_goal.data[1]*target_distance),0])

		xlocation = ball_to_goal.data[0]*target_distance
		ylocation = ball_to_goal.data[1]*target_distance

		agent.renderer.begin_rendering()
		agent.renderer.draw_string_2d(20, 20, 3, 3, "x: " + str(xlocation), agent.renderer.black())
		agent.renderer.draw_string_2d(20, 60, 3, 3, "y: " + str(ylocation), agent.renderer.black())
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
	if time_difference > 2.2 and distance2D(target_location,agent.me) > (velocity2D(agent.me)*2.5) and abs(angle) < 1.0 and agent.me.location.data[2] < 100:
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