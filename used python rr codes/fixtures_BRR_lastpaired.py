
def create_balanced_round_robin_lastinplace_numberpairing(number_of_teams):
    """   
    This creates the "last" cyclic pattern, for a particular number of teams, 
    with anticlockwise movement of teams around a column of tables; 
    keeping the last team on the last table; eg for 6 teams, team 6, python index 5, stays on last table
 
    The fixture is made up of a list of rounds.
    Each round is a list of tuples. eg. [(2, 3), (4, 1), (0, 5)]
    Each tuple is made up of idices in Home and Away order eg. (2, 3)
    eg. for 6 teams; 5 rounds
    [[(2, 3), (4, 1), (0, 5)], 
    [(1, 2), (3, 0), (5, 4)], 
    [(0, 1), (2, 4), (3, 5)], 
    [(4, 0), (1, 3), (5, 2)], 
    [(3, 4), (0, 2), (1, 5)]]

    Firstly, if there are odd teams, then add 1 to make an even number of teams
    For 6 teams, line up 3 tables in a column;
    Intial position numbering in pairs 0&1, 2&3, 4&5
    The team indices are then put in one list working antickwise from the top left of a column of tables
    0,1,2,3,4,5 becomes 0,2,4,5,3,1; where 5 is in mid position (6/2) index 3
    Table numbers are 1 to 3; python tables indices are 0 to 2
    H/A alternate down left hand side: HAH etc
    As teams move 1 step anticlockwise each round, they alternate H and A.
    Last match left hand side team alternates H/A, so that: 
    for odd number of tables: odd round H, even rounds A, 
    for even number of tables: odd round A, even rounds H
    ti is the team index list which will be split into two halves ti_lhs and ti_rhs
    With 6 teams; split into 2 halves of 3 teams.
    mid is half of the number of teams. It is the number of matches or tables in a round
    For each round use the full list and move indices anticlockwise using slicing.
    rd is used here to generalise the number of places each team moves from one round to the next.
    rd =rotatedistance; poss values from 1 to n-2; n/2 is sometimes used but it doesn't give the nice HA alternating pattern.
    To more easily allow rotation to be past half way when rd > n/2; remove mid from list, rotate list and put back in mid
    rd = 1 is required for HA pairing
    eg. 0,2,4,5,3,1 is rotated to 1,0,2,5,4,3 then next time to 3,1,0,5,2,4
    """

    fixture = []
    if number_of_teams % 2 == 1:
        number_of_teams = number_of_teams + 1
    number_of_rounds = number_of_teams - 1
    #build intial list pairs in sequence, 0,2,4 and 1,3,5 etc then reverse second list & join
    ti_lhs = list(range(0, number_of_teams, 2))
    ti_rhs = list(reversed(range(1, number_of_teams, 2)))
    #[0, 2, 4] is list down left side of tables; [5, 3, 1] is list up right side of tables
    ti = ti_lhs + ti_rhs
    mid = number_of_teams // 2   #want interger to be used as an index in list slicing
    for round_number in range(number_of_rounds):
        #split list into 2 halves for each side of tables
        ti_lhs = ti[:mid]
        ti_rhs = ti[mid:]
        #reverse right hand side 
        ti_rhs.reverse()
        round = []
        for table_number in range(mid):
            t1 = ti_lhs[table_number]   #team index 1
            t2 = ti_rhs[table_number]  # team index 2
            #first check for last match to decide its H or A
            if table_number == (mid - 1):
                if mid % 2 == 0:
                    #for last table is even, 0,2,4,6,8..H for odd rounds, A for even rounds
                    if round_number % 2 == 1:
                        # keep the last match H/A, every odd round; index 0,2,4,...
                        round.append((t1, t2))
                    else:
                        # flip the last match H/A, every even round; index 1,3,5,...
                        round.append((t2, t1))
                else:
                    #for last table is odd, 1,3,5,7..A for odd rounds, H for even rounds
                    if round_number % 2 == 0:
                        # keep the last match H/A, every odd round; index 0,2,4,...
                        round.append((t1, t2))
                    else:
                        # flip the last match H/A, every even round; index 1,3,5,...
                        round.append((t2, t1))   
            elif table_number % 2 == 0:
                # H/A pattern is HAHAHA' even table indices 0,2,4, are Home
                round.append((t1, t2))
            else:
                # A for every odd table index 1,3,5,...
                round.append((t2, t1))
        fixture.append(round)
        rd = 1
        ti_mid = [ti[mid]]  # ti[mid] is an int which needs to be put in [ ]  to make it a list
        ti1 = ti[:mid] + ti[(mid + 1):]  # mid removed  0,2,4,5,3,1 to rotate 0,2,4,3,1 
        ti1 = ti1[-rd:] + ti1[:-rd]  # rotate 0,2,4,3,1 is rotated to 1,0,2,4,3
        # put mid back in; keeping in mind there is 1 less in ti1 for slicing
        ti = ti1[:mid] + ti_mid + ti1[mid:]  #0,2,4,5,3,1 is rotated to 1,0,2,5,4,3
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

    
def drr_fixture(fixture, teams, inmatchseparator =" v "):
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
    fixture = create_balanced_round_robin_lastinplace_numberpairing(n)
    teams = teams_number_list(n)
    drr = drr_fixture(fixture, teams, inmatchseparator =" v ")
    save_fixture(n, drr, fixturenamesuffix ='_last')
    #letters version
    #teams = teams_letter_list(n)
    #drr = drr_fixture(fixture, teams, inmatchseparator="")
    #save_fixture(n, drr, fixturenamesuffix='_AZ_last')
