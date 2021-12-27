def get_sql_query(index, **kwargs) -> tuple:
    """Returns sql query with variables

    Args:
        index: index in elasticsearch
    Kwargs:
        updated_at: latest update of specified table
        batch_size: transfer batch size

    Returns:
        (sql_query, (value1, value2, ...))

    """
    return {
        'movies': (
            UPDATE_FILMWORK_INDEX,
            (kwargs['updated_at'], kwargs['updated_at'], kwargs['updated_at'], kwargs['batch_size'])
        ),
        'persons': (kwargs['updated_at'], kwargs['batch_size']),
        'genres': (kwargs['updated_at'], kwargs['batch_size']),
    }[index]


# With provided sql all updated data for denormalized film_works info,
# contained persons and genres as well, are selected in one query
UPDATE_FILMWORK_INDEX = """
    SELECT
        fw.id, fw.rating, fw.title, fw.description,
        jsonb_agg(jsonb_build_object('id', p.id, 'full_name', p.full_name, 'role', pfw.role)) AS persons,
        jsonb_agg(jsonb_build_object('id', g.id, 'name', g.name)) AS genres,
        GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at)) AS latest_update
    FROM content.film_work fw
    LEFT OUTER JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
    LEFT OUTER JOIN content.person p ON p.id = pfw.person_id
    LEFT OUTER JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
    LEFT OUTER JOIN content.genre g ON gfw.genre_id = g.id
    WHERE fw.updated_at > %s or p.updated_at > %s or g.updated_at > %s
    GROUP BY fw.id
    ORDER BY latest_update
    LIMIT %s;
"""
