## @package twitter.control_center
# coding: UTF-8

import json
from control_center.PDP import PDP


class PEP:
	"""
	Policy Enforcement Point
	Class who connects to the PDP - Policy Decision Point and forwards its result to the bot
	"""

	def __init__(self):
		"""
		It may need the PDP to be passed as argument, but for now it's creating a new object every time
		"""
		self.pdp = PDP()

	def first_time_policy(self):
		"""
		If a bot has just arrived to twitter, it must be handed a list of initial users for it to follow
		The list is decided by the PDP, and there's no need for extra params, since it's pretty much chosen at random, for now
		"""
		return self.pdp.get_first_time_list()

	def receive_message(self, msg):
		"""
		The receive message applies to when a request comes to this point, for now, the PEP will start by forwarding that message
		After receiving the response from the PDP object, it will enforce a behaviour based on the response

		@param msg - a dictionary containing the message to be passed on
		"""
		data = self.pdp.receive_request(msg)
		return self.enforce(json.loads(data))

	def enforce(self, data):
		"""
		The enforce method will simply turn the response into a boolean value the bot can understand

		@param data: a dictionaru containing the result of the PDP's logic

		@return Boolean permitting/denying the behaviour
		"""

		if "response" in data:
			return data["response"] != "DENY"

		return False
