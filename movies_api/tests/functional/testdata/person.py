import pytest


@pytest.fixture
def person_list():
    return [
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789101",
            "id": "22345678-1234-1234-1234-123456789101",
            "full_name": "Chris Weitz",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789103"],
        },
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789102",
            "id": "22345678-1234-1234-1234-123456789102",
            "full_name": "David Tomaszewski",
            "role": ["director"],
            "film_ids": ["12345678-1234-1234-1234-123456789102", "12345678-1234-1234-1234-123456789103"],
        },
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789103",
            "id": "22345678-1234-1234-1234-123456789103",
            "full_name": "David Mallet",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789101"],
        },
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789104",
            "id": "22345678-1234-1234-1234-123456789104",
            "full_name": "Alex Kurtzman",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789102", "12345678-1234-1234-1234-123456789104"],
        },
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789105",
            "id": "22345678-1234-1234-1234-123456789105",
            "full_name": "Chris Pine",
            "role": ["writer"],
            "film_ids": [
                "12345678-1234-1234-1234-123456789102",
                "12345678-1234-1234-1234-123456789103",
                "12345678-1234-1234-1234-123456789104",
            ],
        },
        {
            "_index": "persons",
            "_id": "22345678-1234-1234-1234-123456789106",
            "id": "22345678-1234-1234-1234-123456789106",
            "full_name": "Robert Elms",
            "role": ["actor"],
            "film_ids": [
                "12345678-1234-1234-1234-123456789101",
                "12345678-1234-1234-1234-123456789102",
                "12345678-1234-1234-1234-123456789104",
            ],
        },
    ]


@pytest.fixture
def person_by_id_expected():
    return {
        "uuid": "22345678-1234-1234-1234-123456789101",
        "full_name": "Chris Weitz",
        "role": ["actor"],
        "film_ids": ["12345678-1234-1234-1234-123456789103"],
    }


@pytest.fixture
def person_list_expected():
    return [
        {
            "uuid": "22345678-1234-1234-1234-123456789101",
            "full_name": "Chris Weitz",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789103"],
        },
        {
            "uuid": "22345678-1234-1234-1234-123456789102",
            "full_name": "David Tomaszewski",
            "role": ["director"],
            "film_ids": ["12345678-1234-1234-1234-123456789102", "12345678-1234-1234-1234-123456789103"],
        },
        {
            "uuid": "22345678-1234-1234-1234-123456789103",
            "full_name": "David Mallet",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789101"],
        },
        {
            "uuid": "22345678-1234-1234-1234-123456789104",
            "full_name": "Alex Kurtzman",
            "role": ["actor"],
            "film_ids": ["12345678-1234-1234-1234-123456789102", "12345678-1234-1234-1234-123456789104"],
        },
        {
            "uuid": "22345678-1234-1234-1234-123456789105",
            "full_name": "Chris Pine",
            "role": ["writer"],
            "film_ids": [
                "12345678-1234-1234-1234-123456789102",
                "12345678-1234-1234-1234-123456789103",
                "12345678-1234-1234-1234-123456789104",
            ],
        },
        {
            "uuid": "22345678-1234-1234-1234-123456789106",
            "full_name": "Robert Elms",
            "role": ["actor"],
            "film_ids": [
                "12345678-1234-1234-1234-123456789101",
                "12345678-1234-1234-1234-123456789102",
                "12345678-1234-1234-1234-123456789104",
            ],
        },
    ]


@pytest.fixture
def film_list_expected():
    return [
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
    ]
