import pathlib
import numpy as np
import re
import ast
import copy
import math
from itertools import permutations
import random
from io import StringIO
import timeit

##############################################################################################
#####laod and save files

# def load_fixture(name):
#     """Load text file of fixture with format 1 v 6	2 v 7	3 v 8; file name will be name & .txt"""
#     # use with open since it handles errors and closes the file automatically
#     with open(name + ".txt", "r") as f:
#         filetext = f.read()   #readlines()
#     return filetext

def makedir_for_fixtures(subfoldername):
    """Create a subfolder in this folder to hold the group of fixtures, if the subfolder does not exist."""
    thisfilepath = pathlib.Path(__file__).parent.absolute()
    subfdirpath = thisfilepath / subfoldername
    if pathlib.Path.is_dir(subfdirpath) == False:
        subfdirpath.mkdir(parents=True, exist_ok=False)


def load_fixture_nparray(filename, subfolder="fixtures_even_balanced"):
    """Load text file of fixture format 1 v 6	2 v 7	3 v 8 to np array; file name will be name & .txt"""
    # use with open since it handles errors and closes the file automatically
    thisfiledir = pathlib.Path(__file__).parent.absolute()
    if subfolder == "":
        ftxtpath = thisfiledir / (filename + ".txt")
    else:
        ftxtpath = thisfiledir / subfolder / (filename + ".txt")
    with open(ftxtpath, "r") as f:
        fixture_fromfile = f.read()  # readlines()
    #convert to np array
    fixture_fromfile = re.sub(' v ', ', ', fixture_fromfile)
    fixture_fromfile = re.sub('\t', ', ', fixture_fromfile)
    #13, 12, 8, 2, 3, 6, 9, 15, 4, 5, 10, 16, 11, 14, 1, 7....
    # StringIO behaves like a file object
    strfile = StringIO(fixture_fromfile)
    npfixture = np.loadtxt(strfile, delimiter=', ', dtype='int8')
    #[[13 12  8  2  3  6  9 15  4  5 10 16 11 14  1  7]...
    return npfixture

 

def save_fixture(n, fixture_grid, subfolder="", fixturenamesuffix="permuted", fixtureprefix="FixtureTemplate"):
    """Save text file of fixture_grid; file name will be n & fixturenamesuffix & .txt"""
    # use with open since it handles errors and closes the file automatically
    thisfiledir = pathlib.Path(__file__).parent.absolute()
    if subfolder == "":
        ftxtpath = thisfiledir / (fixtureprefix + str(n) + fixturenamesuffix + ".txt")
    else:
        ftxtpath = thisfiledir / subfolder / (fixtureprefix + str(n) + fixturenamesuffix + ".txt")
    with open(ftxtpath, "w") as f:
        f.write('\n'.join(fixture_grid))


##############################################################################################
#####anaylsis using numpy
##############################################################################################


def nparray_from_fixture(fixture):
    """Return a numpy array for a fixture
    [[(4, 1), (0, 5), (2, 3)], [(3, 5), (4, 0), (1, 2)], ... [(3, 4), (5, 2), (0, 1)]]
    to
    [[4, 1, 0, 5, 2, 3], [3, 5, 4, 0, 1, 2],  ...[3, 4, 5, 2, 0, 1]]
    to
    [[4 1 0 5 2 3]
     [3 5 4 0 1 2]
     ...
     [3 4 5 2 0 1]]
    """
    rows = []
    for row in fixture:
        newrowtup = ()
        for tup in row:
            newrowtup += tup
        newrow = list(newrowtup)
        rows.append(newrow)
    # print(rows)
    npfixture = np.array(rows)
    # print(npfixture)
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
        combined_column_occurrences = column_occurrences[::2] + \
            column_occurrences[1::2]
        # add each row to numpy.ndarray
        if len(all_col_occs) == 0:
            all_col_occs = combined_column_occurrences
        else:
            all_col_occs = np.vstack(
                (all_col_occs, combined_column_occurrences))
    return all_col_occs


