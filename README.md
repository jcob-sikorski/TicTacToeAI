# Tic Tac Toe AI Game

This is an implementation of the classic game of Tic Tac Toe, with an AI opponent. The game is played in a 3x3 grid, and the goal is to get three symbols in a row, column, or diagonal.

The AI opponent is implemented using the Q-learning algorithm, which allows it to learn from experience and make smarter decisions over time.

## Dependencies

This implementation requires the following dependencies:

- numpy
- pygame
- time

## How to Play

To play the game, simply run the tictactoe.py script. This will start the game and display the game board.

To make a move, click on one of the empty cells on the board. The game will then update with the AI opponent making a move. The game continues until one player wins or the board is full.

## Q-learning Algorithm

The Q-learning algorithm is a type of reinforcement learning algorithm that allows an agent to learn an optimal policy by exploring the environment and receiving rewards. In this implementation, the Q-table is updated after each move using the following equation:

```Q(s, a) = Q(s, a) * (1 - learning_rate) + learning_rate * (reward + discount_rate * max(Q(s', a')))```

Where:

Q(s, a) is the Q-value for the current state-action pair
- s is the current state
- a is the action taken in the current state
- s' is the new state after taking the action a
- learning rate determines the weight given to new information
- discount_rate is the discount rate, which determines the weight given to future rewards
The AI opponent uses an exploration-exploitation trade-off to balance between exploring new actions and exploiting the Q-values it has learned. The exploration rate starts high and decreases over time as the agent becomes more confident in its actions.
