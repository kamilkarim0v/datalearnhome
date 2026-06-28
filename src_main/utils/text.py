import re

def camel_to_snake(name: str) -> str:
    """Преобразует camelCase или CamelCase в snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()