def npfixture_analysis_home_and_away(n, npfix):
    """Return str of table of home and away sequences for each team (col) in each round (row)"""
    # npfix = nparray_from_fixture(drr_fixture)
    # make sure n is even
    if n % 2 == 1:
        n = n + 1
    rowscount = npfix.shape[0]
    #init numpy array with '' as each element
    home_for_team_in_each_round = np.zeros((rowscount, n), dtype=str)
    for teamnum in range(n):
        for rowround in range(rowscount):
            row_home_for_team_count = np.count_nonzero(
                npfix[rowround, :n:2] == teamnum)
            if row_home_for_team_count == 1:
                home_for_team_in_each_round[rowround, teamnum] = "H"
            else:
                home_for_team_in_each_round[rowround, teamnum] = "."
    return home_for_team_in_each_round


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
            row_home_for_team_count = np.count_nonzero(
                npfix[rowround, :n:2] == teamnum)
            if row_home_for_team_count == 1:
                home_for_team_in_each_round[rowround, teamnum] = "H"
            else:
                home_for_team_in_each_round[rowround, teamnum] = "."
    return home_for_team_in_each_round


def fixture_analysis_opponent_array(n, drr_fixture):
    """Return str of table of opponet team numbers for each team (col) in each round (row)
     drr_fixture = [[(4, 1), (0, 5), (2, 3)], [(3, 5), (4, 0), (1, 2)], ... [(3, 4), (5, 2), (0, 1)]]
    Use standard list for match tuples and store in numpy array with teams down and rounds across
    """
    # make sure n is even
    if n % 2 == 1:
        n = n + 1
    #create dict with team nos as keys and empty list as values to store round opponents in order
    rowscount = len(drr_fixture)
    # print(drr_fixture)
    team_opponent_arr = np.zeros((n, rowscount), dtype=int)
    # print(team_opponent_arr.shape)
    rnd_num = 0
    for roundmatchlist in drr_fixture:
        for rowmatch in roundmatchlist:
            team1 = rowmatch[0]
            team2 = rowmatch[1]
            # print(rnd_num, team1, team2)
            team_opponent_arr[team1, rnd_num] = team2
            team_opponent_arr[team2, rnd_num] = team1
        rnd_num += 1
    #bumb up 1 from 0 index
    team_opponent_arr = team_opponent_arr + 1
    return team_opponent_arr


def fixture_analysis_1(ha_array):
    """Return str of measure of balance by count of non 1 occurance values for home and away columns"""
    size = np.size(ha_array)
    occurrences1 = np.count_nonzero(ha_array == 1)
    return size - occurrences1


def fixture_analysis_3or4(tablebalance_array):
    """Return str of measure of balance by count of non 3 or 4 occurance values for table locations"""
    size = np.size(tablebalance_array)
    occurrences3 = np.count_nonzero(tablebalance_array == 3)
    occurrences4 = np.count_nonzero(tablebalance_array == 4)
    return size - occurrences3 - occurrences4


def fixture_analysis_runsof3_halffixture(ha_array):
    """Return count of runs of 3 Home (HHH) or 3 Away (...)"""
    hah = (ha_array == 'H')
    hah = hah.astype(np.int)
    haa = (hah - 1)
    haah = haa + hah
    revhaah = haah * -1
    fullhah = np.vstack((haah, revhaah))
    fullhah1 = fullhah[:-2]
    fullhah2 = fullhah[1:-1]
    fullhah3 = fullhah[2:]
    sumhah = fullhah1 + fullhah2 + fullhah3
    runsof3 = np.sum(sumhah == 3) + np.sum(sumhah == -3)
    return runsof3


