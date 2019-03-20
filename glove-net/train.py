import os
import glob
import argparse

from tqdm import tqdm

import gym
import textworld.gym
from textworld import EnvInfos

from custom_agent import CustomAgent

import visdom

# List of additional information available during evaluation.
AVAILABLE_INFORMATION = EnvInfos(
    description=True, inventory=True,
    max_score=True, objective=True, entities=True, verbs=True,
    command_templates=True, admissible_commands=True,
    has_won=True, has_lost=True,
    extras=["recipe"]
)


def _validate_requested_infos(infos: EnvInfos):
    msg = "The following information cannot be requested: {}"
    for key in infos.basics:
        if not getattr(AVAILABLE_INFORMATION, key):
            raise ValueError(msg.format(key))

    for key in infos.extras:
        if key not in AVAILABLE_INFORMATION.extras:
            raise ValueError(msg.format(key))


def train(game_files, visualize):
    if visualize:
        viz = visdom.Visdom()
        win = None

    agent = CustomAgent()
    requested_infos = agent.select_additional_infos()
    _validate_requested_infos(requested_infos)

    env_id = textworld.gym.register_games(game_files, requested_infos,
                                          max_episode_steps=agent.max_nb_steps_per_episode,
                                          name="training")
    env_id = textworld.gym.make_batch(env_id, batch_size=agent.batch_size, parallel=True)
    env = gym.make(env_id)

    for epoch_no in range(1, agent.nb_epochs + 1):
        stats = {
            "scores": [],
            "steps": [],
        }
        total_max_score = 0
        for game_no in tqdm(range(len(game_files))):
            obs, infos = env.reset()
            agent.train()

            scores = [0] * len(obs)
            dones = [False] * len(obs)
            steps = [0] * len(obs)
            while not all(dones):
                # Increase step counts.
                steps = [step + int(not done) for step, done in zip(steps, dones)]
                commands = agent.act(obs, scores, dones, infos)
                obs, scores, dones, infos = env.step(commands)

            # Let the agent knows the game is done.
            agent.act(obs, scores, dones, infos)
            total_max_score += infos["max_score"][0]

            stats["scores"].extend(scores)
            stats["steps"].extend(steps)

        score = sum(stats["scores"]) / agent.batch_size
        steps = sum(stats["steps"]) / agent.batch_size
        print("Epoch: {:3d} | {:2.1f} / {:2.1f} pts | {:4.1f} steps".format(epoch_no, score, total_max_score, steps))
        print("# of episodes: {}, epsilon: {}".format(agent.current_episode, agent.epsilon))
        if visualize:
            if win:
                viz.line(Y=[[score, steps]], X=[epoch_no], win=win, update='append')
            else:
                win = viz.line(Y=[[score, steps]], X=[epoch_no], opts=dict(showlegend=True, legend=['score', 'steps'], xlabel='epoch'))
            viz.save(viz.get_env_list())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train an agent.")
    parser.add_argument("games", metavar="game", nargs="+",
                       help="List of games (or folders containing games) to use for training.")
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()

    games = []
    for game in args.games:
        if os.path.isdir(game):
            games += glob.glob(os.path.join(game, "*.ulx"))
        else:
            games.append(game)

    print("{} games found for training.".format(len(games)))
    train(games, args.visualize)