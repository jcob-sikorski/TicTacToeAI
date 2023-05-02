import numpy as np
import random
from TicTacToe.envs import TicTacToeEnv


# create an instance of the TicTacToeEnv environment
env = TicTacToeEnv(render_mode="human")

import numpy as np

# holds all possible states in the TicTacToe ~19500
states_matrix = np.zeros((3**9, 9))

for i in range(3**9):
     c = i
     for j in range(9):
       states_matrix[i][j] = c % 3
       c //= 3

# each state has available actions - each action from each state has a reward
q_table = {}

actions = list(range(9))

# update the q_table
for i in range(states_matrix.shape[0]):
    state = ''.join(map(str, [int(j) for j in states_matrix[i]]))
    q_table[state] = np.zeros(len(actions))


num_episodes = 20000
max_steps_per_episode = 10

learning_rate = 0.008
discount_rate = 0.92

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.35
exploration_decay_rate = 0.07


import random

rewards_all_episodes = []

# Q-learning algorithm
for episode in range(num_episodes):

    # reset the environment and initialize the state
    state = ''.join(env.reset().astype(str))

    rewards_current_episode = 0
    
    # play the episode
    for step in range(max_steps_per_episode):
        available_actions = [index for index, value in enumerate(state) if int(value) == env.empty_symbol]
        if env.current_player == env.player_symbol:
            action = random.choice(available_actions)
        else:
            # Exploration-exploitation trade-off
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > exploration_rate:
                action = available_actions[np.argmax(q_table[state][available_actions])]
            else:
                action = random.choice(available_actions)

        
        # change state, collect reward
        new_state, reward, done = env.step(action)
        new_state = ''.join(new_state.astype(str))
        
        # Update Q-table for Q(s, a)
        q_table[state][action] = q_table[state][action] * (1-learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state]))
    
        # go to a new location
        state = new_state
        rewards_current_episode += reward
    
        if done == True:
            break

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    
    rewards_all_episodes.append(rewards_current_episode)

    
# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000
print("********Average reward per thousand epiosodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000


import pygame
import time


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((500, 500))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the fonts
font = pygame.font.Font(None, 60)
win_font = pygame.font.Font('Press_Start_2P/PressStart2P-Regular.ttf', 60)


# Set up the game loop
running = True
# reset the environment and initialize the state
state = ''.join(env.reset().astype(str))
while running:
    # Handle events
    for event in pygame.event.get():
        available_actions = [index for index, value in enumerate(state) if int(value) == env.empty_symbol]

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            x, y = pygame.mouse.get_pos()

            # Determine which cell was clicked
            action = x // 166 + (y // 166)*3

            # change state, collect reward
            new_state, _, done = env.step(action)
            state = ''.join(new_state.astype(str))

            # Draw the Tic Tac Toe board
            screen.fill(WHITE)
            for row in range(3):
                for col in range(3):
                    rect_x = col * 166 # Calculate the x position of the rectangle
                    rect_y = row * 166 # Calculate the y position of the rectangle
                    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, 166, 166), 1) # Draw the rectangle
                    text = font.render(state[col+row*3], True, BLACK)
                    text_width, text_height = text.get_size()
                    text_x = rect_x + (166 - text_width) // 2 # Calculate the x position of the text
                    text_y = rect_y + (166 - text_height) // 2 # Calculate the y position of the text
                    screen.blit(text, (text_x, text_y)) # Draw the text

            # Update the display
            pygame.display.update()

            time.sleep(0.6)

            if done:
                running = False
                win_surface = win_font.render('O WON!', True, BLACK)
                screen.blit(win_surface, (100, 166))
                # Update the display
                pygame.display.update()
                # Quit Pygame
                pygame.quit()
                # close the environment
                env.close()
                break

            available_actions = [index for index, value in enumerate(state) if int(value) == env.empty_symbol]

            action = available_actions[np.argmax(q_table[state][available_actions])]
            new_state, _, done = env.step(action)
            state = ''.join(new_state.astype(str))

            if done:
                running = False
                win_surface = win_font.render('X WON!', True, BLACK)
                screen.blit(win_surface, (100, 166))
                # Update the display
                pygame.display.update()
                # Quit Pygame
                pygame.quit()
                # close the environment
                env.close()
                break

            # Draw the Tic Tac Toe board
            screen.fill(WHITE)
            for row in range(3):
                for col in range(3):
                    rect_x = col * 166 # Calculate the x position of the rectangle
                    rect_y = row * 166 # Calculate the y position of the rectangle
                    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, 166, 166), 1) # Draw the rectangle
                    text = font.render(state[col+row*3], True, BLACK)
                    text_width, text_height = text.get_size()
                    text_x = rect_x + (166 - text_width) // 2 # Calculate the x position of the text
                    text_y = rect_y + (166 - text_height) // 2 # Calculate the y position of the text
                    screen.blit(text, (text_x, text_y)) # Draw the text
            
            # Update the display
            pygame.display.update()