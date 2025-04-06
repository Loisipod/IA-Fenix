import time
from agent import Agent
import fenix
from math import sqrt, log, exp

class AlphaBeta(Agent):
    def act(self, state, remaining_time):
        actions = state.actions()
        if len(actions) == 1:
            return actions[0]

        num_actions = len(actions)
        player = state.to_move()

        # === Allocation dynamique (asymptotique) ===
        total_time_budget = self.compute_time_budget(remaining_time, num_actions, state.turn)

        deadline = time.time() + total_time_budget

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        for action in actions:
            if time.time() > deadline:
                break  # on s'arrête dès que le budget est épuisé

            child = state.result(action)
            score = self.min_value(child, alpha, beta, player, deadline)

            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, score)

        return best_action

    def compute_time_budget(self, T_remain, N_actions, turn):
        if turn < 10:
            return 2.0  # tours de placement, faible impact stratégique

        k = 0.025
        c = 2
        MAX_TIME = 15
        try:
            ratio = sqrt(T_remain) * log(log(N_actions + c))
            return MAX_TIME * (1 - exp(-k * ratio))
        except:
            return 0.5



    def max_value(self, state, alpha, beta, player, deadline):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline:
            return self.evaluate(state, player)

        value = float('-inf')
        for action in state.actions():
            child = state.result(action)
            value = max(value, self.min_value(child, alpha, beta, player, deadline))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, state, alpha, beta, player, deadline):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline:
            return self.evaluate(state, player)

        value = float('inf')
        for action in state.actions():
            child = state.result(action)
            value = min(value, self.max_value(child, alpha, beta, player, deadline))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def evaluate(self, state, player):
        utilities = []
        piece_values = state.pieces.values()

        def pieces_count(p):
            score = 0
            for value in piece_values:
                if value * p > 0:
                    abs_val = abs(value)
                    if abs_val == 1:
                        score += 0.1
                    elif abs_val == 2:
                        score += 0.2
                    elif abs_val == 3:
                        score += 0.7
            return score
        utilities.append(pieces_count(player) - pieces_count(-player))

        
        def final_util(utilities):
            util = 0
            for a in utilities:
                util += a
            return util/len(utilities)
        
        
        return final_util(utilities)