def fixture_analysis_runsof3(ha_array):
    """Return count of runs of 3 Home (HHH) or 3 Away (...) using single rr as input"""
    hah = (ha_array == 'H')
    hah = hah.astype(np.int)
    #H 1, . 0; now hmake a copy and subtract 1 to get -1 for away
    haa = (hah - 1)
    fullhah = haa + hah
    fullhah1 = fullhah[:-2]
    fullhah2 = fullhah[1:-1]
    fullhah3 = fullhah[2:]
    sumhah = fullhah1 + fullhah2 + fullhah3
    runsof3 = np.sum(sumhah == 3) + np.sum(sumhah == -3)
    return runsof3


def fixture_analysis_runsof3a(ha_array):
    """Return count of runs of 3 Home (HHH) or 3 Away (...); twice as slow as using np arrays"""
    #transpose first so colums put in rows for sequence check
    array_string = str(ha_array.transpose())
    total_runsof3 = 0
    #replace quotes and spaces with empty and remove start [
    array_string = re.sub('\'|\s|\[', '', array_string)
    #replace end] with new line so count works
    array_string = re.sub('\]', '\n', array_string)
    runsof3 = array_string.count('HHH') + array_string.count('...') + \
        array_string.count('HHHH') + array_string.count('....')
    total_runsof3 += runsof3
    return total_runsof3


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


def number_text_rows(text_grid):
    """Return array as a string without quotes, spaces and square brackets"""
    text_grid_list = text_grid.splitlines()
    numbered_text_grid = ''
    teamnum = 0
    for line in text_grid_list:
        teamnum += 1
        if len(line) > 2:
            numbered_text_grid = (numbered_text_grid + str(teamnum) + ':\t' + line + '\n')
    numbered_text_grid_list = str(numbered_text_grid)
    return numbered_text_grid_list


def save_fixture_analysis(n, fixture, drr_fixture, drr_gridnos, subfolder="", fixturenamesuffix="", fixtureprefix="FixtureAnalysis"):
    """Save text file of analysis of fixture; file name will be fixtureprefix & n & fixturenamesuffix & .txt"""
    gridnos = halve_fixture_grid(drr_gridnos)
    fixturegrid = '\n'.join(gridnos)
    drrfixturegrid = '\n'.join(drr_gridnos)
    #
    homeawaytable_array = fixture_analysis_index_pos_count(n, fixture,)
    homeawaytable = array_to_str_for_printing(homeawaytable_array)
    homeawaytable_array_1 = str(fixture_analysis_1(homeawaytable_array))
    #
    tablebalance_array = fixture_analysis_index_table_count(n, drr_fixture)
    tablebalance_string = array_to_str_for_printing(tablebalance_array)
    tablebalance_array_3or4 = str(fixture_analysis_3or4(tablebalance_array))
    #
    homeawaytable_foreachround_array = fixture_analysis_home_and_away(
        n, drr_fixture)
    homeawaytable_foreachround_string = array_to_str_for_printing(
        homeawaytable_foreachround_array)
    runs_of_3 = str(fixture_analysis_runsof3(homeawaytable_foreachround_array))
    #
    opponent_table = fixture_analysis_opponent_array(n, drr_fixture)
    opponent_table_toPrint = array_to_str_for_printing(opponent_table)
    opponent_table_toPrint = number_text_rows(opponent_table_toPrint)
    #
    # use with open since it handles errors and closes the file automatically
    thisfiledir = pathlib.Path(__file__).parent.absolute()
    if subfolder == "":
        ftxtpath = thisfiledir / (fixtureprefix + str(n) + fixturenamesuffix + ".txt")
    else:
        ftxtpath = thisfiledir / subfolder / (fixtureprefix + str(n) + fixturenamesuffix + ".txt")
    with open(ftxtpath, "w") as f:
        f.write('Fixture analysis. ' + str(n) + fixturenamesuffix + '\n\n')
        f.write('Single round robin Fixture grid.\n')
        f.write(fixturegrid)
        f.write('\n\n\n')
        f.write('Double round robin Fixture grid.\n')
        f.write(drrfixturegrid)
        f.write('\n\n\n')
        f.write('Home and Away position count. Row number = index.\n')
        f.write('Counts of 1 are expected. They occur when the team number is only Home (or Away) once on that table in a single round robin fixture.\n')
        f.write('Counts of non 1 in a round robin fixture:  ')
        f.write(homeawaytable_array_1)
        f.write('\n')
        f.write(homeawaytable)
        f.write('\n')
        f.write('Match/Table count. Row number = index.\n')
        f.write('Counts of 3 or 4 are expected. They occur when the team numbers plays on that table in a double round robin fixture.\n')
        f.write('Counts of non 3 or 4 in a double round robin fixture:  ')
        f.write(tablebalance_array_3or4)
        f.write('\n')
        f.write(tablebalance_string)
        f.write('\n')
        f.write('Home and Away vertical sequence for each team number.\n')
        f.write('Runs of 3: ')
        f.write(runs_of_3)
        f.write('\n')
        f.write(homeawaytable_foreachround_string)
        f.write('Opponents by round:\n')
        f.write(opponent_table_toPrint)
        f.write('\n')



