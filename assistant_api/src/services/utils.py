from pathlib import Path

from jinja2 import Environment, FileSystemLoader  # type: ignore

template_dir = Path(__file__).resolve().parent.parent.parent
template_loader = FileSystemLoader(template_dir)


def get_site(template_path: str, query: str, films: list = None, genres: list = None, persons: list = None) -> str:
    env = Environment(loader=template_loader, autoescape=True)
    template = env.get_template(template_path)

    template_data = {
        'query': query,
        'films': films,
        'genres': genres,
        'persons': persons,
    }

    return template.render(**template_data)
