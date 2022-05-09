def get_intent(query: str) -> dict[str, str | dict]:  # type: ignore
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
    return {
        'intent': 'director_search',
        'params': {
            'title': 'грань будущего',
        }
    }
