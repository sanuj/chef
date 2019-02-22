# Chef


Installing dependencies.
```
python3 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
python -m spacy download en
```
If you encounter problems with installation, look at [TextWorld](https://github.com/Microsoft/TextWorld).

Running sample `lstm-dqn` code:
```
cd sample_submissions/lstm-dqn
python train.py ../../sample_games/*.ulx
```
Models will be saved in `sample_submissions/lstm-dqn/saved_models`.

## Data

Download and split training data.
```
wget https://competitions.codalab.org/my/datasets/download/4353feda-a5f7-406a-b49e-aab0b94dd3a8
unzip 4353feda-a5f7-406a-b49e-aab0b94dd3a8
python data/split-train.py train data
```
