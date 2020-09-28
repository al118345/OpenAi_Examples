import time
import gym
import pickle
import numpy as np

epsilon = 0.9
num_episodes = 100000
max_steps = 100

learning_rate = 0.81
gamma = 0.96

env = gym.make('FrozenLake-v0')

Q = np.zeros((env.observation_space.n, env.action_space.n))
print(Q)


def choose_action(state):
    action = 0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])
    return action


def learn(state, new_state, reward, action):
    predict = Q[state, action]
    target = reward + gamma * np.max(Q[new_state, :])
    Q[state, action] = Q[state, action] + learning_rate * (target - predict)

def choose_action_max(state):
    action = np.argmax(Q[state, :])
    return action



num_episodes = 1000
total_reward = 0
num_shows = 5
show_episode = False

# start
for episode in range(num_episodes):

    if (num_episodes - episode) <= num_shows:
        show_episode = True

    state = env.reset()

    if show_episode == True:
        print('')
        print('')
        print("*** Episode: ", episode + 1)
        print('')
        print('')
        time.sleep(0.8)
        env.render()

    t = 0
    while t < 100:
        action = choose_action_max(state)
        state, reward, done, info = env.step(action)

        if show_episode == True:
            time.sleep(0.5)
            env.render()
        if done:
            break

    if show_episode == True:
        time.sleep(0.8)
        print('')
        print('')
        print('Reward = {}'.format(reward))
        print('')
        print('')
        time.sleep(0.8)

    total_reward += reward

success_rate = total_reward * 100 / num_episodes
print("{} successes in {} episodes: {} % of success".format(total_reward, num_episodes, success_rate))