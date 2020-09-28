import time
import gym
import pickle
import numpy as np




env = gym.make('FrozenLake-v0')
env = gym.wrappers.Monitor( env ,"recording", force = True )



print("Action space is {} ".format(env.action_space))
print("Observation space is {} ".format(env.observation_space))
print("Reward range is {} ".format(env.reward_range))

# Environment reset
obs = env.reset()
t, total_reward, done = 0, 0, False
max_steps = 100

# Render the environment
env.render()
print('')
time.sleep(0.1)

while t < max_steps:
    # Get random action (this is the implementation of the agent)
    action = env.action_space.sample()

    # Execute action and get response
    obs, reward, done, info = env.step(action)

    # Render the environment
    env.render()
    print('')

    t += 1
    if done:
        break
    time.sleep(0.1)

print("Episode finished after {} timesteps and reward was {} ".format(t, reward))
env.close()
env.env.close()