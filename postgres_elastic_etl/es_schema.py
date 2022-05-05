import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'data/movies_index.json'), 'r') as movies_index_content:
    MOVIES_INDEX = json.load(movies_index_content)

with open(os.path.join(BASE_DIR, 'data/persons_index.json'), 'r') as persons_index_content:
    PERSONS_INDEX = json.load(persons_index_content)

with open(os.path.join(BASE_DIR, 'data/genres_index.json'), 'r') as genres_index_content:
    GENRES_INDEX = json.load(genres_index_content)
