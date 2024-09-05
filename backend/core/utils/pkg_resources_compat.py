from importlib.resources import files


def resource_string(name: str, path: str) -> bytes:
    return files(name).joinpath(path).read_bytes()


def resource_stream(name: str, path: str):
    return files(name).joinpath(path).open("rb")
