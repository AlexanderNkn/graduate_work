import pytest

from assistant_api.src.services.intent import get_intent, ParsedQuery


@pytest.mark.parametrize(
    'query,expected', [
        (
            'Кто был режиссером фильма девчата',
            ParsedQuery(intent='director_search', params={'title': 'девчата'})
        ),
        (
            'Кто режиссер фильма девчата',
            ParsedQuery(intent='director_search', params={'title': 'девчата'})
        ),
        (
            'Назови режиссера фильма девчата',
            ParsedQuery(intent='director_search', params={'title': 'девчата'})
        ),
        (
            'Кто режиссер зеленой мили',
            ParsedQuery(intent='director_search', params={'title': 'зеленый миля'})
        ),
        (
            'Кто снял зеленую милю',
            ParsedQuery(intent='director_search', params={'title': 'зеленый миля'})
        ),
    ],
)
def test_director_by_film(query, expected):
    assert get_intent(query) == expected, 'director intent should be available'


@pytest.mark.parametrize(
    'query,expected', [
        (
            'Кто сценарист зеленой мили',
            ParsedQuery(intent='writer_search', params={'title': 'зеленый миля'})
        ),
        (
            'Кто автор сценария зеленой мили',
            ParsedQuery(intent='writer_search', params={'title': 'зеленый миля'})
        ),
        (
            'Кто написал сценарий зеленой мили',
            ParsedQuery(intent='writer_search', params={'title': 'зеленый миля'})
        ),
    ],
)
def test_writer_by_film(query, expected):
    assert get_intent(query) == expected, 'writer intent should be available'


@pytest.mark.parametrize(
    'query,expected', [
        (
            'Кто снимался в зеленой миле',
            ParsedQuery(intent='actor_search', params={'title': 'в зеленый миля'})
        ),
        (
            'Назови актеров фильма зеленая миля',
            ParsedQuery(intent='actor_search', params={'title': 'зеленый миля'})
        ),
    ],
)
def test_actor_by_film(query, expected):
    assert get_intent(query) == expected, 'actor intent should be available'


@pytest.mark.parametrize(
    'query,expected', [
        (
            'Какая длительность фильма зеленая миля',
            ParsedQuery(intent='duration_search', params={'title': 'зеленый миля'})
        ),
        (
            'Сколько длится фильма зеленая миля',
            ParsedQuery(intent='duration_search', params={'title': 'зеленый миля'})
        ),
        (
            'Какая продолжительность фильма зеленая миля',
            ParsedQuery(intent='duration_search', params={'title': 'зеленый миля'})
        ),
    ],
)
def test_duration_by_film(query, expected):
    assert get_intent(query) == expected, 'duration intent should be available'


def test_film_by_director():
    assert get_intent('Какие фильмы снял Спилберг') == ParsedQuery(
        intent='film_by_person', params={'directors_names': 'спилберг'}
    )


def test_film_by_writer():
    assert get_intent('Для каких фильмов написал сценарий Марио Пьюзо') == ParsedQuery(
        intent='film_by_person', params={'writers_names': 'марио пьюзо'}
    )


@pytest.mark.parametrize(
    'query,expected', [
        (
            'В каких фильмах снимался Джони Депп',
            ParsedQuery(intent='film_by_person', params={'actors_names': 'джони депп'})
        ),
        (
            'Где снимался Джони Депп',
            ParsedQuery(intent='film_by_person', params={'actors_names': 'джони депп'})
        ),
    ],
)
def test_film_by_actor(query, expected):
    assert get_intent(query) == expected, 'film by person intent should be available'


@pytest.mark.parametrize(
    'query,expected', [
        (
            'Назови режиссера зеленой мили',
            ParsedQuery(intent='director_search', params={'title': 'зеленый миля'})
        ),
        (
            'Скажи кто режиссер зеленой мили',
            ParsedQuery(intent='director_search', params={'title': 'зеленый миля'})
        ),
        (
            'Покажи режиссера зеленой мили',
            ParsedQuery(intent='director_search', params={'title': 'зеленый миля'})
        ),
        (
            'Покажи режиссера фильма покажи мне отца',
            ParsedQuery(intent='director_search', params={'title': 'показывать я отец'})
        ),
    ],
)
def test_intro_word_reduce(query, expected):
    assert get_intent(query) == expected, 'director intent should be available in sentence with intro word'
