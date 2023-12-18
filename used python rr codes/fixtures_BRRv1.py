
import numpy as np
import re
import sys

#24 teams fixture gets truncated without this
np.set_printoptions(threshold=sys.maxsize)

def create_brr_firstinplace(number_of_teams):
    """Return the _1 cyclic pattern fixture of indices from a number of teams.
    create_balanced_round_robin_firstinplace
    This creates the _1 cyclic pattern with anticlockwise movement; keeping position 1 (python index 0)
    Note Slightly better fixtures are possible for 6,8,10 teams in keeping rus of 3 to 0  
    The fixture is a list of rounds.
    Each round is a list of tuples.
    Each tuple is the Home and Away indices to be used on a list of teams.
    eg. for 6 teams
    [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
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

##############################################################################################

def create_brr_evens(n):
    """Return balanced table/slot allocation for all teams 6 to 24 except 16 and 22; fixture is a list of lists of tuples.
    create_balanced_round_robin_evens
    Requires _1 cyclic pattern fixture from create_brr_firstinplace function
    Produce balanced table/slot allocation for all teams 6 to 24 except 16 and 22; n satisfies n≡{0,2}(mod3).
    Use create_brr_firstinplace function then do slot swaps using the algorithm of Hasselgrove and Leech (1977) 
    Use row_order_for_balancing for rows to swap
    It takes the typical cyclic table and starts at Round 1, counts n/2−1 rounds down, and records that round as the next Round. 
    This continues until all the rounds have been chosen; when you reach the last row, cycle back up to the first row and continue. 
    For 8 teams, the Rounds 1-7 correspond to the old Rounds 1,4,7,3,6,2,5 which in python is [0, 3, 6, 2, 5, 1, 4]
    Use col_order_for_balancing for columns to swap
    It follows a symetrical patternas seen in the ex. for 8 teams [2, 3, 4, 4, 3, 2]
    For a good description see: http://www.statsathome.com/2017/07/01/a-post-on-tournament-designs/
    eg. return: [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
    """
    fixture = create_brr_firstinplace(n)
    col_list = col_order_for_balancing(n)
    row_list = row_order_for_balancing(n)
    #for 8teams, swaps are in top 6 rows of 7 rows
    #print(col_list, row_list)
    for i in range(n - 2):
        tuple1 = fixture[row_list[i]][0]
        tuple2 = fixture[row_list[i]][col_list[i]]
        #print(tuple1, tuple2)
        fixture[row_list[i]][col_list[i]] = tuple1
        fixture[row_list[i]][0] = tuple2
    return fixture

##############################################################################################

def create_brr_lastinplace(number_of_teams):
    """Return the _last cyclic pattern fixture of indices from a number of teams.   
    create_balanced_round_robin_lastinplace_numberpairing
    The "last" cyclic pattern, uses anticlockwise movement of teams around a column of tables; 
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
    mid = number_of_teams // 2  # want interger to be used as an index in list slicing
    for round_number in range(number_of_rounds):
        #split list into 2 halves for each side of tables
        ti_lhs = ti[:mid]
        ti_rhs = ti[mid:]
        #reverse right hand side
        ti_rhs.reverse()
        round = []
        for table_number in range(mid):
            t1 = ti_lhs[table_number]  # team index 1
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
        # ti[mid] is an int which needs to be put in [ ]  to make it a list
        ti_mid = [ti[mid]]
        # mid removed  0,2,4,5,3,1 to rotate 0,2,4,3,1
        ti1 = ti[:mid] + ti[(mid + 1):]
        ti1 = ti1[-rd:] + ti1[:-rd]  # rotate 0,2,4,3,1 is rotated to 1,0,2,4,3
        # put mid back in; keeping in mind there is 1 less in ti1 for slicing
        # 0,2,4,5,3,1 is rotated to 1,0,2,5,4,3
        ti = ti1[:mid] + ti_mid + ti1[mid:]
    return fixture

##############################################################################################


def create_brr_firstinplace_forbalanced(number_of_teams):
    """Return the  pattern fixture of indices from a number of teams.   
    create_balanced_round_robin_firstinplace_forbalanced
    clockwise
    step n/2-1
    The fixture is a list of rounds.
    Each round is a list of tuples.
    Each tuple is the Home and Away indices to be used on a list of teams.
    eg. for 6 teams
    [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
    This creates the _1 cyclic pattern with clockwise movement; keeping position 1 (python index 0)
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
                    # keep the first match H/A, every even round; index 1,3,5,...
                    round.append((t1, t2))  # round.append((t2, t1))
            elif table_number % 2 == 0:
                # H/A pattern is HAHAHA' odds in order are Home; even indices are Home
                # every odd table; even index 0,2,4,...
                round.append((t1, t2))
            else:
                # every even table; odd index 1,3,5,...
                round.append((t1, t2))  # round.append((t2, t1))
        fixture.append(round)
        rd = 1
        #keeping first; rd numbers are moved 3 places clockwise
        #01234567 becomes 04567123 becomes 07123456
        # 0,2,4,5,3,1 is rotated to 1,0,2,5,4,3
        # ti[0] is an int and needs to be put in [ ] to make it a list for joining
        ti = [ti[0]] + ti[mid:] + ti[1:mid]
        #print(ti)
    return fixture


def create_brr_evens_forbalanced(n):
    """Return the  pattern fixture of indices from a number of teams.
    create_brr_evens_forbalanced
    Produce balanced table allocation for all teams 6 to 24 except 16 and 22
    Use firstinplace function then do table swaps using the algorithm of Hasselgrove and Leech (1977) 
    n satisfies n≡{0,2}(mod3).
    fixture is a list of lists of tuples.
    [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
    [1, 2, 2, 1] [0, 2, 4, 1, 3]
    (0, 5) (4, 1)
    (0, 3) (5, 1)
    (0, 1) (3, 4)
    (4, 0) (3, 5)
    """
    fixture = create_brr_firstinplace_forbalanced(n)
    col_list = col_order_for_balancing(n)
    row_list = row_order_for_balanced_balancing(n)
    #for 8teams, swapsare in top6rows
    #print(col_list, row_list)
    mid = n//2 - 1
    for i in range(0, mid):
        tuple1 = fixture[row_list[i]][0]
        tuple2 = fixture[row_list[i]][col_list[i]]
        #print(fixture[i])
        #print(i, tuple1, tuple2)
        fixture[row_list[i]][col_list[i]] = tuple1
        fixture[row_list[i]][0] = tuple2
    #print("-----------")
    for i in range(mid, n - 2):
        tuple1 = tuple(reversed(list(fixture[row_list[i]][0])))
        tuple2 = tuple(reversed(list(fixture[row_list[i]][col_list[i]])))
        #print(fixture[i])
        #print(i, tuple1, tuple2)
        fixture[row_list[i]][col_list[i]] = tuple1
        fixture[row_list[i]][0] = tuple2
    return fixture


##############################################################################################

def create_brr_oddteams(number_of_teams, balanced=False):
    """Return the  pattern fixture of indices from a number of teams.   
    create_balanced_round_robin_oddteams
    balanced=False has first 2 teams in alternating pattern
    balanced=True has first 2 teams not in alternating pattern; perfectly balanced half of season as well as overall
    #
    Create a fixture of indices from a number of teams (to be used with a list of teams)
    The fixture is a list of rounds.
    Each round is a list of tuples.
    Each tuple is the Home and Away indices to be used on a list of teams.
    eg. for 6 teams
    [[(0, 5), (4, 1), (2, 3)], [(4, 0), (3, 5), (1, 2)], [(0, 3), (2, 4), (5, 1)], [(2, 0), (1, 3), (4, 5)], [(0, 1), (5, 2), (3, 4)]]
    This uses the _1 cyclic pattern with anticlockwise movement; keeping position 1 (python index 0); as the starting point
    Then matches 0 and 1 have HA reversed.
    Then match 0 is put to last match in each row.
    Then rows are reversed in order.
    This gives the minimum number of runs of 3s due to byes; first 2 teams have this mid season in a double round robin.
    #
    _1 cyclic pattern:
    If there are odd teams add another as a placeholder to make an even number of teams
    For 6 teams, line up 3 tables in a column;
    Intial position numbering in sequence down side 0,1,2 and 3,4,5
    Table numbers are tables indices are 0 to 2
    H/A alternate down left hand side: HAH
    match 0 left hand side team alternates H/A, odd (0,2,4 indices) round H, even ( 1,3,5 indices) rounds A
    ti is the team index list which will be split into two halves ti_lhs and ti_rhs
    With 6 teams; split into 2 halves of 3 teams.
    mid is half of the number of teams. It is the number of matches or tables in a round
    For each round use the full list and move indices anticlockwise using slicing.
    rd =rotatedistance; poss values from 1 to n-2; n/2 is ofter used by others
    rd = 1 is required for HA pairing
    eg. 0,1,2,3,4,5 is rotated to 0,5,1,2,3,4 then next time to 0,4,5,1,2,3
    """
    fixture = []
    if number_of_teams % 2 == 1:
        number_of_teams = number_of_teams + 1
    number_of_rounds = number_of_teams - 1
    ti = list(range(number_of_teams))[::-1]
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
                    # keep the first match H/A, every odd round; even table index 0,2,4,...
                    round.append((t1, t2))
                else:
                    # flip the first match H/A, every even round; odd table index 1,3,5,...
                    round.append((t2, t1))
            elif table_number % 2 == 0:
                # H/A pattern is HAHAHA' odds in order are Home; even indices are Home
                # every odd table; even index 0,2,4,...
                round.append((t1, t2))
            else:
                # every even table; odd index 1,3,5,...
                round.append((t2, t1))
        if balanced == False:
            # adjust first round first 2 matches flip HA in tuples of matches
            if round_number == 0:
                #print(round[0])
                round0match0 = [(swapHomeAway(round[0]))]
                #print(round0match0)
                #print(round[1])
                round0match1 = [(swapHomeAway(round[1]))]
                #print(round0match1)
                round = round0match0 + round0match1 + round[2:]
                #print(round)
        fixture.append(round)
        rd = 1
        #keeping first; rd numbers are moved from right hand end of list to after index 0.
        # ti[0] is an int and needs to be put in [ ] to make it a list for joining
        ti = [ti[0]] + ti[-rd:] + ti[1:-rd]
    #move match 1 of each row to last match
    # reverse row order; this reduces suns of 3 in minimum of 2 in double round robin
    newfixture = []
    for round in fixture:
        newround = [round[1:] + round[:1]]
        newfixture = newround + newfixture
    return newfixture

##############################################################################################

def row_order_for_balanced_balancing(n):
    """Return a list of row orders (from 0) for n team fixture for balancing algorithm
    eg. for 8 teams [0,1,2,3,4,5] not 6
    """
    #make n even
    if n % 2 == 1:
        n = n + 1
    #fixture has one less row than the number of teams
    rowcount = n - 2
    row_list = []
    for i in range(0, rowcount):
        row = i
        row_list.append(row)
    return row_list

##############################################################################################

def row_order_for_balancing(n):
    """Return a list of row orders (from 0) for n team fixture for balancing algorithm.
    eg. for 8 teams [0, 3, 6, 2, 5, 1, 4]
    """
    #make n even
    if n % 2 == 1:
        n = n + 1
    #fixture has one less row than the number of teams
    rowcount = n - 1
    rowadd = n//2 - 1
    #keep first row
    row = 0
    row_list = [row]
    #for 6 teams, 5 rows, loop 4 times from 1 to 4
    # calculatings are mod the number of rows
    for i in range(1, rowcount):
        row = (row + rowadd) % rowcount
        row_list.append(row)
    return row_list


def col_order_for_balancing(n):
    """Return a list of col orders (from 0) for n team fixture for balancing algorithm
    eg. for 8 teams [2, 3, 4, 4, 3, 2]
    """
    #make n even
    if n % 2 == 1:
        n = n + 1
    #fixture has one less row than the number of teams; will go up to but not include n-1, so only n-2 top rows
    rowcount = n - 1
    #top half of n-2 rows has symmetry with bottom half
    rowmid = n//2 - 1  # 3 for 8 teams
    #keep first row
    col_list = []
    #for 8 teams, 6 rows, loop 2x3 times
    #for 8 teams rows = 0 to 2; col =  2 to 4
    for col in range(rowmid):
        col_list.append(col + 1)
    #for 8 teams rows = 3 to 5; col =  4 to 2
    for col in range(rowmid, rowcount - 1):
        col_list.append(rowcount - col -1)
    return col_list


def create_drr(fixture):
    """Return double fixture, reversing HA in second half of RoundRobin"""
    fixture_rounds = fixture[:]
    #add second half of double round robin reversing HA
    for round in fixture:
        fixture_rounds.append([pair[::-1] for pair in round])
    return fixture_rounds


def create_drr_withshift(fixture):
    """Return double fixture with shift 1 column to right, reversing HA in second half of RoundRobin"""
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


def create_fixture_grid(fixture, teams, inmatchseparator=" v "):
    """Return text grid of fixture.
    Fixture made up of H v A format with tab separator between matches of same round in same line.
    eg: 1 v 2	4 v 3	5 v 6
    """
    fixture_rounds = []
    for round in fixture:
        fixture_rounds.append(
            '\t'.join([f'{teams[pair[0]]}{inmatchseparator}{teams[pair[1]]}' for pair in round]))
    return fixture_rounds


def save_fixture(n, fixture_grid, fixturenamesuffix="", fixtureprefix="FixtureTemplate"):
    """Save text file of fixture_grid; file name will be n & fixturenamesuffix & .txt"""
    # use with open since it handles errors and closes the file automatically
    with open(fixtureprefix + str(n) + fixturenamesuffix + ".txt", "w") as f:
        f.write('\n'.join(fixture_grid))


def teams_number_list(n):
    """Return a list of teams using numbers.
    eg. teamlist(8) = ['1', '2', '3', '4', '5', '6', '7', '8']
    """
    if n % 2 == 1:
        n = n + 1
    team_list = []
    for i in range(1, n+1):
        team_list.append(str(i))
    return team_list


def teams_letter_list(n):
    """Return a list of teams using letters from A ...
    eg. teamlist(8) = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    """
    if n % 2 == 1:
        n = n + 1
    AsciiStart = ord('A') - 1
    team_list = []
    for i in range(1, n+1):
        team_list.append(chr(AsciiStart + i))
    return(team_list)

##############################################################################################
##### balanced for 10,16,22
##############################################################################################

# def balanced10():
#     return '[[0, 5, 1, 6, 2, 7, 3, 8, 4, 9],\
#     [4, 1, 0, 2, 6, 3, 9, 7, 8, 5],\
#     [3, 2, 9, 8, 4, 0, 5, 6, 7, 1],\
#     [1, 9, 5, 7, 8, 6, 4, 2, 3, 0],\
#     [2, 8, 4, 3, 9, 5, 0, 1, 6, 7],\
#     [9, 6, 2, 5, 3, 1, 7, 4, 0, 8],\
#     [8, 7, 3, 9, 5, 4, 6, 0, 1, 2],\
#     [6, 4, 7, 0, 1, 8, 2, 9, 5, 3],\
#     [7, 3, 8, 4, 0, 9, 1, 5, 2, 6]]'


def balanced10():
    list10 = [[(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)],
              [(4, 1), (0, 2), (6, 3), (9, 7), (8, 5)],
              [(3, 2), (9, 8), (4, 0), (5, 6), (7, 1)],
              [(1, 9), (5, 7), (8, 6), (4, 2), (3, 0)],
              [(2, 8), (4, 3), (9, 5), (0, 1), (6, 7)],
              [(9, 6), (2, 5), (3, 1), (7, 4), (0, 8)],
              [(8, 7), (3, 9), (5, 4), (6, 0), (1, 2)],
              [(6, 4), (7, 0), (1, 8), (2, 9), (5, 3)],
              [(7, 3), (8, 4), (0, 9), (1, 5), (2, 6)]]
    return list10

##############################################################################################
#####anaylsis using numpy
##############################################################################################

def nparray_from_fixture(fixture):
    """Return a numpy array for a fixture"""
    # [[(4, 1), (0, 5), (2, 3)], [(3, 5), (4, 0), (1, 2)], [(5, 1), (2, 4), (0, 3)], [(2, 0), (1, 3), (4, 5)], [(3, 4), (5, 2), (0, 1)]]
    rows = []
    for row in fixture:
        newrowtup = ()
        for tup in row:
            newrowtup += tup
        newrow = list(newrowtup)
        rows.append(newrow)
    #[[4, 1, 0, 5, 2, 3], [3, 5, 4, 0, 1, 2], [5, 1, 2, 4, 0, 3], [2, 0, 1, 3, 4, 5], [3, 4, 5, 2, 0, 1]]
    npfixture = np.array(rows)
    # [[4 1 0 5 2 3]
    #  [3 5 4 0 1 2]
    #  [5 1 2 4 0 3]
    #  [2 0 1 3 4 5]
    #  [3 4 5 2 0 1]]
    return npfixture


def fixture_analysis_index_pos_count(n, fixture):
    """Return a numpy array of counts of each team index in each team slot of a single round robin fixture"""
    '''Home and Away position count; row number matches index having the occurance count in each column eg. HAHAHA
    [[0 1 1 1 2 0]
    [0 2 1 0 1 1]
    [1 0 1 1 1 1]
    [2 0 0 1 0 2]
    [1 1 1 1 1 0]
    [1 1 1 1 0 1]]
    '''
    npfix = nparray_from_fixture(fixture)
    #make sure n is even
    if n % 2 == 1:
        n = n + 1
    #init numpy array for length test to start
    all_col_occs = np.array([])
    for i in range(n):
        column_occurrences = np.count_nonzero(npfix == i, axis=0)
        # add each row to numpy.ndarray
        if len(all_col_occs) == 0:
            all_col_occs = column_occurrences
        else:
            all_col_occs = np.vstack((all_col_occs, column_occurrences))
    return all_col_occs


def fixture_analysis_index_table_count(n, drr_fixture):
    """Return a numpy array of counts of each team index in each table slot of a double round robin fixture"""
    '''
    Match/Table count with row number matches index having the occurance count for match/table columns
    [[3 3 4]
    [4 3 3]
    [3 3 4]
    [4 3 3]
    [3 4 3]
    [3 4 3]]
    '''
    npfix = nparray_from_fixture(drr_fixture)
    #make sure n is even
    if n % 2 == 1:
        n = n + 1
    #init numpy array for length test to start
    all_col_occs = np.array([])
    for i in range(n):
        column_occurrences = np.count_nonzero(npfix == i, axis=0)
        combined_column_occurrences = column_occurrences[::2] + column_occurrences[1::2]
        # add each row to numpy.ndarray
        if len(all_col_occs) == 0:
            all_col_occs = combined_column_occurrences
        else:
            all_col_occs = np.vstack(
                (all_col_occs, combined_column_occurrences))
    return all_col_occs


def fixture_analysis_home_and_away(n, drr_fixture):
    """Return str of table of home and away sequences for each team (col) in each round (row)"""
    npfix = nparray_from_fixture(drr_fixture)
    # make sure n is even
    if n % 2 == 1:
        n = n + 1
    rowscount = npfix.shape[0]
    #init numpy array with '' as each element
    home_for_team_in_each_round = np.zeros((rowscount, n), dtype=str)
    for teamnum in range(n):
        for rowround in range(rowscount):
            row_home_for_team_count = np.count_nonzero(npfix[rowround,:n:2] == teamnum)
            if row_home_for_team_count == 1:
                home_for_team_in_each_round[rowround, teamnum] = "H"
            else:
                home_for_team_in_each_round[rowround, teamnum] = "."
    return home_for_team_in_each_round


def fixture_analysis_1(homeawaytable_array):
    """Return str of measure of balance by count of non 1 occurance values for home and away columns"""
    size = np.size(homeawaytable_array)
    occurrences1 = np.count_nonzero(homeawaytable_array == 1)
    return str(size - occurrences1)


def fixture_analysis_3or4(tablebalance_array):
    """Return str of measure of balance by count of non 3 or 4 occurance values for table locations"""
    size = np.size(tablebalance_array)
    occurrences3 = np.count_nonzero(tablebalance_array == 3)
    occurrences4 = np.count_nonzero(tablebalance_array == 4)
    return str(size - occurrences3 - occurrences4)


def fixture_analysis_runsof3(ha_array):
    """Return count of runs of 3 Home (HHH) or 3 Away (...)"""
    #transpose first so colums put in rows for sequence check
    array_string = str(ha_array.transpose())
    total_runsof3 = 0
    #replace quotes and spaces with empty and remove start [
    array_string = re.sub('\'|\s|\[', '', array_string)
    #replace end] with new line so count works
    array_string = re.sub('\]', '\n', array_string)
    runsof3 = array_string.count('HHH') + array_string.count('...')
    total_runsof3 += runsof3
    return str(total_runsof3)


def array_to_str_for_printing(array):
    """Return array as a string without quotes, spaces and square brackets"""
    #convert to a list first to get comma separators instead of space to make it easier to remove
    array_string = str(array.tolist())
    #print(array_string)
    array_string = re.sub('\]\, \[', '\n', array_string)
    array_string = re.sub('\, ', '\t', array_string)
    array_string = re.sub('\'|\[', '', array_string)
    array_string = re.sub('\]', '\n', array_string)
    #print(array_string)
    return array_string


def save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix="", fixtureprefix="FixtureAnalysis"):
    """Save text file of analysis of fixture; file name will be fixtureprefix & n & fixturenamesuffix & .txt"""
    homeawaytable_array = fixture_analysis_index_pos_count(n, fixture,)
    homeawaytable = array_to_str_for_printing(homeawaytable_array)
    homeawaytable_array_1 = fixture_analysis_1(homeawaytable_array)
    #
    tablebalance_array = fixture_analysis_index_table_count(n, drr_fixture)
    tablebalance_string = array_to_str_for_printing(tablebalance_array)
    tablebalance_array_3or4 = fixture_analysis_3or4(tablebalance_array)
    #
    homeawaytable_foreachround_array = fixture_analysis_home_and_away(n, drr_fixture)
    homeawaytable_foreachround_string = array_to_str_for_printing(homeawaytable_foreachround_array)
    runs_of_3 = fixture_analysis_runsof3(homeawaytable_foreachround_array)
    # use with open since it handles errors and closes the file automatically
    with open(fixtureprefix + str(n) + fixturenamesuffix + ".txt", "w") as f:
        f.write('Fixture analysis.' + fixtureprefix + str(n) + fixturenamesuffix + '\n\n')
        f.write('Home and Away position count. Row number = index.\n')
        f.write('Counts of 1 are expected. They occur when the team number is only Home (or Away) once on that table in a single round robin fixture.\n')
        f.write('Counts of non 1 in a round robin fixture:  ')
        f.write(homeawaytable_array_1)
        f.write('\n')
        f.write(homeawaytable)
        f.write('\n\n')
        f.write('Match/Table count. Row number = index.\n')
        f.write('Counts of 3 or 4 are expected. They occur when the team numbers plays on that table in a double round robin fixture.\n')
        f.write('Counts of non 3 or 4 in a double round robin fixture:  ')
        f.write(tablebalance_array_3or4)
        f.write('\n')
        f.write(tablebalance_string)
        f.write('\n\n')
        f.write('Home and Away vertical sequence for each team number.\n')
        f.write('Runs of 3: ')
        f.write(runs_of_3)
        f.write('\n')
        f.write(homeawaytable_foreachround_string)



##############################################################################################
###### save files of fixtures and their analysis
##############################################################################################

def fixtures_even():
    """Save text files of all fixtures for 6,8,10,12,14,16,18,20,22,24 teams"""
    for n in range(6, 25, 2):
        fixture = create_brr_evens(n)
        drr_fixture = create_drr_withshift(fixture)
        teams = teams_number_list(n)
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator=" v ")
        save_fixture(n, drr_grid, fixturenamesuffix='')
        save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix='')
        #  
        #letters version
        #teams = teams_letter_list(n)
        #drr = drr_fixture_withshift(fixture, teams, inmatchseparator="")
        #save_fixture(n, drr, fixturenamesuffix='_AZ1')


def fixtures_even_1():
    """Save text files of all fixtures_1 for 6,8,10,12,14,16,18,20,22,24 teams"""
    for n in range(6, 25, 2):
        fixture = create_brr_firstinplace(n)
        drr_fixture = create_drr(fixture)
        teams = teams_number_list(n)
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator=" v ")
        save_fixture(n, drr_grid, fixturenamesuffix='_1')
        save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix='_1')


def fixtures_last():
    """Save text files of all fixtures_last for 6,8,10,12,14,16,18,20,22,24 teams"""
    for n in range(6, 25, 2):
        fixture = create_brr_lastinplace(n)
        drr_fixture = create_drr(fixture)
        teams = teams_number_list(n)
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator=" v ")
        save_fixture(n, drr_grid, fixturenamesuffix='_last')
        save_fixture_analysis(n, fixture, drr_fixture,fixturenamesuffix='_last')


def fixtures_even_balanced():
    """Save text files of all fixtures_balanced for 6,8,10,12,14,16,18,20,22,24 teams"""
    for n in range(6, 25, 2):
        fixture = create_brr_evens_forbalanced(n)
        drr_fixture = create_drr_withshift(fixture)
        teams = teams_number_list(n)
        #teams = ['1', '3', '4', '5', '6', '7', '8', '2']
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator="\t")
        save_fixture(n, drr_grid, fixturenamesuffix='_balanced')
        save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix='_balanced')


def fixtures_odds():
    """Save text files of all fixtures 5,7,9,11,13,15,17,19,21,23 teams"""
    # not intended for use with even number teams 6...24
    for n in range(5, 24, 2):
        fixture = create_brr_oddteams(n)
        drr_fixture = create_drr(fixture)
        teams = teams_number_list(n)
        #teams = ['1', '3', '4', '5', '6', '7', '8', '2']
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator=" v ")
        save_fixture(n, drr_grid, fixturenamesuffix='')
        save_fixture_analysis(n, fixture, drr_fixture,fixturenamesuffix='')
        

def fixtures_odds_balanced():
    """Save text files of all fixtures balanced 5,7,9,11,13,15,17,19,21,23 teams"""
    # not intended for use with even number teams 6...24
    for n in range(5, 24, 2):
        fixture = create_brr_oddteams(n, balanced=True)
        drr_fixture = create_drr(fixture)
        teams = teams_number_list(n)
        #teams = ['1', '3', '4', '5', '6', '7', '8', '2']
        drr_grid = create_fixture_grid(drr_fixture, teams, inmatchseparator=" v ")
        save_fixture(n, drr_grid, fixturenamesuffix='B')
        save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix='B')   # Balanced


def fixtures_even_balanced_special():
    """Save text files of fixtures_balanced for 10,16,22 teams"""
    for n in range(10, 11, 6):
        fixture = balanced10()  # create_brr_evens_forbalanced(n)
        drr_fixture = create_drr_withshift(fixture)
        teams = teams_number_list(n)
        #teams = ['1', '3', '4', '5', '6', '7', '8', '2']
        drr_grid = create_fixture_grid(
            drr_fixture, teams, inmatchseparator="\t")
        save_fixture(n, drr_grid, fixturenamesuffix='_balanced')
        save_fixture_analysis(n, fixture, drr_fixture, fixturenamesuffix='_balanced')

#fixtures_even()
#fixtures_even_1()
#fixtures_last()
#fixtures_even_balanced()
#fixtures_odds()
#fixtures_odds_balanced()

# fixtures_even_balanced_special()





# import ast
# base = ast.literal_eval(balanced10x())
# print(base)
# print(type(base))
# fulllist = []
# for row in base:
#     out = [tuple(row[i: i + 2]) for i in range(0, len(row), 2)]
#     fulllist.append(out)
# print(fulllist)

# base = balanced10x()
# print(type(base))

