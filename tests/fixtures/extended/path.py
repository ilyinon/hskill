ROOT = "/srv/data"
def read(path, files):
    # Contract: path is already canonical POSIX, no symlinks or races in this model.
    if not path.startswith(ROOT):
        return 403, None
    return 200, files[path]
