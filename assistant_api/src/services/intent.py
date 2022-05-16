from dataclasses import dataclass

from pymystem3 import Mystem

text_normalizer = Mystem()


@dataclass
class ParsedQuery:
    intent: str
    params: dict | None = None
    check_cache: bool = False


def get_word(lemma):
    if 'analysis' in lemma:
        return lemma['analysis'][0]['lex']
    return lemma['text']


def is_preposition(lemma):
    if 'analysis' in lemma:
        grammem = lemma['analysis'][0]['gr'].split('=')[0]
        return grammem == 'PR'
    return False


def is_movie_word(lemma):
    return get_word(lemma) == 'фильм'


def intro_word_count(words):
    intro_words = ['сказать', 'показывать', 'называть']
    word_num = 0
    while word_num < len(words):
        if words[word_num] in intro_words:
            word_num += 1
        else:
            break
    return word_num


def clear_movie_word(film_lemmas):
    if len(film_lemmas) > 0 and is_movie_word(film_lemmas[0]):
        film_lemmas = film_lemmas[1:]
    elif len(film_lemmas) > 1 and is_preposition(film_lemmas[0]) and is_movie_word(film_lemmas[1]):
        film_lemmas = film_lemmas[2:]
    return film_lemmas


def query_start_with_phrase(stemmed_query: str, start_phrases: list, goal_phrases: dict[str, str]):
    for start_phrase in start_phrases:
        if not stemmed_query.startswith(start_phrase):
            continue

        for phrase, phrases_type in goal_phrases.items():
            if start_phrase:
                search_phrase = f'{start_phrase} {phrase}'
            else:
                search_phrase = phrase

            if stemmed_query.startswith(search_phrase):
                phrase_words = len(search_phrase.split())

                return phrases_type, phrase_words

    return None, 0


def lemmas_to_sentence(lemmas):
    return ' '.join(get_word(lemma) for lemma in lemmas)


def get_intent(query: str) -> ParsedQuery | None:
    """Returns intent with params from given query.

    Example:
        from query 'Who+is+a+director+of+edge+of+tomorrow' returns
        {
            'intent': 'director_search',
            'params': {
                'title': 'edge of tomorrow',
            }
        }
    """
    lemmas = text_normalizer.analyze(query)
    lemmas = [lemma for lemma in lemmas if 'analysis' in lemma or lemma['text'].isdigit()]
    words = [get_word(lemma) for lemma in lemmas]

    word_num = intro_word_count(words)
    lemmas = lemmas[word_num:]

    stemmed_query = lemmas_to_sentence(lemmas)

    # TODO implement method to search query in cache
    # this block for testing only
    if stemmed_query == 'а кто там сниматься':
        return ParsedQuery(
            intent='actor_search',
            check_cache=True
        )

    person_phrases = {
        'режиссер': 'director',
        'сниматься': 'actor',
        'снять': 'director',
        'снимать': 'director',
        'актер': 'actor',
        'написать сценарий': 'writer',
        'создать сценарий': 'writer',
        'сценарист': 'writer',
        'автор сценарий': 'writer',
    }

    # find persons in movie
    start_phrases = ['кто быть', 'кто являться', 'кто', '']
    person_type, phrase_words = query_start_with_phrase(stemmed_query, start_phrases, person_phrases)
    if person_type:
        film_lemmas = lemmas[phrase_words:]
        film_lemmas = clear_movie_word(film_lemmas)
        film_title = lemmas_to_sentence(film_lemmas)

        return ParsedQuery(
            intent=f'{person_type}_search',
            params={'title': film_title}
        )

    # find movie by person
    start_phrases = ['что', 'где', 'какой фильм', 'в какой фильм', 'для какой фильм']
    person_type, phrase_words = query_start_with_phrase(stemmed_query, start_phrases, person_phrases)
    if person_type:
        intent = 'film_by_person'

        person_lemmas = lemmas[phrase_words:]
        person_name = lemmas_to_sentence(person_lemmas)

        return ParsedQuery(
            intent=intent,
            params={f'{person_type}s_names': person_name}
        )

    # find movie duration
    duration_phrases = {
        'сколько длиться': 'duration',
        'какой длительность': 'duration',
        'какой продолжительность': 'duration',
        'какой длина': 'duration',
        'сколько время': 'duration',
    }
    start_phrases = ['']
    query_type, phrase_words = query_start_with_phrase(stemmed_query, start_phrases, duration_phrases)
    if query_type:
        intent = 'duration_search'
        film_lemmas = lemmas[phrase_words:]
        film_lemmas = clear_movie_word(film_lemmas)
        film_title = lemmas_to_sentence(film_lemmas)

        return ParsedQuery(
            intent=intent,
            params={'title': film_title}
        )

    return None
