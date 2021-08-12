import random

def world_economy_mover_func():
	down_rate = float(random.randint(50, 100) / 90)
	up_rate = float(random.randint(50, 100) / 90)
	if down_rate < up_rate:
		return (down_rate - up_rate + down_rate)
	elif up_rate < down_rate:
		return (up_rate - down_rate + up_rate)


def move():
	global copper, silver, gold
	iv_of_c = random.randint(100, 120)
	iv_of_s = random.randint(200, 230)
	iv_of_g = random.randint(400, 440)
	world_economy = float(world)
	copper = iv_of_c - world_economy / world_economy
	silver = iv_of_s - world_economy / world_economy
	gold = iv_of_g - world_economy / world_economy


def run():
	global world
	world = world_economy_mover_func()
	if world < 1:
		world = world + (world / 150)
	if world > 1:
		world = world - (world / 150)
	move()

run()

print(copper)
print(silver)
print(gold)