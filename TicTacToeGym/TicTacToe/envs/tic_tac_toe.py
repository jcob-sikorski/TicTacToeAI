import numpy as np
import gymnasium as gym
from numpy import random


class TicTacToeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None, size=3):
        super().__init__()
        
        self.size = size  # The size of the square grid
        self.window_size = 512  # The size of the PyGame window

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.empty_symbol = 0
        self.player_symbol = 1
        self.agent_symbol = 2

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
    

    def reset(self):
        # We need the following line to seed self.np_random
        super().reset()

        self.board = np.array([self.empty_symbol for _ in range(9)])

        # Randomly choose who goes first
        self.current_player = random.choice([self.player_symbol, self.agent_symbol])

        return self.board
    

    def _check_for_winner(self):
        # check rows
        for row in [0, 3, 6]:
            if (self.board[row] == self.board[row+1] == self.board[row+2] != self.empty_symbol):
                return self.board[row]

        # check columns
        for col in [0, 1, 2]:
            if (self.board[col] == self.board[col+3] == self.board[col+6] != self.empty_symbol):
                return self.board[col]

        # check diagonals
        if (self.board[0] == self.board[4] == self.board[8] != self.empty_symbol):
            return self.board[0]

        if (self.board[2] == self.board[4] == self.board[6] != self.empty_symbol):
            return self.board[2]

        for cell in self.board:
            if cell == self.empty_symbol:
                return self.empty_symbol # game is still in progress
        return "tie"


    def step(self, action):
        self.board[action] = self.current_player

        # Check if the game has ended
        winner = self._check_for_winner()
        if winner != self.empty_symbol and winner != "tie":
            # If agent has won, return a reward of 10 or -10 depending on the winner
            return self.board, 10 if winner == self.agent_symbol else -10, True

        # Check if the board is full (i.e. a tie)
        if winner == "tie":
            # If the board is full and no winner, return a reward of 0 and terminate the episode
            return self.board, 0, True

        # If the game is still ongoing, switch to the other player
        self.current_player = self.agent_symbol if self.current_player == self.player_symbol else self.player_symbol

        return self.board, 0, False