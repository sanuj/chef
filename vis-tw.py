from glob import glob
from os.path import join as pjoin

GAMES_PATH = "sample_games"
gamefiles = glob(pjoin(GAMES_PATH, "*.ulx"))
print("Found {} games.".format(len(gamefiles)))

print("Choose a game from below:")
for i, g in enumerate(gamefiles):
	print("[{}]: {}".format(i, g))

game_i = int(input('> '))

gamefile = gamefiles[game_i]  # Pick a game.

import textworld
game = textworld.Game.load(gamefile.replace(".ulx", ".json"))
textworld.render.visualize(game, True)

input('> ')

