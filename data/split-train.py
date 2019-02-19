import argparse
import shutil
import os
import re

def main(src, dst):
    files = os.listdir(src)
    rgx = "(.*)-(\w+)\.(?:json|ulx|z8)"
    games = {}
    for f in files:
        typ, val = re.search(rgx, f).groups()
        if typ not in games:
            games[typ] = []
        games[typ].append(val)
    print("Total number of games: ", len(games.values()))
    print("Number of game types: ", len(games.keys()))
    print("Number of games in each type: ", len(games.values())/len(games.keys()))

    for i in range(20):
        cd = "train-"+str(i)
        os.mkdir(os.path.join(dst, cd))
        for k in games:
            for ex in ['.json', '.ulx', '.z8']:
                name = k + '-' + games[k][i] + ex
                shutil.copyfile(os.path.join(src, name), os.path.join(dst, cd, name))
        print(cd + " finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split train data files.')
    parser.add_argument('src_data_dir', type=str, help='location of training data dir')
    parser.add_argument('dst_data_dir', type=str, help='destination dir')

    args = parser.parse_args()
    main(args.src_data_dir, args.dst_data_dir)

