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
            "actors_names": ["David Mallet", "Robert Elms"],
            "writers_names": [],
            "directors_names": [],
            "actors": [
                {
                    "id": "22345678-1234-1234-1234-123456789103",
                    "name": "David Mallet"
                },
                {
                    "id": "22345678-1234-1234-1234-123456789106",
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
            "actors_names": ["Alex Kurtzman", "Robert Elms"],
            "writers_names": ["Chris Pine"],
            "directors_names": ["David Tomaszewski"],
            "actors": [
                {
                    "id": "22345678-1234-1234-1234-123456789104",
                    "name": "Alex Kurtzman"
                },
                {
                    "id": "22345678-1234-1234-1234-123456789106",
                    "name": "Robert Elms"
                }
            ],
            "writers": [
                {
                    "id": "22345678-1234-1234-1234-123456789105",
                    "name": "Chris Pine"
                },
            ],
            "directors": [
                {
                    "id": "22345678-1234-1234-1234-123456789102",
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
            "actors_names": ["Chris Weitz"],
            "writers_names": ["Chris Pine"],
            "directors_names": ["David Tomaszewski"],
            "actors": [
                {
                    "id": "22345678-1234-1234-1234-123456789101",
                    "name": "Chris Weitz"
                }
            ],
            "writers": [
                {
                    "id": "22345678-1234-1234-1234-123456789105",
                    "name": "Chris Pine"
                },
            ],
            "directors": [
                {
                    "id": "22345678-1234-1234-1234-123456789102",
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
            "actors_names": ["Alex Kurtzman", "Robert Elms"],
            "writers_names": ["Chris Pine"],
            "directors_names": [],
            "actors": [
                {
                    "id": "22345678-1234-1234-1234-123456789104",
                    "name": "Alex Kurtzman"
                },
                {
                    "id": "22345678-1234-1234-1234-123456789106",
                    "name": "Robert Elms"
                }
            ],
            "writers": [
                {
                    "id": "22345678-1234-1234-1234-123456789105",
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
                "uuid": "22345678-1234-1234-1234-123456789103",
                "full_name": "David Mallet"
            },
            {
                "uuid": "22345678-1234-1234-1234-123456789106",
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
