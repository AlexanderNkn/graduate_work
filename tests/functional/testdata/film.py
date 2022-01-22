import pytest


@pytest.fixture
def film_list():
    return [
        {
            "_index": "movies",
            "_id": "12345678-1234-1234-1234-123456789101",
            "id": "12345678-1234-1234-1234-123456789101",
            "title": "Video Killed the Radio Star",
            "imdb_rating": 7,
            "description": "Featuring interviews with iconic bands and artists, such as Guns 'n' Roses, Fleetwood Mac, Metallica, A-Ha, Bon Jovi and Bryan Adams.",
            "genre": [
                {
                    "id": "6d141ad2-d407-4252-bda4-95590aaf062a",
                    "name": "Documentary"
                },
                {
                    "id": "56b541ab-4d66-4021-8708-397762bff2d4",
                    "name": "Music"
                }
            ],
            "actors": [
                {
                    "id": "589a55c7-d9b0-4f3f-862f-4f547f6218e8",
                    "name": "David Mallet"
                },
                {
                    "id": "ab77efeb-dc56-4452-bdd9-43d782e223f1",
                    "name": "Robert Elms"
                }
            ],
            "writers": [],
            "directors": []
        },
    ]


@pytest.fixture
def film_by_id_expected():
    return {
        "uuid": "12345678-1234-1234-1234-123456789101",
        "title": "Video Killed the Radio Star",
        "imdb_rating": 7,
        "description": "Featuring interviews with iconic bands and artists, such as Guns 'n' Roses, Fleetwood Mac, Metallica, A-Ha, Bon Jovi and Bryan Adams.",
        "genre": [
            {
                "uuid": "6d141ad2-d407-4252-bda4-95590aaf062a",
                "name": "Documentary"
            },
            {
                "uuid": "56b541ab-4d66-4021-8708-397762bff2d4",
                "name": "Music"
            }
        ],
        "actors": [
            {
                "uuid": "589a55c7-d9b0-4f3f-862f-4f547f6218e8",
                "full_name": "David Mallet"
            },
            {
                "uuid": "ab77efeb-dc56-4452-bdd9-43d782e223f1",
                "full_name": "Robert Elms"
            }
        ],
        "writers": [],
        "directors": []
    }
