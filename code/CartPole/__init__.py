import gym
import numpy as np

#creamos una estancia
env = gym.make('CartPole-v0')
env = gym.wrappers.Monitor( env ,"recording", force = True )

#dimensiones del espacio
print("Action space is {} ".format(env.action_space))
print("Observation space is {} ".format(env.observation_space))
print("Reward range is {} ".format(env.reward_range))



# Environment reset
obs = env.reset()
#inicializamos las variables
t, total_reward, done = 0, 0, False


#ejecutamos el juego
while not done:
    # Render the environment
    env.render()

    # Get random action (this is the implementation of the agent)
    action = env.action_space.sample()

    # Execute action and get response
    new_obs, reward, done, info = env.step(action)
    print("Obs: {} -> Action: {} and reward: {}".format(np.round(obs, 3), action, reward))

    obs = new_obs
    total_reward += reward
    t += 1

total_reward += reward
t += 1
print("Obs: {} -> Action: {} and reward: {}".format(np.round(obs, 3), action, reward))

print("Episode finished after {} timesteps and reward was {} ".format(t, total_reward))
env.close()
