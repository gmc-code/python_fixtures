
def create_balanced_round_robin_firstinplace(number_of_teams):
    """   
    Create a fixture of indices from a number of teams (to be used with a list of teams)
    The fixture is a list of rounds.
    Each round is a list of tuples.
    Each tuple is the Home and Away indices to be used on a list of teams.
    eg. for 6 teams
    [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
    This creates the _1 cyclic pattern with anticlockwise movement; keeping position 1 (python index 0)
    If there are odd teams add another as a placeholder to make an even number of teams
    For 6 teams, line up 3 tables in a column;
    Intial position numbering in sequence down side 1,2,3 then up other side 4,5,6
    python position numbering to start with is then 0,1,2 and 3,4,5
    Table numbers are 1 to 3; python tables indices are 0 to 2
    H/A alternate down left hand side: HAH
    match 1 left hand side team alternates H/A, odd round H, even rounds A
    ti is the team index list which will be split into two halves ti_lhs and ti_rhs
    With 6 teams; split into 2 halves of 3 teams.
    mid is half of the number of teams. It is the number of matches or tables in a round
    For each round use the full list and move indices anticlockwise using slicing.
    rd =rotatedistance; poss values from 1 to n-2; n/2 is ofter used by otehrs
    rd = 1 is required for HA pairing
    eg. 0,1,2,3,4,5 is rotated to 0,5,1,2,3,4 then next time to 0,4,5,1,2,3
    """
    fixture = []
    if number_of_teams % 2 == 1:
        number_of_teams = number_of_teams + 1
    number_of_rounds = number_of_teams - 1
    ti = list(range(number_of_teams))
    mid = number_of_teams // 2
    for round_number in range(number_of_rounds):
        #split list into 2 halves for each side of tables
        ti_lhs = ti[:mid]
        ti_rhs = ti[mid:]
        #reverse right hand side 
        ti_rhs.reverse()
        round = []
        for table_number in range(mid):
            t1 = ti_lhs[table_number]
            t2 = ti_rhs[table_number]
            if table_number == 0:
                if round_number % 2 == 0:
                    # keep the first match H/A, every odd round; index 0,2,4,...
                    round.append((t1, t2))
                else:
                    # flip the first match H/A, every even round; index 1,3,5,...
                    round.append((t2, t1))
            elif table_number % 2 == 0:
                # H/A pattern is HAHAHA' odds in order are Home; even indices are Home
                # every odd table; even index 0,2,4,...
                round.append((t1, t2))
            else:
                # every even table; odd index 1,3,5,...
                round.append((t2, t1))
        fixture.append(round)
        rd = 1
        #keeping first; rd numbers are moved from right hand end of list to after index 0.
        ti = [ti[0]] + ti[-rd:] + ti[1:-rd]  # ti[0] is an int and needs to be put in [ ] to make it a list for joining
    return fixture


def create_drr(fixture):
    """
    double fixture, reversing HA 
    """
    fixture_rounds = fixture[:]
    #add second half of double round robin reversing HA
    for round in fixture:
        fixture_rounds.append([pair[::-1] for pair in round])
    return fixture_rounds


def create_drr_withshift(fixture):
    """
    double fixture, reversing HA, with shift to right
    """
    fixture_rounds = fixture[:]
    #add second half of double round robin reversing HA
    #shift to right
    for round in fixture:
        round = round[-1:] + round[:-1]
        fixture_rounds.append([pair[::-1] for pair in round])
    return fixture_rounds


def swapHomeAway(mytuple):
    """
    swap the place of 2 elements in a tuple
    return new tuple
    """
    newtuple = mytuple[1], mytuple[0]
    return newtuple

    
def drr_fixture(fixture, teams, inmatchseparator=" v "):
    """
    double round robin fixture with last team on last table
    return fixture made up of H v A format with tab sperator between matches of same round in same line.
    eg: 1 v 2	4 v 3	5 v 6
    """
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
    """
    save text file of fixture; file name will be fixture_rounds & fixturenamesuffix & .txt
    """
   # use with open since it handles errors and closes the file automatically
    with open(str(n) + fixturenamesuffix + ".txt", "w") as f:
        f.write('\n'.join(fixture))


def teams_number_list(n):
    """
    Produce a list of teams using numbers.
    eg. teamlist(8) = ['1', '2', '3', '4', '5', '6', '7', '8']
    """
    if n % 2 == 1:
        n = n + 1
    team_list = []
    for i in range(1, n+1):
        team_list.append(str(i))
    return team_list


def teams_letter_list(n):
    """
    Produce a lists of teams using letters from A ...
    eg. teamlist(8) = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    """
    if n % 2 == 1:
        n = n + 1
    AsciiStart = ord('A') - 1
    team_list = []
    for i in range(1, n+1):
        team_list.append(chr(AsciiStart + i))
    return(team_list)


# save text files of all fixtures for 6,8,10,12,14,16,18,20,22,24 teams
for n in range(6, 25, 2):
    fixture = create_balanced_round_robin_firstinplace(n)
    teams = teams_number_list(n)
    drr = drr_fixture(fixture, teams, inmatchseparator=" v ")
    save_fixture(n, drr, fixturenamesuffix='_1')
    #letters version
    #teams = teams_letter_list(n)
    #drr = drr_fixture(fixture, teams, inmatchseparator="")
    #save_fixture(n, drr, fixturenamesuffix='_AZ1')
