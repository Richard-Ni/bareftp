import stat


def str_from_mode(mode):
    p = '-'
    if stat.S_ISDIR(mode):
        p = 'd'
    elif stat.S_ISLNK(mode):
        p = 'l'
    elif stat.S_ISSOCK(mode):
        p = 'l'
    for level in "USR", "GRP", "OTH":
        for perm in "R", "W", "X":
            if mode & getattr(stat, "S_I" + perm + level):
                p = p + perm.lower()
            else:
                p = p + '-'
    return p
