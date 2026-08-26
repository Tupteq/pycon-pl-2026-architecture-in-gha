"""A tiny demo package used only to give tox and CI something real to run."""


def greet(name: str) -> str:
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
