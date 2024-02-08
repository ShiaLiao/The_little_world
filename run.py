# create Agents and run the simulation
from Agent_01 import Agent
import random
# define a function to generate random positions
def random_position():
    return random.randint(0,3), random.randint(0,3)

# create a list of agents
agents = [
    Agent(id= 1, pos=random_position(), age = random.randint(1,50), abilities = {'food_production': 3, 'clothes_production': 2, 'tools_production': 1}),
    Agent(id= 2, pos=random_position(), age = random.randint(1,50), abilities = {'food_production': 1, 'clothes_production': 3, 'tools_production': 1}),
    Agent(id= 3, pos=random_position(), age = random.randint(1,50), abilities = {'food_production': 1, 'clothes_production': 1, 'tools_production': 10})
]

# run the simulation
# print every n days
n = 20
for day in range(101):
    for agent in agents:
        agent.update(agents)

    if day % n == 0:
        print("Day", day+1)
        for agent in agents:
            if agent.is_alive:
                print("Agent", agent.id, "at", agent.pos, "has", agent.food, "food,", agent.clothes, "clothes,", agent.tools, "tools,", agent.fullness, "fullness,", agent.warmth, "warmth,", agent.stamina, "stamina,", agent.age, "age,", agent.time, "time.")
            else:
                print("Agent", agent.id, "is dead.")
        print()
print("Simulation finished.")
