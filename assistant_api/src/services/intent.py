from dataclasses import dataclass

INTENTS = {
    ('кто', 'снимать'): 'director_search',
    ('кто', 'режиссёр'): 'director_search',
}


@dataclass
class ParsedQuery:
    intent: str
    params: dict


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
    # respons for testing purposes only
    words = query.lower().split()
    for combination, intent in INTENTS.items():
        if all(word in words for word in combination):
            return ParsedQuery(
                intent=intent,
                params={
                    'title': ' '.join(word for word in words if word not in combination),
                }
            )

    return None
