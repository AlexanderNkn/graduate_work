from services.intent import get_intent, ParsedQuery


def test_director_by_film_1():
    assert get_intent('Кто был режиссером фильма девчата') == ParsedQuery(
        intent='director_search',
        params={'title': 'девчата'}
    )


def test_director_by_film_2():
    assert get_intent('Кто режиссер фильма девчата') == ParsedQuery(
        intent='director_search',
        params={'title': 'девчата'}
    )


def test_director_by_film_3():
    assert get_intent('Назови режиссера фильма девчата') == ParsedQuery(
        intent='director_search',
        params={'title': 'девчата'}
    )


def test_director_by_film_4():
    assert get_intent('Кто режиссер зеленой мили') == ParsedQuery(
        intent='director_search',
        params={'title': 'зеленый миля'}
    )


def test_director_by_film_5():
    assert get_intent('Кто снял зеленую милю') == ParsedQuery(
        intent='director_search',
        params={'title': 'зеленый миля'}
    )


def test_writer_by_film_1():
    assert get_intent('Кто сценарист зеленой мили') == ParsedQuery(
        intent='writer_search',
        params={'title': 'зеленый миля'}
    )


def test_writer_by_film_2():
    assert get_intent('Кто автор сценария зеленой мили') == ParsedQuery(
        intent='writer_search',
        params={'title': 'зеленый миля'}
    )


def test_writer_by_film_3():
    assert get_intent('Кто написал сценарий зеленой мили') == ParsedQuery(
        intent='writer_search',
        params={'title': 'зеленый миля'}
    )


def test_actor_by_film_1():
    assert get_intent('Кто снимался в зеленой миле') == ParsedQuery(
        intent='actor_search',
        params={'title': 'в зеленый миля'}
    )


def test_actor_by_film_2():
    assert get_intent('Назови актеров фильма зеленая миля') == ParsedQuery(
        intent='actor_search',
        params={'title': 'зеленый миля'}
    )


def test_duration_by_film_1():
    assert get_intent('Какая длительность фильма зеленая миля') == ParsedQuery(
        intent='duration_search',
        params={'title': 'зеленый миля'}
    )


def test_duration_by_film_2():
    assert get_intent('Сколько длится фильма зеленая миля') == ParsedQuery(
        intent='duration_search',
        params={'title': 'зеленый миля'}
    )


def test_duration_by_film_3():
    assert get_intent('Какая продолжительность фильма зеленая миля') == ParsedQuery(
        intent='duration_search',
        params={'title': 'зеленый миля'}
    )


def test_film_by_director_1():
    assert get_intent('Какие фильмы снял Спилберг') == ParsedQuery(
        intent='film_by_person',
        params={'directors_names': 'спилберг'}
    )


def test_film_by_writer_1():
    assert get_intent('Для каких фильмов написал сценарий Марио Пьюзо') == ParsedQuery(
        intent='film_by_person',
        params={'writers_names': 'марио пьюзо'}
    )


def test_film_by_actor_1():
    assert get_intent('В каких фильмах снимался Джони Депп') == ParsedQuery(
        intent='film_by_person',
        params={'actors_names': 'джони депп'}
    )


def test_film_by_actor_2():
    assert get_intent('Где снимался Джони Депп') == ParsedQuery(
        intent='film_by_person',
        params={'actors_names': 'джони депп'}
    )
