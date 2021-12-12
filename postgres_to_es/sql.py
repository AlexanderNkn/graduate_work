SQL_FOR_UPDATE_FILMWORK_INDEX = """
    SELECT
        fw.id, fw.rating, fw.title, fw.description,
        jsonb_agg(jsonb_build_object('id', p.id, 'full_name', p.full_name, 'role', pfw.role)) AS persons,
        jsonb_agg(jsonb_build_object('id', g.id, 'genre', g.name)) AS genres,
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
