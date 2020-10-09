import matplotlib.pyplot as plt
import pprint
import glob
import imageio
import pathlib
import numpy as np
from typing import Tuple
from tqdm import tqdm
from IPython.display import Image

import gym
import gfootball  # Required as envs registered on import

simple_env = gym.make("GFootball-11_vs_11_kaggle-simple115v2-v0")
pixels_env = gym.make("GFootball-11_vs_11_kaggle-Pixels-v0")
smm_env = gym.make("GFootball-11_vs_11_kaggle-SMM-v0")

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

pprint.pprint(obs[0])


obs = simple_env.reset()

print(obs.shape)

pprint.pprint(obs)


def plot_smm_obs(obs: np.ndarray) -> Tuple[plt.Figure, plt.Axes]:
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    for i, (ax, title) in enumerate(
            zip(axs.flatten(), ['left team', 'right team',
                                'ball', 'active player'])):
        ax.imshow(obs[..., i], animated=True)
        ax.set_title(title)
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

    return fig, ax


def generate_gif(env: gym.Env, suffix: str = "smm_env/"):
    obs = env.reset()

    ims = []
    for s in tqdm(range(250)):
        obs, _, _, _ = env.step(5)
        fig, ax = plot_smm_obs(obs)
        fig.suptitle(f"Step: {s}")
        fig.tight_layout()
        fig.savefig(f'{suffix}{s}.png')
        plt.close('all')

    fns = glob.glob(f'{suffix}*.png')
    sorted_idx = np.argsort(
        [int(f.split(suffix)[1].split('.png')[0]) for f in fns])
    fns = np.array(fns)[sorted_idx]
    output_path = f"{suffix}replay.gif"
    images = [imageio.imread(f) for f in fns]
    imageio.mimsave(output_path, images,
                    duration=0.1,
                    subrectangles=True)


smm_env = gym.make("GFootball-11_vs_11_kaggle-SMM-v0")
print(smm_env.reset().shape)

pathlib.Path("smm_env/").mkdir(exist_ok=True)
generate_gif(smm_env, "smm_env/")

Image(filename=f"smm_env/replay.gif", format='png')

pixels_env.render()
obs = pixels_env.reset()