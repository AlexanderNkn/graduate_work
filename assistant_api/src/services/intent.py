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
        'кто режиссер': 'director_search',
        'кто сняться': 'actor_search',
        'кто снять': 'director_search',
        'кто актер': 'actor_search',
        'кто написать сценарий': 'writer_search',
        'кто создать сценарий': 'writer_search',
        'кто сценарист': 'writer_search',
        'кто автор сценарий': 'writer_search',
    }

    for phrase in person_phrases:
        if stemmed_query.startswith(phrase):
            intent = person_phrases[phrase]
            phrase_words = len(phrase.split())
            film_lemmas = lemmas[phrase_words:]
            # уберем вводные "в фильме", "для фильма" "фильма"
            if len(film_lemmas) > 0 and is_movie_word(film_lemmas[0]):
                film_lemmas = film_lemmas[1:]
            elif len(film_lemmas) > 1 and is_preposition(film_lemmas[0]) and is_movie_word(film_lemmas[1]):
                film_lemmas = film_lemmas[2:]
            film_title = ' '.join(get_word(lemma) for lemma in film_lemmas)
            params = {
                'title': film_title,
            }

            return ParsedQuery(
                intent=intent,
                params={'title': film_title, }
            )

    film_phrases = {
        'что снял ': '',
        'где снялся': '',
        'в каких фильмах снялся': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
    }

    # for lemma in lemmas:
    #     lemma['lemma_type'] = 'word'
    #
    # # заменим все вводные слова на один токен
    # intro_words = ['сказать', 'показывать', 'называть']
    # for lemma in lemmas:
    #     word = lemma['text']
    #     if word in intro_words and lemma['lemma_type'] == 'word':
    #         lemma['lemma_type'] = 'intro'
    #     else:
    #         break

    # # уберем соединительные глаголы: кто был режиссером - кто режиссер
    # stop_words = ['быть', 'являться']
    # # words = [word for word in words if word not in stop_words]
    # for lemma in lemmas:
    #     word = lemma['text']
    #     if word in stop_words and lemma['lemma_type'] == 'word':
    #         lemma['lemma_type'] = 'stop_words'
    #
    #
    #
    # # заменим фразы на токены-профессии
    # key_words = {
    #     'director': ['режиссер', 'снять', ],
    #     'actor': ['актер', 'сниматься', ],
    #     'writer': ['сценарист', 'написать сценарий', 'написать', 'создать сценарий', 'автор сценарий'],
    # }
    #
    # for token, key_phrases in key_words.items():
    #     for key_phrase in key_phrases:
    #         stemmed_query = stemmed_query.replace(key_phrase, '<' + token + '>')

    # "Кто (автор / режиссер / снял) (фильм) (название фильма)"
    # "Кто ((быть, являться) + существительное) ((предлог) + фильм) (название фильма)"
    # "Кто (глагол) (предлог + фильм) (название фильма)"
    # templates = [
    #     (('кто', 'intro', ), 0), (('сущ', ), 1)
    # ]
    #
    # key_words = {
    #     'director_search': ['кто режиссер', 'кто снять', 'кто автор', 'intro режиссер', ],
    #     'actor_search': ['кто сниматься', 'кто актер', 'какой актер', 'intro актер'],
    #     'write_search': ['кто написать', 'кто сценарист', 'кто написать сценарий', 'кто создать сценарий',
    #                      'intro автор сценарий', 'сценарий'],
    #     'film_search': ['что снять', 'какой фильм', '']
    # }

    # response for testing purposes only
    return ParsedQuery(
        intent='director_search',
        params={
            'title': 'грань будущего',
        }
    )


def check_text_by_template(text, template):
    pass
