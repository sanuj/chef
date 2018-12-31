# Chef


Installing dependencies.
```
python3 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
If you encounter problems with installation, look at [TextWorld](https://github.com/Microsoft/TextWorld).

Running sample `lstm-dqn` code:
```
cd sample_submissions/lstm-dqn
python train.py ../../sample_games/*.ulx
```
Models will be saved in `sample_submissions/lstm-dqn/saved_models`.
