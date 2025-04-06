import random_agent, alphabeta
import game_manager
import fenix
import visual_game_manager
import time
import agent

inp = input("Enter 0 for graphic interface (pvp or pve game), n for running the game n times and show results (ai vs ai only, replace n by a number) \n=>")
if int(inp) == 0:
    running = visual_game_manager.VisualGameManager
    running.play(running(black_agent=alphabeta.AlphaBeta(agent.Agent)))
else:
    for i in range(int(inp)):
        running = game_manager.TextGameManager(agent_1=alphabeta.AlphaBeta(agent.Agent), agent_2=random_agent.RandomAgent(agent.Agent))
        running.play()


    
        
