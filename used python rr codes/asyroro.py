'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# asyroro.py: ASYnchronous ROund-RObin tournaments
# Author: Rolf Sander (2017)
# Version: 1.0
# http://www.rolf-sander.net/software/asyroro

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np

def range1(n):
    # range1 goes from 1 to n (unlike range which goes from 0 to n-1)
    return [i+1 for i in range(n)]

def regularize(pairings, verbose=False):
    if verbose: print('--- Regularize ---')
    # turn pairings into a regular tournament, i.e. ensure that all
    # teams have (almost) the same number of "home" games, where a
    # "home" team is the first team that is mentioned in a game:
    #   (A-B) --> A=home, B=away
    # For example, in a tournament with 3 teams, the order of teams in
    # the game (A-C) must be swapped here:
    #   (A-B) (A-C) (B-C) --> (A-B) (C-A) (B-C)
    for i in range(len(pairings)):
        team0 = np.min(pairings[i])
        team1 = np.max(pairings[i])
        # "team1 % 2" <=> team1 is odd
        # "team0<(team1+1)//2" <=> team0 is in the first half
        # higher number first if either:
        # team1 is odd AND team0 is in 2nd half
        # or:
        # team1 is even AND team0 is in 1st half
        if ((team1 % 2) ^ (team0<(team1+1)//2)): # ^ is xor
            pairings[i] = (team1, team0)
        else:
            pairings[i] = (team0, team1)
        if verbose:
            print('%4d (%s-%s) --> (%s-%s)' % (
                i+1, teamname(team0), teamname(team1),
                teamname(pairings[i][0]), teamname(pairings[i][1])))
    return pairings

def make_schedule(N_teams, verbose=False):
    if (N_teams % 2): # if odd:
        pairings = make_schedule_suksumpong(N_teams, verbose)
    else: # if even:
        pairings = make_schedule_circlemethod(N_teams, verbose)
    return pairings

def make_schedule_circlemethod(N_teams, verbose=False):
    if verbose: print('--- Circle Method ---')
    N_games = N_teams * (N_teams-1) // 2
    pairings = np.full((N_games, 2), -1, dtype=int)
    print(pairings)
    rotarray = range(1,N_teams) # create rotating array
    for j in range(N_teams-1): # rounds
        # add zero at beginning to obtain full array:
        fullarray = np.insert(rotarray, 0, 0) # (array, pos, val)
        for i in range(N_teams//2): # games in this round
            game = j*(N_teams//2) + i + 1 # game number (starting with 1)
            pairings[game-1,0] = fullarray[i]
            pairings[game-1,1] = fullarray[-i-1]
            if verbose: print(game, '(', fullarray[i]+1, fullarray[-i-1]+1, ')',)
        if verbose: print()
        rotarray = np.roll(rotarray,1)
    pairings = regularize(pairings, verbose)
    return pairings

def make_schedule_suksumpong(N_teams, verbose=False):
    if verbose: print('--- Suksumpong Method ---')
    N_games = N_teams * (N_teams-1) // 2
    k = N_teams // 2 # number of games in a round
    pairings = np.full((N_games, 2), -1, dtype=int)
    for j in range1(N_teams): # 1 <= j <= N_teams
        for i in range1(k): # 1 <= i <= k
            # item 1:
            if (j<=2*i):
                slot = i % (k+1)
            else:
                slot = (i + j-2*i) % (k+1)
            game = (j-1)*k + slot # game number (starting with 1)
            team = 2*i-1
            if verbose: print(' i = ', i, 'round = ', j, ' team', team, '-> slot = ', slot,)
            if (slot>0):
                if verbose: print(' = game ', game)
                if (pairings[game-1,0]==-1): # first team assigned to this game?
                    pairings[game-1,0] = team-1
                else:
                    pairings[game-1,1] = team-1
            else:
                if verbose: print(' no game ')
            # item 2:
            if (j<=2*k+3-2*i):
                slot = (i+j-1) % (k+1)
            else:
                slot = (2*k+2-i) % (k+1)
            game = (j-1)*k + slot # game number (starting with 1)
            team = 2*i
            if verbose: print(' i = ', i, 'round = ', j, ' team', team, '-> slot = ', slot,)
            if (slot>0):
                if verbose: print(' = game ', game)
                if (pairings[game-1,0]==-1): # first team assigned to this game?
                    pairings[game-1,0] = team-1
                else:
                    pairings[game-1,1] = team-1
            else:
                if verbose: print(' no game ')
        # item 3:
        slot = j // 2
        game = (j-1)*k + slot # game number (starting with 1)
        team = 2*k+1
        if verbose: print(' i = ', i, 'round = ', j, ' team', team, '-> slot = ', slot,)
        if (slot>0):
            if verbose: print(' = game ', game)
            if (pairings[game-1,0]==-1): # first team assigned to this game?
                pairings[game-1,0] = team-1
            else:
                pairings[game-1,1] = team-1
        else:
            if verbose: print(' no game ')
    pairings = regularize(pairings, verbose)
    return pairings


def printteams(N_teams):
    for oneteam in range(N_teams):
        print('%2s' % (teamname(oneteam)),)
    print(' ',)


def teamname(number):
    return chr(number+65)


def evaluate_schedule(pairings, verbose=False):
    if verbose: print('--- Evaluate Schedule ---')
    N_teams = np.max(pairings)+1
    N_games = len(pairings)
    print_team_summary(pairings)
    print_game_summary(pairings)
    gamesplayed = [0] * N_teams
    resttime = [N_teams*N_teams] * N_teams
    minresttime = [N_teams*N_teams] * N_teams
    maxresttime = [0] * N_teams
    lastgame = [-1] * N_teams
    homecount = [0] * N_teams
    gamesplayeddiff = [0] * N_games
    restdiffidx = [0] * N_games # rest difference index
    if verbose:
        print('Game Teams   Games played %s Last game %s Rest time %s GPD RDI' % (
            ' '*(3*N_teams-12), ' '*(3*N_teams-9), ' '*(3*N_teams-11)))
        print('           ',)
        printteams(N_teams)
        printteams(N_teams)
        printteams(N_teams)
        print()
    for i in range(N_games):
        team0 = pairings[i,0]
        team1 = pairings[i,1]
        homecount[team0] += 1 # team0 is first
        gamesplayed[team0] += 1
        gamesplayed[team1] += 1
        restdiffidx[i] = abs(lastgame[team0]-lastgame[team1])
        if (gamesplayed[team0]>1):
            newresttime = i - lastgame[team0] - 1
            minresttime[team0] = min(minresttime[team0], newresttime)
            maxresttime[team0] = max(maxresttime[team0], newresttime)
            resttime[team0] = newresttime
        if (gamesplayed[team1]>1):
            newresttime = i - lastgame[team1] - 1
            minresttime[team1] = min(minresttime[team1], newresttime)
            maxresttime[team1] = max(maxresttime[team1], newresttime)
            resttime[team1] = newresttime
        lastgame[team0] = i
        lastgame[team1] = i
        gamesplayeddiff[i] = np.amax(gamesplayed) - np.amin(gamesplayed)
        if verbose:
            print('%4d (%s-%s)' % (i+1, teamname(team0), teamname(team1)),)
            print(('['+' '.join(['%2d']*len(gamesplayed))+']') % tuple(gamesplayed),)
            print(('['+' '.join(['%2d']*len(lastgame))+']') % (tuple([j+1 for j in lastgame])),)
            #print(('['+' '.join(['%2d']*len(resttime))+']') % tuple(np.ma.masked_equal(resttime, N_teams*N_teams)),)
            print(gamesplayeddiff[i], ' ', restdiffidx[i])

    print('GRT = guaranteed (minimum) rest time = ',)
    print(np.min(minresttime), minresttime)
    print('      maximum rest time              = ',)
    print(np.max(maxresttime), maxresttime)
    print('GPD = games played difference        = ',)
    print(np.max(gamesplayeddiff)) #, gamesplayeddiff
    print('RDI = rest difference index          = ',)
    print(np.max(restdiffidx)) #, restdiffidx
    print('TII = tournament irregularity index  = ',)
    print(np.amax(homecount)-np.amin(homecount), homecount)
    print()


def print_team_summary(pairings, teamnames=[]):
    N_teams = np.max(pairings)+1
    print('%d teams: ' % (N_teams),)
    for i in range(N_teams):
        if (teamnames):
            print(teamnames[i],)
        else:
            print(teamname(i),)
    print()


def print_game_summary(pairings, teamnames=[]):
    N_games = len(pairings)
    print('%d games:' % (N_games),)
    for i in range(N_games):
        print('(%s-%s)' % (teamname(pairings[i,0]), teamname(pairings[i,1])),)
    print()


def print_schedule(pairings, teamnames=[]):
    print_team_summary(pairings, teamnames)
    N_games = len(pairings)
    print('Game schedule:')
    for i in range(N_games):
        team0 = pairings[i,0]
        team1 = pairings[i,1]
        if (teamnames):
            maxlength = max(len(name) for name in teamnames)
            print('{:>4}: {:<{width}} - {:<{width}}'.format(
                i+1, teamnames[team0], teamnames[team1],width=maxlength))
        else:
            print('%4d %s - %s' % (i+1, teamname(team0), teamname(team1)))
    print()


def print_example(number, description):
    HLINE =  "-" * 78
    print(HLINE)
    print('Example %d: %s' % (number, description))
    print(HLINE, '\n')


'''
if __name__ == '__main__':
    #----------------------------------------------------------------------
    print_example(1, 'A very detailed evaluation')
    pairings = make_schedule(5, verbose=True)
    evaluate_schedule(pairings, verbose=True)
    #----------------------------------------------------------------------
    print_example(2, 'Analyze schedule quality for several tournament sizes')
    for N_teams in (3,5,6,7):
        pairings = make_schedule(N_teams)
        evaluate_schedule(pairings)
    #----------------------------------------------------------------------
    print_example(3, 'Create schedule with individual teamnames')
    teamnames = [ 'Allstars', 'Bulldogs', 'Caribous', 'Dragons', 'Eagles']
    # create the schedule:
    pairings = make_schedule(len(teamnames))
    # print(the schedule:
    print_schedule(pairings, teamnames)
    #----------------------------------------------------------------------
'''

print_example(1, 'A very detailed evaluation')
pairings = make_schedule(6, verbose=False)
evaluate_schedule(pairings, verbose=True)
#----------------------------------------------------------------------
# print_example(2, 'Analyze schedule quality for several tournament sizes')
# for N_teams in (3,5,6,7):
#     pairings = make_schedule(N_teams)
#     evaluate_schedule(pairings)
# #----------------------------------------------------------------------
# print_example(3, 'Create schedule with individual teamnames')
# teamnames = [ 'Allstars', 'Bulldogs', 'Caribous', 'Dragons', 'Eagles']
# # create the schedule:
# pairings = make_schedule(len(teamnames))
# # print(the schedule:
# print_schedule(pairings, teamnames)
