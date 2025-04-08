import time
from agent import Agent
import fenix
from math import sqrt, log, exp

class AlphaBeta(Agent):
    def act(self, state, remaining_time):
        if state.is_terminal():
            return None
        actions = self.filter_actions(state.actions(), state)
        if len(actions) == 1:
            return actions[0]

        num_actions = len(actions)
        player = state.to_move()

        # === Allocation dynamique (asymptotique) ===
        total_time = self.time_check(remaining_time, num_actions, state.turn)

        deadline = time.time() + total_time

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        if num_actions <= 4:
            depth = 5
        elif num_actions <= 8:
            depth = 4
        else:
            depth = 3


        #trier les actions par les meilleures d'abord
        actions.sort(key=lambda a: self.evaluate(state.result(a), player), reverse=True)

        for action in actions:
            if time.time() > deadline:
                break  # on s'arrête dès que le budget est épuisé

            child = state.result(action)
            score = self.min_value(child, alpha, beta, player, deadline, depth-1)

            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, score)

        return best_action

    def time_check(self, T_remain, N_actions, turn):
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

    def filter_actions(self, actions, state):  #filtrer les actions (avec des règle de capture)
        max_capture = -1
        filtered = []

        for action in actions:
            score = self.capture_score(state, action)
            if score > max_capture:
                max_capture = score
                filtered = [action]
            elif score == max_capture:
                filtered.append(action)

        return filtered if max_capture > 0 else actions

    def capture_score(self, state, action): # évaluer combien de pièces sont capturées
        result = state.result(action)
        captured = state.captured_by(action) if hasattr(state, 'captured_by') else []
        
        score = 0
        for pos in captured:
            value = state.pieces.get(pos, 0)
            score += self.piece_value(value)
        return score


    def max_value(self, state, alpha, beta, player, deadline, depth):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline or depth == 0:
            return self.evaluate(state, player)

        value = float('-inf')
        actions = self.filter_actions(state.actions(), state)
        actions.sort(key=lambda a: self.evaluate(state.result(a), player), reverse=True)
        for action in actions:
            child = state.result(action)
            value = max(value, self.min_value(child, alpha, beta, player, deadline, depth-1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, state, alpha, beta, player, deadline, depth):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline or depth == 0:
            return self.evaluate(state, player)

        value = float('inf')
        actions = self.filter_actions(state.actions(), state)
        actions.sort(key=lambda a: self.evaluate(state.result(a), -player), reverse=True)
        for action in actions:
            child = state.result(action)
            value = min(value, self.max_value(child, alpha, beta, player, deadline, depth-1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def evaluate(self, state, player): #évalue la position actuelle pour un côté
        score = 0
        pieces = state.pieces

        for pos, val in pieces.items():
            if val * player > 0:
                score += self.piece_value(val)
                if abs(val) >= 2 and self.is_exposed(state, pos, player):
                    score -= 1.5 #p^énalité si pièce isolée
            elif val * player < 0:
                score -= self.piece_value(val)

        def has_king(p):
            return any(v == 3 * p for v in pieces.values())

        if has_king(player) and not has_king(-player):
            score += 5
        elif not has_king(player) and has_king(-player):
            score -= 5

        return score

    def piece_value(self, val):
        abs_val = abs(val)
        if abs_val == 1: return 1
        elif abs_val == 2: return 2
        elif abs_val == 3: return 3
        return 0
    
    def is_exposed(self, state, pos, player):
        x, y = pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x+dx, y+dy)
            if neighbor in state.pieces and state.pieces[neighbor] * player > 0:
                return False
        return True