##############################################################################################
#####check fixtures runs of 3
##############################################################################################

def create_np_drr(npfixture):
    """Return double np fixture, reversing HA in second half of RoundRobin"""
    #use indices to rearrange
    n = np.size(npfixture, axis=1)
    col_indices = range(n)
    #np.concatenate converts the tuples into list elements
    #print(col_indices[1::2], col_indices[0::2])
    np_col_indices = np.concatenate(list(zip(col_indices[1::2], col_indices[0::2])))
    #print(np_col_indices)
    npfixture2 = npfixture[:, np_col_indices]
    #print(npfixture2)
    #add second half of double round robin reversing HA  
    npdrrfixture = np.vstack((npfixture, npfixture2))
    return npdrrfixture


def create_np_drr_shiftright(npfixture):
    """Return double np fixture shifted 2 col teams to right, reversing HA in second half of RoundRobin"""
    #use indices to rearrange
    n = np.size(npfixture, axis=1)
    col_indices = range(n)
    #np.concatenate converts the tuples into list elements
    #print(col_indices[1::2], col_indices[0::2])
    np_col_indices = np.concatenate(list(zip(col_indices[1::2], col_indices[0::2])))
    np_col_indices = np.roll(np_col_indices, 2)
    npfixture2 = npfixture[:, np_col_indices]
    #print(npfixture2)
    #add second half of double round robin reversing HA
    npdrrfixture = np.vstack((npfixture, npfixture2))
    return npdrrfixture


def fixture_runs(n, npfixture):
    """Return runs of 3 in fixture; fixture is a np 2D array"""
    ha_foreachround_array = npfixture_analysis_home_and_away(n, npfixture)
    #print(ha_foreachround_array)
    runs_of_3 = fixture_analysis_runsof3(ha_foreachround_array)
    return runs_of_3

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


