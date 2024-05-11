# agent_trainer.py
import numpy as np
from algorithm.ann import Network, Layer
from piece import Piece
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE

class AgentTrainer:
    def __init__(self, history_size: int, buf: bytes):
        self.history_size = history_size
        self.network = self.deserialize_network(buf)
        self.id = f"Agent-{self.history_size}-{self.network.inputs}"  # simpler ID format
        self.history = np.zeros(self.history_size, dtype=np.float32)
        self._games = set()
        self.games = 0
        self.wins = 0
        self.score = 0
        self.min_score = float('inf')
        self.max_score = float('-inf')
        self.age = 0
        self.taken = False
        self._player = WHITE

    def on_new_epoch(self):
        self.age += 1
        self.score = 0
        self.games = 0
        self._games = set()
        self.max_score = float('-inf')
        self.min_score = float('inf')
        self.wins = 0
        self.reset()

    def has_played_before(self, player: 'AgentTrainer') -> bool:
        return player.id in self._games

    def set_result(self, score: float, opponent: 'AgentTrainer'):
        self._games.add(opponent.id)
        self.games += 1
        self.score += score
        self.min_score = min(self.min_score, score)
        self.max_score = max(self.max_score, score)
        if score > 0:
            self.wins += 1

    def get_average_score(self) -> float:
        return self.score / self.games

    def get_weights(self) -> np.ndarray:
        return self.network.get_weights()

    def get_topology(self) -> list:
        return self.network.get_topology()

    def serialize(self) -> bytes:
        return self.network.to_binary()

    def reset(self):
        self.history = np.zeros(self.history_size, dtype=np.float32)
        self.taken = False

    def __str__(self) -> str:
        return f"{self.id} with {self.score:.2f} points min: {self.min_score:.2f} max: {self.max_score:.2f} avg: {self.get_average_score():.2f} {self.wins / self.games * 100:.2f}%"

    def set_player(self, player: str):
        self._player = player

    def get_move(self, game_state: str) -> str:
        board = np.zeros(50, dtype=np.float32)
        w_mul = 1 if self._player == WHITE else -1

        for i, piece in enumerate(game_state.split()[1:]):
            is_king = piece.isking()
            pos = int(piece[1:] if is_king else piece)
            board[pos] = w_mul * (2 if is_king else 1)

        for i, piece in enumerate(game_state.split()[3:]):
            is_king = piece.isking()
            pos = int(piece[1:] if is_king else piece)
            board[pos] = -w_mul * (2 if is_king else 1)

        self.history = np.concatenate([board, self.history[:-50]])

        value = np.zeros(self.network.inputs, dtype=np.float32)
        value[:50] = board
        value[50:] = self.history

        pos = 0
        pos_val = float('-inf')

        moves = self.get_moves(game_state)

        for i, move in enumerate(moves):
            val = value.copy()
            val[move.from_position - 1] = -1
            val[move.to_position - 1] = 1

            result = self.network.predict(val)

            if result[0] > pos_val:
                pos = i
                pos_val = result[0]

        return f"{moves[pos].from_position}-{moves[pos].to_position}"

    def deserialize_network(self, buf: bytes) -> 'Network':
        topology = np.frombuffer(buf, dtype=np.int32, count=3)
        inputs, outputs, length = topology
        layers = []
        offset = 3
        for _ in range(length):
            layer_topology = np.frombuffer(buf, dtype=np.int32, offset=offset, count=3)
            layer_inputs, layer_activation, layer_outputs = layer_topology
            offset += 3
            weights = np.frombuffer(buf, dtype=np.float32, offset=offset, count=layer_inputs * layer_outputs)
            offset += layer_inputs * layer_outputs
            biases = np.frombuffer(buf, dtype=np.float32, offset=offset, count=layer_outputs)
            offset += layer_outputs
            layers.append(Layer(layer_inputs, layer_outputs, layer_activation))
            layers[-1].set_weights(np.concatenate([weights, biases]))
        return Network(inputs, outputs, layers)

    def get_moves(self, game_state: str) -> list:
        # implement get_moves logic here
        pass