import random_agent, alphabeta
import game_manager
import fenix
import visual_game_manager
import time
import agent

running = visual_game_manager.VisualGameManager
running.play(running(red_agent=alphabeta.AlphaBeta(agent.Agent), black_agent=random_agent.RandomAgent(agent.Agent)))