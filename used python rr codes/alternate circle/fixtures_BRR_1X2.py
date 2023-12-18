import collections


def create_balanced_round_robin(number_of_teams):
    rounds = number_of_teams - 1
    mid = number_of_teams // 2
    schedule = []
    teams = teams_indexlist(number_of_teams)
    d = collections.deque(teams)  # deque([0, 1, 2, 3, 4, 5])
    dl = list(collections.deque(d))   #[0, 1, 2, 3, 4, 5]
    rl = dl[::-1]
    pl = list(zip(dl[:mid:1], rl[:mid:1]))   # [(0, 1), (2, 3), (4, 5)]
    print(dl, rl, pl, sep= '\n')
    schedule.append(pl)
    for turn in range(1,rounds):
        d.rotate(1)  # deque([5, 0, 1, 2, 3, 4])
        # Swap bye week back to top
        d[1] = d[0]
        d[0] = 0  #deque([0, 5, 1, 2, 3, 4])
        dl = list(collections.deque(d))
        rl = dl[::-1]
        pl = list(zip(dl[:mid:1], rl[:mid:1]))  # [(0, 5), (1, 2), (3, 4)]
        schedule.append(pl)
        print(dl, rl, pl, sep='\n')
    return schedule


def teams_indexlist(n):
    '''
    Produce a list of teams using numbers starting at 0.
    '''
    if n % 2 == 1:
        n = n + 1
    team_list = []
    for i in range(0, n):
        team_list.append(i)
    return team_list


def teams_number_list(n):
    '''
    Produce a list of teams using numbers.
    eg. teamlist(8) = ['1', '2', '3', '4', '5', '6', '7', '8']
    '''
    if n % 2 == 1:
        n = n + 1
    team_list = []
    for i in range(1, n+1):
        team_list.append(str(i))
    return team_list


def drr_fixture(fixture, teams, inmatchseparator=" v "):
    '''
    double round robin fixture with last team on last table
    return fixture made up of H v A format with tab sperator between matches of same round in same line.
    eg: 1 v 2	4 v 3	5 v 6
    '''
    fixture_rounds = []
    for round in fixture:
        fixture_rounds.append(
            '\t'.join([f'{teams[pair[0]]}{inmatchseparator}{teams[pair[1]]}' for pair in round]))
    #add second half of double round robin reversing HA
    for round in fixture:
        fixture_rounds.append(
            '\t'.join([f'{teams[pair[1]]}{inmatchseparator}{teams[pair[0]]}' for pair in round]))
    return fixture_rounds


def save_fixture(n, fixture, fixturenamesuffix=""):
    '''
    save text file of fixture; file name will be fixture_rounds & fixturenamesuffix & .txt
    '''
   # use with open since it handles errors and closes the file automatically
    with open(str(n) + fixturenamesuffix + ".txt", "w") as f:
        f.write('\n'.join(fixture))


for n in range(6, 7, 2):
    fixture = create_balanced_round_robin(n)
    teams=teams_number_list(n)
    drr = drr_fixture(fixture, teams, inmatchseparator=" v ")
    save_fixture(n, drr, fixturenamesuffix='_1X2')
    
    
    
