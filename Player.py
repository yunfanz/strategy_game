import numpy as np

class Player:
	def __init__(self, name, world, player_id):
		self.name = name
		self.world = world
		self.resource = 200
		self.army = 100
		self.id = player_id
		self.knowledge = {'resource':[None]*len(self.world.resources), 
							'player':[None]*len(self.world.players)}

	def passive(self, verbose=False):
		consumption = self.army // 10
		if consumption > self.resource:
			self.army -= consumption - self.resource
			self.resource = 0
		else:
			self.resource -= consumption
			self.army += int(self.resource//100)
		if verbose:
			print(self.name, self.army, self.resource)
		

	def gather_resource(self, resource_id, man_power, verbose=False):
		resource = self.world.resources[resource_id]
		if resource is None:
			return
		if resource.occupied is not None:
			return resource.occupied
		self.army -= man_power
		amount = min(resource.amount, man_power // 2)
		amount = min(amount, 100)
		if amount > 0:
			amount = np.random.randint(0, amount)
		else:
			amount = 0
		resource.amount -= amount
		self.resource += amount
		if resource.amount <= 0:
			self.world.resources[resource_id] = None
		self.army += man_power
		if verbose:
			print("gathered", amount, "from ", resource_id)
		return None

	def attack(self, player_id, man_power, verbose=True):
		if player_id == self.id:
			return None
		player = self.world.players[player_id]
		if self.army < man_power or man_power <= 0:
			#print("can't attack")
			return
		self.army -= man_power
		loot = 0
		if man_power >= player.army:
			success = True
			death_toll = int(np.random.uniform(player.army // 10, player.army//2 + 1))
			player.army -= death_toll
			man_power -= death_toll
			loot = min(player.resource, man_power)
			self.resource += loot
			player.resource -= loot
		else:
			success = False
			death_toll = int(np.random.uniform(man_power // 10, man_power//2 + 1))
			player.army -= death_toll
			man_power -= death_toll
		self.army += man_power
		if verbose:
			print(self.name+" attacked "+player.name, success)
			print("loot ", loot)
			print()
		return success

	def random_action(self, p_gather, p_attack):
		assert p_gather+p_attack <= 1
		man_power = self.army #np.random.randint(low=0, high=self.army+1)
		if self.resource <= self.army // 10:
			p_gather = 1
			man_power = self.army
		a = np.random.uniform(0, 1)
		
		if a < p_gather:
			i = np.random.randint(low=0, high=100)
			self.gather_resource(i, man_power)
		elif a < p_gather+p_attack:
			i = np.random.randint(low=0, high=5)
			self.attack(i, man_power)
		self.passive()
		return

