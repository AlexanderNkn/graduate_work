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
        {
            "_index": "movies",
            "_id": "12345678-1234-1234-1234-123456789102",
            "id": "12345678-1234-1234-1234-123456789102",
            "title": "film 2",
            "imdb_rating": 8.1,
            "description": "Movie for test 2",
            "genre": [
                {
                    "id": "5373d043-3f41-4ea8-9947-4b746c601bbd",
                    "name": "Comedy"
                }
            ],
            "actors": [
                {
                    "id": "82b7dffe-6254-4598-b6ef-5be747193946",
                    "name": "Alex Kurtzman"
                },
                {
                    "id": "ab77efeb-dc56-4452-bdd9-43d782e223f1",
                    "name": "Robert Elms"
                }
            ],
            "writers": [
                {
                    "id": "9f38323f-5912-40d2-a90c-b56899746f2a",
                    "name": "Chris Pine"
                },
            ],
            "directors": [
                {
                    "id": "41ac0f45-d12d-434a-81b4-3bb9c1ebd4e4",
                    "name": "David Tomaszewski"
                },
            ]
        },
        {
            "_index": "movies",
            "_id": "12345678-1234-1234-1234-123456789103",
            "id": "12345678-1234-1234-1234-123456789103",
            "title": "film 3",
            "imdb_rating": 6.5,
            "description": "Movie for test 3",
            "genre": [
                {
                    "id": "5373d043-3f41-4ea8-9947-4b746c601bbd",
                    "name": "Comedy"
                }
            ],
            "actors": [
                {
                    "id": "06d3686f-56e0-40df-81ea-af95a203b58a",
                    "name": "Chris Weitz"
                }
            ],
            "writers": [
                {
                    "id": "9f38323f-5912-40d2-a90c-b56899746f2a",
                    "name": "Chris Pine"
                },
            ],
            "directors": [
                {
                    "id": "41ac0f45-d12d-434a-81b4-3bb9c1ebd4e4",
                    "name": "David Tomaszewski"
                },
            ]
        },
        {
            "_index": "movies",
            "_id": "12345678-1234-1234-1234-123456789104",
            "id": "12345678-1234-1234-1234-123456789104",
            "title": "film 4",
            "imdb_rating": 4.7,
            "description": "Film for test 4",
            "genre": [
                {
                    "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                    "name": "Romance"
                }
            ],
            "actors": [
                {
                    "id": "82b7dffe-6254-4598-b6ef-5be747193946",
                    "name": "Alex Kurtzman"
                },
                {
                    "id": "ab77efeb-dc56-4452-bdd9-43d782e223f1",
                    "name": "Robert Elms"
                }
            ],
            "writers": [
                {
                    "id": "9f38323f-5912-40d2-a90c-b56899746f2a",
                    "name": "Chris Pine"
                },
            ],
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


@pytest.fixture
def film_list_expected():
    return [
        {
            "uuid": "12345678-1234-1234-1234-123456789101",
            "title": "Video Killed the Radio Star",
            "imdb_rating": 7,
        },
        {
            "uuid": "12345678-1234-1234-1234-123456789102",
            "title": "film 2",
            "imdb_rating": 8.1,
        },
        {
            "uuid": "12345678-1234-1234-1234-123456789103",
            "title": "film 3",
            "imdb_rating": 6.5,
        },
        {
            "uuid": "12345678-1234-1234-1234-123456789104",
            "title": "film 4",
            "imdb_rating": 4.7,
        },
    ]
