import gym
import gfootball  # Required as envs registered on import

simple_env = gym.make("GFootball-11_vs_11_kaggle-simple115v2-v0")
pixels_env = gym.make("GFootball-11_vs_11_kaggle-Pixels-v0")

print(f"simple115v2:\n {simple_env.__str__()}\n")
print(f"Pixels:\n {pixels_env.__str__()}\n")
print(f"SMM:\n {smm_env.__str__()}\n")


from gfootball.env.football_env import FootballEnv

env_name = "GFootballBase-v0"
gym.envs.register(id=env_name,
                  entry_point="gfootball.env.football_env:FootballEnv",
                  max_episode_steps=10000)

from gfootball.env.config import Config

base_env = gym.make(env_name, config=Config())

obs = base_env.reset()

print('ggg')