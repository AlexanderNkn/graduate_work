from dataclasses import dataclass
from pymystem3 import Mystem

text_normalizer = Mystem()

@dataclass
class ParsedQuery:
    intent: str
    params: dict


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
    #
    # # уберем соединительные глаголы: кто был режиссером - кто режиссер
    # stop_words = ['быть', 'являться']
    # # words = [word for word in words if word not in stop_words]
    # for lemma in lemmas:
    #     word = lemma['text']
    #     if word in stop_words and lemma['lemma_type'] == 'word':
    #         lemma['lemma_type'] = 'stop_words'
    #
    # words = [lemma['analysis'][0]['lex'] for lemma in lemmas]
    #
    # stemmed_query = (' '.join(words))
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
