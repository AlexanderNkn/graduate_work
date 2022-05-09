from dataclasses import dataclass


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
    # respons for testing purposes only
    return ParsedQuery(
        intent='director_search',
        params={
            'title': 'грань будущего',
        }
    )
