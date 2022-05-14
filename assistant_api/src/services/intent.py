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
            search_phrase = start_phrase + ' ' + phrase
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

    duration_phrases = {
        'сколько длиться': 'duration',
        'какая длительность': 'duration',
        'какая длина': 'duration',
        'сколько времени': 'duration',
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
    return None


def check_text_by_template(text, template):
    pass
