from Resource import *
from Player import *
class World:
	def __init__(self, name=None):
		self.name = name
		self.resources = []
		self.players = []

	def add_resource(self, amount):
		self.resources.append(Resource(amount=amount))

	def add_player(self, name):
		player_id = len(self.players)
		player = Player(name=name, world=self, player_id=player_id)
		self.players.append(player)
		return player

	def get_player(self, name):
		for player in self.players:
			if player.name == name:
				return player
		return None

	def print_state(self):
		print("Players:")
		for player in self.players:
			print(player.name)
			print("Army: ", player.army)
			print("Resource: ", player.resource)
		print()
		print("Resources")
		for r in self.resources:
			if r is not None:
				print(r.amount)
		print()



