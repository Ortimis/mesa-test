# mesa imports
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# visualisation imports
import matplotlib.pyplot as plot
import numpy as np


class InfectModel(Model):
    """A model with some number of agents and a patient 0"""

    def __init__(self, N, width, height):
        super()
        self.running = True
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        self.num_innocent_agents = N
        self.time_contagious = 7

        # Create agents
        for i in range(self.num_innocent_agents):
            a = HumanAgent(i + 1, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.patient0 = HumanAgent(0, self)
        self.schedule.add(self.patient0)

        self.datacollector = DataCollector(
            model_reporters={"Gini": ""},
            agent_reporters={
                "Infected": "is_infected",
                "Immune": "is_immune",
                "Contagious": "is_contagious",
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


class HumanAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.is_infected = False
        self.is_immune = False
        self.is_contagious = False
        self.time_since_infection = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def spread_virus(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for mate in cellmates:
                mate.is_infected = True

    def step(self):

        self.move()

        if self.is_infected == True:
            self.time_since_infection += 1

        if self.time_since_infection < self.model.time_contagious:
            self.is_contagious = True
        else:
            self.is_contagious = False

        if self.is_contagious == True:
            self.spread_virus()


"""
def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N-i) for i, xi in enumerate(x)) / (N*sum(x))
    return (1 + (1/N) - 2*B)
"""

model = InfectModel(N=50, width=10, height=10)
for i in range(100):
    model.step()
    print(model.schedule.agents)

""" gini = model.datacollector.get_model_vars_dataframe()
print(type(gini))
gini.plot()
plot.show() """

""" agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()
plt.show() """
