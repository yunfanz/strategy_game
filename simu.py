from World import World
from Resource import *
from Player import Player
import pylab as plt
import numpy as np

human_play = False

world = World()

for k in range(100):
	world.add_resource(10000)
	#world.add_resource(10000)

cynthia = world.add_player("Cynthia")
jeremy = world.add_player("Jeremy")
scott = world.add_player("Scott")
mary = world.add_player("Mary")

if human_play:
	myname = input("What is your name? ")
	me = world.add_player(myname)
else:
	me = world.add_player("Gerry")

nturns = 3000
player_attributes = np.zeros((2,len(world.players),nturns))


for turn in range(nturns):
	try:
		print("# Turn", turn)
		cynthia.random_action(p_gather=0.8, p_attack=0.2)
		jeremy.random_action(p_gather=0.7, p_attack=0.3)
		scott.random_action(p_gather=1., p_attack=0.0)
		mary.random_action(p_gather=0.9, p_attack=0.1)
		if not human_play:
			me.random_action(p_gather=0.95, p_attack=0.05)
		else:
			action = input("gather or attack? ")
			man_power = me.army
			if action =='a':
				target_name = input("who to attack? ")
				target = world.get_player(target_name)
				me.attack(target.id, man_power, verbose=True)
			else:
				#resource_id = eval(input("Resource id to gather from? "))
				#resource_id = resource_id % 100
				resource_id = np.random.randint(0,100)
				me.gather_resource(resource_id, man_power, verbose=True)
			me.passive(verbose=True)

		for i, pl in enumerate(world.players):
			player_attributes[0,i,turn] = pl.army
			player_attributes[1,i,turn] = pl.resource
	except(KeyboardInterrupt):
		player_attributes = player_attributes[...,:turn]
		break
	#world.print_state()
world.print_state()
f, ax = plt.subplots(2,1)
for i in range(player_attributes.shape[1]):
	ax[0].plot(player_attributes[0,i],label=world.players[i].name)
	ax[1].plot(player_attributes[1,i],label=world.players[i].name)
ax[0].set_ylabel('army')
ax[1].set_ylabel('resource')
plt.legend()
plt.show()
