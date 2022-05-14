from dataclasses import dataclass
from pymystem3 import Mystem

text_normalizer = Mystem()

@dataclass
class ParsedQuery:
    intent: str
    params: dict


def get_word(lemma):
    if 'analysis' in lemma:
        return lemma['analysis'][0]['lex']
    else:
        return lemma['text']


def is_preposition(lemma):
    if 'analysis' in lemma:
        grammem = lemma['analysis'][0]['gr'].split('=')[0]
        return grammem == 'PR'
    else:
        return False


def is_movie_word(lemma):
    return get_word(lemma) == 'фильм'


def get_intent(query: str) -> ParsedQuery:
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

    # сделаем лемматизацию
    # отсеем знаки препинания и лишние символы
    lemmas = text_normalizer.analyze(query)
    lemmas = [lemma for lemma in lemmas if 'analysis' in lemma or lemma['text'].isdigit()]
    words = [get_word(lemma) for lemma in lemmas]

    # уберем вводные слова
    intro_words = ['сказать', 'показывать', 'называть']
    word_num = 0
    while word_num < len(words):
        if words[word_num] in intro_words:
            word_num += 1
        else:
            break
    words = words[word_num:]
    lemmas = lemmas[word_num:]

    stemmed_query = ' '.join(words)
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

    start_phrases = ['кто быть', 'кто являться', 'кто', '']
    for start_phrase in start_phrases:
        if not stemmed_query.startswith(start_phrase):
            continue

        for phrase in person_phrases:
            if start_phrase:
                search_phrase = start_phrase + ' ' + phrase
            else:
                search_phrase = phrase

            if stemmed_query.startswith(search_phrase):
                person_type = person_phrases[phrase]

                phrase_words = len(search_phrase.split())
                film_lemmas = lemmas[phrase_words:]
                # уберем вводные "в фильме", "для фильма" "фильма"
                if len(film_lemmas) > 0 and is_movie_word(film_lemmas[0]):
                    film_lemmas = film_lemmas[1:]
                elif len(film_lemmas) > 1 and is_preposition(film_lemmas[0]) and is_movie_word(film_lemmas[1]):
                    film_lemmas = film_lemmas[2:]
                film_title = ' '.join(get_word(lemma) for lemma in film_lemmas)

                return ParsedQuery(
                    intent=person_type + '_search',
                    params={'title': film_title, }
                )

    start_phrases = ['что', 'где', 'какой фильм', 'в какой фильм', 'для какой фильм']
    for start_phrase in start_phrases:
        if not stemmed_query.startswith(start_phrase):
            continue

        for phrase in person_phrases:
            search_phrase = start_phrase + ' ' + phrase
            if stemmed_query.startswith(search_phrase):
                person_type = person_phrases[phrase]
                intent = 'film_by_person'

                phrase_words = len(search_phrase.split())
                person_lemmas = lemmas[phrase_words:]
                person_name = ' '.join(get_word(lemma) for lemma in person_lemmas)

                return ParsedQuery(
                    intent=intent,
                    params={person_type + 's_names': person_name, }
                )

    start_phrases = [
        'сколько длиться',
        'какой длительность',
        'какой продолжительность',
        'какой длина',
        'сколько время',
    ]
    for start_phrase in start_phrases:
        search_phrase = start_phrase

        if stemmed_query.startswith(search_phrase):
            intent = 'duration_search'

            phrase_words = len(search_phrase.split())
            film_lemmas = lemmas[phrase_words:]
            # уберем вводные "в фильме", "для фильма" "фильма"
            if len(film_lemmas) > 0 and is_movie_word(film_lemmas[0]):
                film_lemmas = film_lemmas[1:]
            elif len(film_lemmas) > 1 and is_preposition(film_lemmas[0]) and is_movie_word(film_lemmas[1]):
                film_lemmas = film_lemmas[2:]
            film_title = ' '.join(get_word(lemma) for lemma in film_lemmas)

            return ParsedQuery(
                intent=intent,
                params={'title': film_title, }
            )

    # response for testing purposes only
    return None


def check_text_by_template(text, template):
    pass
