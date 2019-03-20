#!/usr/bin/env python
import json
import logging
from tqdm import tqdm
from embeddings import GloveEmbedding, KazumaCharEmbedding


if __name__ == '__main__':
    with open("./vocab.txt") as f:
        word_vocab = f.read().split("\n")

    logging.warn('Computing word embeddings')
    embeddings = [GloveEmbedding(), KazumaCharEmbedding()]
    E = []
    for w in tqdm(word_vocab):
        e = []
        for emb in embeddings:
            e += emb.emb(w, default='zero')
        E.append(e)
    with open('emb.json', 'wt') as f:
        json.dump(E, f)
