import random


import Hunters
import draw_labirynt


class Escapee:
    def __init__(self, escapee_id, environment, alpha=0.1, gamma=0.9, epsilon=0.5):
        self.escapee_id = escapee_id
        self.environment = environment
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.pos_x = None
        self.pos_y = None

    def get_state(self, hunters, exits):
        closest_hunter = min(hunters, key=lambda h: abs(self.pos_x - h.pos_x) + abs(self.pos_y - h.pos_y))
        closest_exit = min(exits, key=lambda e: abs(self.pos_x - e[0]) + abs(self.pos_y - e[1]))
        return (self.pos_x, self.pos_y, closest_hunter.pos_x, closest_hunter.pos_y, closest_exit[0], closest_exit[1])

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def set_state(self, x, y):
        self.pos_x, self.pos_y = x, y

    def print_info(self):
        print(f"Escapee ID: {self.escapee_id} został wczytany do gry")

    def move(self, decision, map):
        if decision == 0:  # Do góry
            if self.pos_y > 0 and map[self.pos_y - 1][self.pos_x] not in[1,2,3]:
                self.pos_y -= 1
        elif decision == 1:  # W dół
            if self.pos_y < len(map) - 1 and map[self.pos_y + 1][self.pos_x] not in[1,2,3]:
                self.pos_y += 1
        elif decision == 2:  # W lewo
            if self.pos_x > 0 and map[self.pos_y][self.pos_x - 1] not in[1,2,3]:
                self.pos_x -= 1
        elif decision == 3:  # W prawo
            if self.pos_x < len(map[0]) - 1 and map[self.pos_y][self.pos_x + 1] not in[1,2,3]:
                self.pos_x += 1

    def dist_to_exit(self, exit):
        return self.a_star_distance((self.pos_x, self.pos_y), exit, self.environment.map)

    def initialize_q_table(self, state, possible_actions):
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in possible_actions}

    def choose_move(self, state, possible_actions):
        self.initialize_q_table(state, possible_actions)
        if random.random() < self.epsilon:  # Eksploracja
            return random.choice(possible_actions)
        else:  # Eksploatacja
            return max(self.q_table[state], key=self.q_table[state].get)

    def a_star_distance(self, start, goal, map):
        from heapq import heappush, heappop

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return g_score[current]

            x, y = current
            neighbors = [
                (x - 1, y), (x + 1, y),  # góra, dół
                (x, y - 1), (x, y + 1)  # lewo, prawo
            ]

            for nx, ny in neighbors:
                if 0 <= nx < len(map[0]) and 0 <= ny < len(map) and map[ny][nx] not in [1, 3]:
                    tentative_g_score = g_score[current] + 1
                    if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = tentative_g_score
                        f_score[(nx, ny)] = tentative_g_score + heuristic((nx, ny), goal)
                        heappush(open_set, (f_score[(nx, ny)], (nx, ny)))

        return float('inf')
    def update_q_table(self, o_state, action, reward, n_state, possible_actions):
        self.initialize_q_table(n_state, possible_actions)
        max_future_q = max(self.q_table[n_state].values()) if n_state in self.q_table else 0
        current_q = self.q_table[o_state][action]
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[o_state][action] = new_q

    def calculate_reward(self, state, hunters, exits):
        x, y = state[:2]
        # Kara za powtarzanie tej samej pozycji
        if (x, y) == (self.pos_x, self.pos_y):
            stationary_penalty = 10
        else:
            stationary_penalty = 0
        # Kara za bliskość łowców
        hunter_penalty = sum(max(0, 10 - self.a_star_distance((x, y), (hunter.pos_x,hunter.pos_y), self.environment.map)) for hunter in hunters)

        # Nagroda za bliskość wyjścia
        exit_distances = [self.a_star_distance((x, y), exit, self.environment.map) for exit in exits]
        exit_reward = max(50 - min(exit_distances), 0)  # Im bliżej wyjścia, tym większa nagroda

        # Jeśli uciekinier osiągnął wyjście, uznaje to za zakończenie gry lub przejście przez wyjście
        if min(exit_distances) == 0:  # Dotarcie do wyjścia
            return 100  # Duża nagroda za osiągnięcie celu

        return exit_reward - hunter_penalty - stationary_penalty

    def check_possible_actions(self, actions, map):
        new_actions = []
        for action in actions:
            if action == 0:  # Do góry
                if self.pos_y > 0 and map[self.pos_y - 1][self.pos_x] not in[1,2,3]:
                    new_actions.append(action)
            elif action == 1:  # W dół
                if self.pos_y < len(map) - 1 and map[self.pos_y + 1][self.pos_x] not in[1,2,3]:
                    new_actions.append(action)
            elif action == 2:  # W lewo
                if self.pos_x > 0 and map[self.pos_y][self.pos_x - 1] not in[1,2,3]:
                    new_actions.append(action)
            elif action == 3:  # W prawo
                if self.pos_x < len(map[0]) - 1 and map[self.pos_y][self.pos_x + 1] not in[1,2,3]:
                    new_actions.append(action)
        return new_actions

    def step(self, hunters, exits, possible_actions):
        old_state = self.get_state(hunters, exits)
        self.initialize_q_table(old_state, possible_actions)

        action_distances = {}
        for action in possible_actions:
            self.move(action, self.environment.map)
            new_state = self.get_state(hunters, exits)
            distance_to_exit = min(
                self.a_star_distance((new_state[0], new_state[1]), exit, self.environment.map) for exit in exits)
            action_distances[action] = distance_to_exit
            self.set_state(old_state[0], old_state[1])  # Cofnięcie ruchu

        best_action = min(action_distances, key=action_distances.get)
        self.move(best_action, self.environment.map)

        # Aktualizacja Q-tabeli
        new_state = self.get_state(hunters, exits)
        reward = self.calculate_reward(new_state, hunters, exits)
        self.update_q_table(old_state, best_action, reward, new_state, possible_actions)
        self.epsilon = max(self.epsilon * 0.995, 0.05)