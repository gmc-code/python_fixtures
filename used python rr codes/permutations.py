from itertools import permutations


def teamlist(n):
    """
    Generates a list of teams using numbers from 1 to n.

    Args:
        n (int): The number of teams.

    Returns:
        list: A list of teams represented as strings. For example, teamlist(8) returns ['1', '2', '3', '4', '5', '6', '7', '8'].
    """
    team_list = []
    for i in range(1, n + 1):
        team_list.append(str(i))
    return team_list


def save_permutation(n, perm, namesuffix=""):
    """
    Saves a text file of permutations. The file name will be 'perm' concatenated with n, namesuffix, and '.txt'.
    ('1', '2', '3', '4', '5', '6') on a line

    Args:
        n (int): The number of teams.
        perm (list): The list of permutations.
        namesuffix (str, optional): The suffix for the file name. Defaults to "".

    Returns:
        None
    """
    with open("perm" + str(n) + namesuffix + ".txt", "w") as f:
        f.write("\n".join(str(permtuple) for permtuple in perm))


def perm_list(n):
    """
    Generates a list of permutations of teams.

    Args:
        n (int): The number of teams.

    Returns:
        list: A list of permutations of teams.
    """
    teams = teamlist(n)
    return list(permutations(teams))


# 12 fails with memory error
for n in range(6, 11, 2):
    perms = perm_list(n)
    save_permutation(n, perms, namesuffix="")
