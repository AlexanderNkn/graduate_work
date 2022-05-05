import pytest


@pytest.fixture
def genre_list():
    return [
        {
            "_index": "genres",
            "_id": "32345678-1234-1234-1234-123456789101",
            "id": "32345678-1234-1234-1234-123456789101",
            "name": "Game-Show",
            "description": "Watch gaming.",
        },
        {
            "_index": "genres",
            "_id": "32345678-1234-1234-1234-123456789102",
            "id": "32345678-1234-1234-1234-123456789102",
            "name": "Talk-Show",
            "description": "Talking about all: politics, religion, science",
        },
        {
            "_index": "genres",
            "_id": "32345678-1234-1234-1234-123456789103",
            "id": "32345678-1234-1234-1234-123456789103",
            "name": "Science fiction",
            "description": "Advanced science and technology, space exploration, time travel, parallel universes, and extraterrestrial life.",
        },
    ]


@pytest.fixture
def genre_by_id_expected():
    return {
        "uuid": "32345678-1234-1234-1234-123456789101",
        "name": "Game-Show",
        "description": "Watch gaming.",
    }


@pytest.fixture
def genre_list_expected():
    return [
        {
            "uuid": "32345678-1234-1234-1234-123456789101",
            "name": "Game-Show",
            "description": "Watch gaming.",
        },
        {
            "uuid": "32345678-1234-1234-1234-123456789102",
            "name": "Talk-Show",
            "description": "Talking about all: politics, religion, science",
        },
        {
            "uuid": "32345678-1234-1234-1234-123456789103",
            "name": "Science fiction",
            "description": "Advanced science and technology, space exploration, time travel, parallel universes, and extraterrestrial life.",
        },
    ]
