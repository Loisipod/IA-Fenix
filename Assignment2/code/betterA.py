import time
from agent import Agent
import fenix

class AlphaBeta(Agent):
    def act(self, state, remaining_time):
        if state.is_terminal():
            return None
        actions = state.actions()
        if len(actions) == 1:
            return actions[0]

        player = state.to_move()
        deadline = time.time() + min(5, remaining_time / (2 * len(actions)))

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        # profondeur dynamique
        if len(actions) <= 4:
            depth = 5
        elif len(actions) <= 8:
            depth = 4
        else:
            depth = 3

        # Trier les actions
        actions.sort(key=lambda a: self.evaluate(state.result(a), player), reverse=True)

        for action in actions:
            if time.time() > deadline:
                break

            child = state.result(action)
            score = self.min_value(child, alpha, beta, player, deadline, depth - 1, filtered=False)

            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, score)

        return best_action

    def max_value(self, state, alpha, beta, player, deadline, depth, filtered):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline or depth == 0:
            return self.evaluate(state, player)

        value = float('-inf')
        actions = self.get_action(state, filtered)
        for action in actions:
            child = state.result(action)
            value = max(value, self.min_value(child, alpha, beta, player, deadline, depth - 1, filtered=True))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, state, alpha, beta, player, deadline, depth, filtered):
        if state.is_terminal():
            return state.utility(player)
        if time.time() > deadline or depth == 0:
            return self.evaluate(state, player)

        value = float('inf')
        actions = self.get_action(state, filtered)
        for action in actions:
            child = state.result(action)
            value = min(value, self.max_value(child, alpha, beta, player, deadline, depth - 1, filtered=True))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def get_action(self, state, filtered):
        actions = state.actions()
        if not filtered:
            return actions
        best_score = -1
        best_actions = []
        for a in actions:
            s = self.capture_score(state, a)
            if s > best_score:
                best_score = s
                best_actions = [a]
            elif s == best_score:
                best_actions.append(a)
        return best_actions if best_score > 0 else actions

    def capture_score(self, state, action):
        captured = state.captured_by(action) if hasattr(state, 'captured_by') else []
        score = 0
        for pos in captured:
            value = state.pieces.get(pos, 0)
            score += self.piece_value(value)
        return score

    def evaluate(self, state, player):
        score = 0
        for pos, val in state.pieces.items():
            if val * player > 0:
                score += self.piece_value(val)
                if self.is_exposed(state, pos, player):
                    score -= 0.5
            elif val * player < 0:
                score -= self.piece_value(val)

        # Bonus pour le roi
        if state._has_king(player):
            score += 2
        if not state._has_king(-player):
            score += 5
        return score

    def piece_value(self, val):
        abs_val = abs(val)
        if abs_val == 1: return 1
        elif abs_val == 2: return 2
        elif abs_val == 3: return 4 
        return 0

    def is_exposed(self, state, pos, player):
        x, y = pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if neighbor in state.pieces and state.pieces[neighbor] * player > 0:
                return False
        return True
