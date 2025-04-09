import time
from agent import Agent
import fenix

class AlphaBet(Agent):
    def act(self, state, remaining_time):
        actions = state.actions()
        if len(actions) == 1:
            return actions[0]

        # Allocation dynamique : on réserve un peu de marge
        time_per_action = min(5, remaining_time / (2 * len(actions)))
        deadline = time.time() + time_per_action

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        player = state.to_move()

        for action in actions:
            child = state.result(action)
            value = self.min_value(child, alpha, beta, player, deadline)
            if value > best_score:
                best_score = value
                best_action = action
            alpha = max(alpha, value)

        return best_action

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

        def score_for(p):
            score = 0
            for value in piece_values:
                if value * p > 0:
                    abs_val = abs(value)
                    if abs_val == 1:
                        score += 0.01
                    elif abs_val == 2:
                        score += 0.05
                    elif abs_val == 3:
                        score += 0.2
            return score
        utilities.append(score_for(player) - score_for(-player))
        
        def final_util(utilities):
            util = 0
            for a in utilities:
                util += a
            return util/len(utilities)
        
        
        return final_util(utilities)