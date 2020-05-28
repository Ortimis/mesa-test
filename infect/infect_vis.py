from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from infect import InfectModel


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5,
                 "Color": "grey",
                 }

    if agent.is_contagious:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    if agent.is_immune:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule([{"Label": "Chart",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(InfectModel,
                       [grid, chart],
                       "Money Model",
                       {"N": 10, "width": 10, "height": 10})
server.port = 8522  # The default
server.launch()
