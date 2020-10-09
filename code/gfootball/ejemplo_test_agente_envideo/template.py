from kaggle_environments.envs.football.helpers import *
@human_readable_agent
def agent(obs):
    if Action.Sprint not in obs['sticky_actions']:
        return Action.Sprint
    controlled_player_pos = obs['left_team'][obs['active']]
    if obs['ball_owned_player'] == obs['active'] and obs['ball_owned_team'] == 0:
        if controlled_player_pos[0] > 0.5:
            return Action.Shot
        return Action.Right
    else:
        if obs['ball'][0] > controlled_player_pos[0] + 0.05:
            return Action.Right
        if obs['ball'][0] < controlled_player_pos[0] - 0.05:
            return Action.Left
        if obs['ball'][1] > controlled_player_pos[1] + 0.05:
            return Action.Bottom
        if obs['ball'][1] < controlled_player_pos[1] - 0.05:
            return Action.Top
        return Action.Slide