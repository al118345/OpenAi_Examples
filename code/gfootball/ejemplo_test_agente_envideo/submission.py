from kaggle_environments.envs.football.helpers import *
from random import random, choice

memory = []


@human_readable_agent
def agent(obs):
    # Execute memorized actions
    global memory
    if memory:
        return memory.pop(0)

    # Execute a sequence of actions
    def do_actions(sequence):
        global memory
        memory = sequence[1:]
        return sequence[0]

    # Evaluate distance between two objects (euclidian or manatthan)
    def get_distance(pos1, pos2, euclidian=False):
        if euclidian:
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** (
            1 / 2)
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # Find colser opponent distance (euclidian or manatthan)
    def get_closer_opponent_dist(euclidian=False):
        closer_opponent_dist = 5
        for opponent_pos in obs['right_team']:
            closer_opponent_dist = min(
                get_distance(controlled_player_pos, opponent_pos, euclidian),
                closer_opponent_dist)
        return closer_opponent_dist

    # Return T/F based on probability
    def do_it(probability):
        return random() < probability

    # Conditioned probability multiplier
    def rev_prob(probability):
        return 1 / (1 - probability)

    controlled_player_pos = obs['left_team'][obs['active']]

    # Check current mode
    # Kickoff strategy: short pass to mate
    if obs['game_mode'] == GameMode.KickOff:
        return do_actions(
            [Action.Top if controlled_player_pos[1] > 0 else Action.Bottom,
             Action.ShortPass])
    # Penalty strategy: make a shot
    if obs['game_mode'] == GameMode.Penalty:
        return do_actions(
            [choice([Action.TopRight, Action.BottomRight, Action.Right]),
             Action.Shot])
    # Goalkick strategy: pass to front
    if obs['game_mode'] == GameMode.GoalKick:
        return do_actions(
            [choice([Action.TopRight, Action.BottomRight, Action.Right]),
             choice([Action.ShortPass, Action.LongPass, Action.HighPass])])
    # Freekick strategy: make shot when close to goal, high pass when in back field, and short pass in mid field
    if obs['game_mode'] == GameMode.FreeKick:
        if controlled_player_pos[0] > 0.5:  # Near goal Shot or Cross
            action = [Action.Shot]
            if abs(controlled_player_pos[1]) < 0.1:
                action.insert(0, Action.Right)
            elif abs(controlled_player_pos[1]) < 0.3:
                action.insert(0, Action.TopRight if controlled_player_pos[
                                                        1] > 0 else Action.BottomRight)
            else:
                action = [Action.HighPass]
                action.insert(0, Action.Top if controlled_player_pos[
                                                   1] > 0 else Action.Bottom)

        elif controlled_player_pos[0] < 0:  # Back side longpass to front
            action = [choice([Action.LongPass, Action.HighPass])]
            if abs(controlled_player_pos[1]) < 0.3:
                action.insert(0, Action.Right)
            else:
                action.insert(0, Action.TopRight if controlled_player_pos[
                                                        1] > 0 else Action.BottomRight)

        else:  # MidField pass to front
            action = [Action.ShortPass]
            if abs(controlled_player_pos[1]) < 0.3:
                action.insert(0, Action.Right)
            action.insert(0, Action.TopRight if controlled_player_pos[
                                                    1] > 0 else Action.BottomRight)

        return do_actions(action)
    # Corner strategy: high pass to goal area
    if obs['game_mode'] == GameMode.Corner:
        return do_actions(
            [Action.Top if controlled_player_pos[1] > 0 else Action.Bottom,
             Action.HighPass])
    # Throwin strategy: short pass into field
    if obs['game_mode'] == GameMode.ThrowIn:
        return do_actions([choice([Action.Top, Action.TopRight]) if
                           controlled_player_pos[1] > 0 else choice(
            [Action.Bottom, Action.BottomRight]), Action.ShortPass])
    # Normal Play
    if obs['ball_owned_player'] == obs['active'] and obs[
        'ball_owned_team'] == 0:  # We have the ball

        def_keeper_pos = obs['right_team'][0]

        # Shot if we are close to the goal or the goalkeeper is coming, cross if near out
        if controlled_player_pos[0] > 0.6 or (
                def_keeper_pos[0] < 0.7 and controlled_player_pos[0] > 0.4):
            action = [Action.Shot]
            if abs(controlled_player_pos[1]) < 0.1:
                action.insert(0, Action.Right)
            elif abs(controlled_player_pos[1]) < 0.3:
                action.insert(0, Action.TopRight if controlled_player_pos[
                                                        1] > 0 else Action.BottomRight)
            elif controlled_player_pos[0] < 0.85:
                return Action.Right
            else:
                action = [Action.HighPass]
                action.insert(0, Action.Top if controlled_player_pos[
                                                   1] > 0 else Action.Bottom)
            return do_actions(action)

        # Make sure player is running and dribbling.
        if Action.Sprint not in obs['sticky_actions']:
            return Action.Sprint
        if Action.Dribble not in obs['sticky_actions']:
            return Action.Dribble

        # Run towards the goal otherwise.
        # randomly: Right(80%), ShortPass(10%), TopRight(5%), BottomRight(5%)
        if do_it(0.8 * rev_prob(0)):
            return Action.Right
        if do_it(0.1 * rev_prob(0.8)):
            return Action.ShortPass
        if do_it(0.1 * rev_prob(0.9)):
            return choice([Action.TopRight, Action.BottomRight])

    # We not have ball
    # Make sure player is running and not dribbling.
    if Action.Sprint not in obs['sticky_actions']:
        return Action.Sprint
    if Action.Dribble in obs['sticky_actions']:
        return Action.ReleaseDribble

    if obs['ball_owned_team'] == 1:  # Opponents have ball

        # Run towards the ball but not to right.
        if obs['ball'][0] > controlled_player_pos[0] + 0.05:
            if obs['ball'][1] > controlled_player_pos[1] + 0.05:
                if obs['ball'][0] > controlled_player_pos[0] + 0.2:
                    return Action.Bottom
                return Action.BottomLeft
            if obs['ball'][1] < controlled_player_pos[1] - 0.05:
                if obs['ball'][0] > controlled_player_pos[0] + 0.2:
                    return Action.Top
                return Action.TopLeft
            return Action.Right
        if obs['ball'][0] < controlled_player_pos[0] + 0.05:
            if obs['ball'][1] > controlled_player_pos[1] + 0.05:
                return Action.BottomLeft
            if obs['ball'][1] < controlled_player_pos[1] - 0.05:
                return Action.TopLeft
            return Action.Left
        # Try to take over the ball if close to the ball and opponent is not between.
        if get_distance(controlled_player_pos,
                        obs['ball']) < get_closer_opponent_dist():
            action = [Action.Slide]
            if controlled_player_pos[0] - obs['ball'][0] < -0.01:
                if controlled_player_pos[1] - obs['ball'][1] < -0.01:
                    action.insert(0, Action.BottomRight)
                elif controlled_player_pos[1] - obs['ball'][1] > 0.01:
                    action.insert(0, Action.TopRight)
                else:
                    action.insert(0, Action.Right)
            elif controlled_player_pos[0] - obs['ball'][0] > 0.01:
                if controlled_player_pos[1] - obs['ball'][1] < -0.01:
                    action.insert(0, Action.BottomLeft)
                elif controlled_player_pos[1] - obs['ball'][1] > 0.01:
                    action.insert(0, Action.TopLeft)
                else:
                    action.insert(0, Action.Left)
            else:
                if controlled_player_pos[1] - obs['ball'][1] < -0.01:
                    action.insert(0, Action.Bottom)
                elif controlled_player_pos[1] - obs['ball'][1] > 0.01:
                    action.insert(0, Action.Top)
            return do_actions(action)

    # None have ball
    # Run towards the ball.
    if obs['ball'][0] > controlled_player_pos[0] + 0.05:
        if obs['ball'][1] > controlled_player_pos[1] + 0.05:
            return Action.BottomRight
        if obs['ball'][1] < controlled_player_pos[1] - 0.05:
            return Action.TopRight
        return Action.Right
    if obs['ball'][0] < controlled_player_pos[0] + 0.05:
        if obs['ball'][1] > controlled_player_pos[1] + 0.05:
            return Action.BottomLeft
        if obs['ball'][1] < controlled_player_pos[1] - 0.05:
            return Action.TopLeft
        return Action.Left
    return Action.Idle