def halve_fixture_grid(fixturegrid):
    """Return half of a fixture grid list; half the lines are returned."""
    return fixturegrid[:(len(fixturegrid)//2)]

    
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


def fixture_from_npfixture(npfixture):
    """Return a fixture from nparray
    [[4 1 0 5 2 3]
    [3 5 4 0 1 2]
    ...
    [3 4 5 2 0 1]]
    to
    [[4, 1, 0, 5, 2, 3], [3, 5, 4, 0, 1, 2],  ...[3, 4, 5, 2, 0, 1]]
    to
    [[(4, 1), (0, 5), (2, 3)], [(3, 5), (4, 0), (1, 2)], ... [(3, 4), (5, 2), (0, 1)]]
    """
    #convert to a list first to get comma separators instead of space
    fixture = npfixture.tolist()
    # print(fixture)
    #in each sublist group pairs of elements into tuples
    rows=[]
    for row in fixture:
        #this also works: newrow = [tuple(row[i: i + 2]) for i in range(0, len(row), 2)]
        newrow = list(zip(row[0::2], row[1::2]))
        rows.append(newrow)
    #print(rows)
    return rows

#####################################################################################################
#1,000,000 30 min for 16; 60 min for 22


def permute1_random_balanced_fixture(filename="FixtureTemplate10B"):
    """Save randomised rows in balanced fixture"""
    subfoldername = "fixtures_even_balanced"
    makedir_for_fixtures(subfoldername)
    npfixture = load_fixture_nparray(filename, subfolder=    makedir_for_fixtures(subfoldername))
    #[[0 5 1 6 2 7 3 8 4 9]...
    # #renumber each number to 1 less to be able to use the rest of the scripts
    npfixture = npfixture - 1
    #n = fixture_team_count
    n = np.size(npfixture, axis=1)
    fixture_row_count = np.size(npfixture, axis=0)
    fixture_row_count_half = fixture_row_count // 2
    #split in half for permuting each halves using permute vector on each
    npfixture1 = npfixture[:fixture_row_count_half]
    npfixture2 = npfixture[fixture_row_count_half:]
    row_indices = list(range(fixture_row_count_half))
    random.shuffle(row_indices)
    new_npfixture1 = npfixture1[row_indices]  # ,:]
    new_npfixture2 = npfixture2[row_indices]
    new_npfixture = np.vstack((new_npfixture1, new_npfixture2))
    #convert to fixture list for saving and analysis
    npfixture_list = fixture_from_npfixture(new_npfixture)
    npfixture_list_half = npfixture_list[:fixture_row_count_half]
    teams = teams_number_list(n)
    drr_grid = create_fixture_grid(npfixture_list, teams, inmatchseparator=" v ")
    drr_gridnos = create_fixture_grid(npfixture_list, teams, inmatchseparator="\t")
    #
    save_fixture(n, drr_grid, subfolder=subfoldername, fixturenamesuffix='B')
    save_fixture_analysis(n, npfixture_list_half, npfixture_list, drr_gridnos, subfolder=subfoldername, fixturenamesuffix='B')


def permute_random_balanced_fixtures(filename="FixtureTemplate10B", permutes = 100):
    """Save balanced fixture with reduced number of runs; manually choose file and length of tries"""
    subfoldername = "fixtures_even_balanced"
    makedir_for_fixtures(subfoldername)
    npfixture = load_fixture_nparray(filename, subfolder=subfoldername)
    #[[0 5 1 6 2 7 3 8 4 9]...
    # #renumber each number to 1 less to be able to use the rest of the scripts
    npfixture = npfixture - 1
    #n = fixture_team_count
    n = np.size(npfixture, axis=1)
    fixture_row_count = np.size(npfixture, axis=0)
    fixture_row_count_half = fixture_row_count // 2
    #split in half for permuting each halves using permute vector on each
    npfixture1 = npfixture[:fixture_row_count_half]
    npfixture2 = npfixture[fixture_row_count_half:]
    #get runs for fixture; use half fixture as arguemnt which is used to make full fixture H. in def
    best_fixture_runs_count = fixture_runs(n, npfixture1)
    #print(best_fixture_runs_count)
    best_npfixture = npfixture
    row_indices = list(range(fixture_row_count_half))
    #random indices required for 12+ teams, so use random appraoch; 50000 reps is about 35sec
    for i in range(permutes):
        random.shuffle(row_indices)
        new_npfixture1 = npfixture1[row_indices]  #,:]
        new_fixture_runs_count = fixture_runs(n, new_npfixture1)
        if new_fixture_runs_count < best_fixture_runs_count:
            new_npfixture2 = npfixture2[row_indices]
            new_npfixture = np.vstack((new_npfixture1, new_npfixture2))
            best_fixture_runs_count = copy.deepcopy(new_fixture_runs_count)
            best_npfixture = copy.deepcopy(new_npfixture)
        if best_fixture_runs_count == 0:
            new_npfixture2 = npfixture2[row_indices]
            new_npfixture = np.vstack((new_npfixture1, new_npfixture2))
            break
    #convert to fixture list for saving and analysis
    best_npfixture_list = fixture_from_npfixture(best_npfixture)
    best_npfixture_list_half = best_npfixture_list[:fixture_row_count_half]
    teams = teams_number_list(n)
    drr_grid = create_fixture_grid(best_npfixture_list, teams, inmatchseparator=" v ")
    drr_gridnos = create_fixture_grid(best_npfixture_list, teams, inmatchseparator="\t")
    #
    save_fixture(n, drr_grid, subfolder=subfoldername, fixturenamesuffix='B')
    save_fixture_analysis(n, best_npfixture_list_half, best_npfixture_list, drr_gridnos, subfolder=subfoldername, fixturenamesuffix='B')


#####################################################################################################
#7min per use

def permute_balanced_fixtures_parts(filename="FixtureTemplate10B", section=1):
    """Save balanced fixture with reduced number of runs for 12 or more teams; specify filename without extension .txt.
    Use perms of 9. Specify section 1 for top to permute, 2 for middle or 3 for bottom."""
    npfixture = load_fixture_nparray(filename, subfolder="fixtures_even_balanced")
    #[[13 12  8  2  3  6  9 15  4  5 10 16 11 14  1  7]...

    #renumber each number to 1 less to be able to use the rest of the scripts
    npfixture = npfixture - 1
    #[[0 5 1 6 2 7 3 8 4 9]

    #n = fixture_team_count
    n = np.size(npfixture, axis=1)
    fixture_row_count = np.size(npfixture, axis=0)
    fixture_row_count_half = fixture_row_count // 2
    npfixture_half = npfixture[:fixture_row_count_half]

    ########################
    #split top half for permuting; ignore bottom half
    if section == 1:
        #perm top
        npfixture1 = npfixture_half[:9]
        npfixture2 = npfixture_half[9:]
    elif section == 2:
        #mid
        cutoff1 = (fixture_row_count_half - 9)//2
        cutoff2 = cutoff1 + 9
        npfixture1 = npfixture[:cutoff1]
        npfixture2 = npfixture[cutoff1:cutoff2]
        npfixture3 = npfixture[cutoff2:]
    elif section == 3:
        #perm bot
        cutoff = fixture_row_count_half - 9
        npfixture1 = npfixture[:cutoff]
        npfixture2 = npfixture[cutoff:]
    #get runs for full fixture, using half as input
    best_fixture_runs_count = fixture_runs(n, npfixture_half)
    #print(best_fixture_runs_count)
    best_npfixture_half = npfixture_half
    row_indices = list(range(fixture_row_count_half))
    #######################
    #use all perms 9 rows at a time; 362880
    perms = permutations(range(9))
    # counter = 1
    for row_indices in perms:
        # counter += 1
        # if counter > 362880:
        #     break
        if section == 1:
            new_npfixture1 = npfixture1[row_indices, :]
            new_npfixture_half = np.vstack((new_npfixture1, npfixture2))
            new_fixture_runs_count = fixture_runs(n, new_npfixture_half)
            if new_fixture_runs_count < best_fixture_runs_count:
                best_fixture_runs_count = copy.deepcopy(new_fixture_runs_count)
                best_npfixture_half = copy.deepcopy(new_npfixture_half)
            if best_fixture_runs_count == 0:
                break
        elif section == 2:
            new_npfixture2 = npfixture2[row_indices, :]
            new_npfixture_half = np.vstack((npfixture1, new_npfixture2, npfixture3))
            new_fixture_runs_count = fixture_runs(n, new_npfixture_half)
            if new_fixture_runs_count < best_fixture_runs_count:
                best_fixture_runs_count = copy.deepcopy(new_fixture_runs_count)
                best_npfixture_half = copy.deepcopy(new_npfixture_half)
            if best_fixture_runs_count == 0:
                break
        elif section == 3:
            new_npfixture2 = npfixture2[row_indices, :]
            new_npfixture_half = np.vstack((npfixture1, new_npfixture2))
            new_fixture_runs_count = fixture_runs(n, new_npfixture_half)
            if new_fixture_runs_count < best_fixture_runs_count:
                best_fixture_runs_count = copy.deepcopy(new_fixture_runs_count)
                best_npfixture_half = copy.deepcopy(new_npfixture_half)
            if best_fixture_runs_count == 0:
                break
    #create full np fixture
    best_npfixture = create_np_drr_shiftright(best_npfixture_half)
    #convert to fixture list for saving and analysis
    best_npfixture_list = fixture_from_npfixture(best_npfixture)
    best_npfixture_list_half = best_npfixture_list[:fixture_row_count_half]
    teams = teams_number_list(n)
    drr_grid = create_fixture_grid(best_npfixture_list, teams, inmatchseparator=" v ")
    drr_gridnos = create_fixture_grid(best_npfixture_list, teams, inmatchseparator="\t")
    #
    subfoldername = "fixtures_even_balanced"
    makedir_for_fixtures(subfoldername)
    save_fixture(n, drr_grid, subfolder=subfoldername, fixturenamesuffix='B')
    save_fixture_analysis(n, best_npfixture_list_half, best_npfixture_list, drr_gridnos, subfolder=subfoldername, fixturenamesuffix='B')
 


##########################################################################################
#########for coverting output for 10,16,22 into lists for storing in libraries
##########################################################################################


def fixture_list_from_saved_fixture(filename="FixtureTemplate10B"):
    """[summary]return fixture in list format:
    Convert from saved fixture to fixture list; useful for storing library lists of fixtures.
    Args:
        filename (str, optional): [description]. Defaults to "FixtureTemplate10B".
    """
    npfixture = load_fixture_nparray(filename, subfolder="fixtures_even_balanced")
    #[[13 12  8  2  3  6  9 15  4  5 10 16 11 14  1  7]...
    #renumber each number to 1 less to be able to use the rest of the scripts
    npfixture = npfixture - 1
    #[[0 5 1 6 2 7 3 8 4 9] ...
    fixture_row_count = np.size(npfixture, axis=0)
    fixture_row_count_half = fixture_row_count // 2
    #split in half
    npfixture1 = npfixture[:fixture_row_count_half]
    #convert to fixture list with tuples for each match
    npfixture_list = fixture_from_npfixture(npfixture1)
    #[[(1, 6), (2, 7), (3, 8), (4, 9), (5, 10)],...
    print(npfixture_list)


#fixture_list_from_saved_fixture(filename="FixtureTemplate16B")

##########################################################################################
def updateFixtureTemplates_all():
    """[summary]Save fixture analysis for even balanced for 8, 10, 12, 14, 16, 18, 20, 22, 24 teams."""
    for n in range(8, 25, 2):
        filename_perm = "FixtureTemplate" + str(n) + "B"
        #do one permute just to reload fixture and save updated analysis
        permute_random_balanced_fixtures(filename=filename_perm, permutes=1)


# updateFixtureTemplates_all()

#12 min for 16 teams 1234567 reps
# filename_perm = "FixtureTemplate16B"
# filename_perm = "FixtureTemplate20B"
# filename_perm = "FixtureTemplate22B"
filename_perm = "FixtureTemplate16B"
for i in range(3):
    permute_balanced_fixtures_parts(filename=filename_perm, section=1)
    permute_balanced_fixtures_parts(filename=filename_perm, section=3)
    permute_balanced_fixtures_parts(filename=filename_perm, section=2)

# for i in range(2):
#     permute_random_balanced_fixtures(filename=filename_perm, permutes=1234567)

#7 min for 12; 10 min for 14; 17min for 18; 21 min for 20; 30 min for 24;    per repeat with all 3 used once





