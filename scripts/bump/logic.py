import pathlib


def find(file: str, dir: str | pathlib.Path | None = "", shard: str | None = None, recursive_limit: int = 3):
    """
    Files a file given a name and parent dir
    """

    # Check Files
    current: pathlib.Path = shard or pathlib.Path("./")   
    parts = current.glob("./*")
    if dir[0] is None:
        result = [x for x in parts if (x.is_file() and x.name == file)]
        if not result:
            return None
        return result[0]
    
    if isinstance(dir, str):
        dir = dir.split("/")
    
    # Check Dirs
    res = [x for x in parts if (x.is_dir() and x.name == dir[0])]
    if res:
        if recursive_limit == 0:
            print("Reached recursive limit")
            return None
        del dir[0]
        if not dir:
            dir = [None]
        return find(file, dir, res[0], recursive_limit=recursive_limit-1)        

    return None


def update(old, level):
    
    if level not in ["major", "minor", "patch"]:
        return level.strip("v")

    # in major minor patch
    o_ma, o_mi, o_p = [int(x) for x in old.split(".")]

    match level:
        case "major":
            o_ma += 1
            o_mi = 0
            o_p = 0
        case "minor":
            o_mi += 1
            o_p = 0
        case "patch":
            o_p += 1

    return ".".join([str(o_ma), str(o_mi), str(o_p)])

        