from vb2py.vbfunctions import *
from vb2py.vbdebug import *

def library(n):
    #n = (10, 16, 22, 28, 34, 40, 46, 52, 58, 64)
    if n == 10:
        return liblist10()
    elif n == 16:
        return liblist16()
    elif n == 22:
        return liblist22()
    else:
        return ""


def liblist10():
    return '[[0, 5, 1, 6, 2, 7, 3, 8, 4, 9],\
    [4, 1, 0, 2, 6, 3, 9, 7, 8, 5],\
    [3, 2, 9, 8, 4, 0, 5, 6, 7, 1],\
    [1, 9, 5, 7, 8, 6, 4, 2, 3, 0],\
    [2, 8, 4, 3, 9, 5, 0, 1, 6, 7],\
    [9, 6, 2, 5, 3, 1, 7, 4, 0, 8],\
    [8, 7, 3, 9, 5, 4, 6, 0, 1, 2],\
    [6, 4, 7, 0, 1, 8, 2, 9, 5, 3],\
    [7, 3, 8, 4, 0, 9, 1, 5, 2, 6]]'


def liblist16():
    return'[[2, 3, 8, 13, 1, 6, 12, 15, 10, 11, 0, 5, 14, 9, 4, 7], \
    [5, 4, 9, 11, 8, 15, 2, 6, 12, 13, 1, 3, 0, 7, 10, 14], \
    [0, 1, 10, 12, 11, 14, 5, 7, 9, 8, 2, 4, 3, 6, 15, 13], \
    [6, 7, 5, 3, 4, 0, 9, 10, 15, 14, 13, 11, 8, 12, 2, 1], \
    [12, 11, 7, 1, 2, 5, 8, 14, 3, 4, 9, 15, 10, 13, 0, 6], \
    [14, 13, 0, 2, 3, 7, 4, 1, 5, 6, 8, 10, 15, 11, 9, 12], \
    [15, 10, 4, 6, 9, 13, 3, 0, 7, 2, 14, 12, 5, 1, 11, 8], \
    [8, 0, 3, 10, 6, 12, 14, 5, 11, 7, 4, 9, 1, 15, 13, 2], \
    [11, 2, 1, 9, 15, 4, 7, 13, 8, 5, 10, 6, 12, 3, 14, 0], \
    [4, 14, 12, 7, 10, 2, 1, 8, 13, 3, 15, 0, 9, 5, 6, 11], \
    [13, 6, 15, 5, 0, 9, 11, 3, 14, 1, 12, 2, 7, 10, 8, 4], \
    [3, 15, 13, 0, 5, 11, 6, 9, 4, 12, 7, 14, 2, 8, 1, 10], \
    [1, 12, 2, 14, 7, 8, 10, 4, 6, 15, 5, 13, 11, 0, 3, 9], \
    [7, 9, 11, 4, 13, 1, 15, 2, 0, 10, 3, 8, 6, 14, 12, 5], \
    [10, 5, 6, 8, 14, 3, 0, 12, 2, 9, 11, 1, 13, 4, 7, 15]]'


def liblist22():
    return '[[0, 11, 1, 12, 2, 13, 3, 14, 4, 15, 5, 16, 6, 17, 7, 18, 8, 19, 9, 20, 10, 21], \
    [1, 10, 13, 11, 3, 12, 2, 4, 16, 14, 17, 15, 5, 7, 8, 6, 18, 20, 21, 19, 0, 9], \
    [2, 9, 3, 10, 11, 15, 1, 5, 13, 6, 14, 18, 4, 8, 16, 20, 17, 21, 7, 0, 19, 12], \
    [8, 3, 20, 15, 21, 16, 11, 17, 18, 12, 19, 13, 14, 9, 10, 4, 5, 0, 6, 1, 7, 2], \
    [4, 7, 5, 8, 9, 6, 21, 18, 11, 19, 12, 20, 2, 10, 3, 0, 15, 1, 13, 16, 17, 14], \
    [6, 5, 18, 17, 8, 7, 19, 20, 10, 9, 11, 21, 1, 0, 12, 13, 3, 2, 15, 14, 16, 4], \
    [21, 1, 2, 0, 12, 14, 13, 15, 5, 3, 6, 4, 16, 18, 19, 17, 7, 9, 10, 8, 11, 20], \
    [20, 2, 14, 21, 0, 4, 12, 16, 17, 13, 3, 7, 15, 19, 5, 9, 6, 10, 18, 11, 8, 1], \
    [3, 19, 9, 4, 10, 5, 0, 6, 7, 1, 8, 2, 20, 14, 21, 15, 16, 11, 17, 12, 18, 13], \
    [18, 4, 16, 19, 20, 17, 10, 7, 0, 8, 1, 9, 13, 21, 14, 11, 12, 15, 2, 5, 6, 3], \
    [5, 17, 7, 6, 19, 18, 8, 9, 21, 20, 0, 10, 12, 11, 1, 2, 14, 13, 4, 3, 15, 16], \
    [12, 21, 11, 2, 1, 3, 4, 13, 14, 5, 15, 6, 7, 16, 17, 8, 9, 18, 19, 10, 20, 0], \
    [13, 20, 21, 3, 4, 11, 5, 12, 6, 2, 7, 14, 8, 15, 9, 16, 10, 17, 0, 18, 1, 19], \
    [19, 14, 4, 20, 5, 21, 6, 11, 12, 7, 13, 8, 9, 3, 15, 10, 0, 16, 1, 17, 2, 18], \
    [15, 18, 19, 5, 6, 20, 7, 21, 8, 11, 9, 12, 10, 13, 0, 14, 1, 4, 16, 2, 3, 17], \
    [17, 16, 6, 18, 7, 19, 20, 8, 9, 21, 10, 11, 0, 12, 13, 1, 2, 14, 3, 15, 4, 5], \
    [10, 12, 0, 13, 14, 1, 15, 2, 3, 16, 4, 17, 18, 5, 6, 19, 20, 7, 8, 21, 9, 11], \
    [9, 13, 10, 14, 15, 0, 16, 1, 2, 17, 18, 3, 19, 4, 20, 5, 21, 6, 11, 7, 12, 8], \
    [14, 8, 15, 9, 16, 10, 17, 0, 1, 18, 2, 19, 3, 20, 4, 21, 11, 5, 12, 6, 13, 7], \
    [7, 15, 8, 16, 17, 9, 18, 10, 19, 0, 20, 1, 21, 2, 11, 3, 4, 12, 5, 13, 14, 6], \
    [16, 6, 17, 7, 18, 8, 9, 19, 20, 10, 21, 0, 11, 1, 2, 12, 13, 3, 14, 4, 5, 15]]'

def RoundRobin(n, ha, doub, Rand, byes):
    test = "test"
    i = Integer()
    j = Integer()
    k = Integer()
    hbRound = Integer()
    nRound = Integer()
    hbCourt = Integer()
    Odd = Integer()
    step = Integer()
    s = String()
    RR = vbObjectInitialize(objtype=Integer)
    # Generate a round robin schedule for n players (or teams) and return it as a three
    # dimensional array. If ha is false then the 1st dimension of the array indexes
    # the left and right side of each match, but when ha is true the 1st dim indexes
    # the location (home or away) for a team's match.  The second dimension of the array
    # indexes the round number, the third dimension the match number within a round.
    # if n is odd then then byes will be a vector with the team number in each round who
    # has the bye, when n=even byes will be empty.  If doub is set to true then then
    # a double-round robin schedule is returned with twice as many rounds.
    if n < 3:
        return None
    hbCourt = (n // 2) - 1
    Odd = n % 2
    nRound = n + Odd - 1
    if doub:
        RR = vbObjectInitialize(
            ((0, 1), (0, 2 * nRound - 1), (0, hbCourt),), Integer)
    else:
        RR = vbObjectInitialize(
            ((0, 1), (0, nRound - 1), (0, hbCourt),), Integer)
    #print(RR[0, 0, i], RR[1, 0, i])
    if Odd == 1:
        # In unrandomised form the team with a bye will be the same as the round number
        if doub:
            byes = vbObjectInitialize(((0, 2 * nRound - 1),), Variant)
        else:
            byes = vbObjectInitialize(((0, nRound - 1),), Variant)
        for i in vbForRange(0, nRound - 1):
            byes[i] = i + 1
            if doub:
                byes[i + nRound] = i + 1
    else:
        byes = False
    # Read special cases of the court balanced design from the library worksheet
    # These are n=(10,16,22,28,34,40,46,52,58,64)
    if (ha == False) and (n >= 10) and (n <= 64) and ((n % 6) == 4):
        #k = (n * n - 8 * n - 8) // 12
        for i in vbForRange(0, nRound - 1):
            s = library(n)
            for j in vbForRange(0, hbCourt):
                RR[0, i, j] = AscB(Mid(s, j * 2 + 1, 1)) - 47
                RR[1, i, j] = AscB(Mid(s, j * 2 + 2, 1)) - 47
    else:
        # Set up the first round of the schedule
        RR[0, 0, 0] = Odd - 1
        #added to set 0 ;
        # RR[1, 0, 0] = 0
        for i in vbForRange(1, hbCourt + Odd):
            #print(i)
            RR[0, 0, i - Odd] = i
            RR[1, 0, i - Odd] = nRound - i
            #print(RR[0, 0, i], RR[1, 0, i])
            # For home and away swap around alternate matches in the first row
            if ha and ((i % 2) == 1):
                k = RR(0, 0, i - Odd)
                RR[0, 0, i - Odd] = RR(1, 0, i - Odd)
                RR[1, 0, i - Odd] = k
        # Remaining rounds are generated by adding the value 'step' to each element from the
        # previous round. Note that -1 represents the infinite element and remains unchanged.
        if (Odd == 0) and ((n % 3) != 1) and (not ha):
            step = hbCourt
        else:
            step = 1
        for i in vbForRange(1, nRound - 1):
            for j in vbForRange(0, hbCourt):
                for k in vbForRange(0, 1):
                    if RR(k, i - 1, j) >= 0:
                        RR[k, i, j] = (RR(k, i - 1, j) + step) % nRound
                    else:
                        RR[k, i, j] = -1
                #print(RR[0, i, j], RR[1, i, j])
        # distribute any -1s evenly between home and away
        if ha and (Odd == 0):
            for i in vbForRange(1, nRound - 2, 2):
                #print(RR[1, i, 0], end=" ")
                RR[0, i, 0] = RR(1, i, 0)
                RR[1, i, 0] = -1
                #print(RR[0, i, 0], [1, i, 0], end=" ")
        # if possible rearrange the schedule to obtain court balance
        if step > 1:
            for j in vbForRange(1, hbCourt):
                RR[0, j - 1, 0] = RR(0, j - 1, j)
                k = RR(1, j - 1, 0)
                RR[1, j - 1, 0] = RR(1, j - 1, j)
                RR[0, j - 1, j] = - 1
                RR[1, j - 1, j] = k
            # For the matches that are swapped below, the left player is also swapped for the
            # right player. This gives a schedule with side balance. So where players play twice
            # at a venue, they play once on the left and once on the right.
            for j in vbForRange(hbCourt, 1, - 1):
                RR[0, nRound - j - 1, 0] = RR(1, nRound - j - 1, j)
                k = RR(1, nRound - j - 1, 0)
                RR[1, nRound - j - 1, 0] = RR(0, nRound - j - 1, j)
                RR[1, nRound - j - 1, j] = - 1
                RR[0, nRound - j - 1, j] = k
        # finally adjust the whole schedule so that the elements are numbered 1...n
        k = 2 - Odd
        for i in vbForRange(0, nRound - 1):
            for j in vbForRange(0, hbCourt):
                RR[0, i, j] = RR(0, i, j) + k
                RR[1, i, j] = RR(1, i, j) + k
    if doub:
        if ha and (Odd == 0):
            # for ha need to fix it so that three H or three A across the join is avoided (see IA p162)
            k = RR(0, nRound - 2, 0)
            RR[0, nRound - 2, 0] = RR(1, nRound - 2, 0)
            RR[1, nRound - 2, 0] = k
            k = RR(0, nRound - 1, 0)
            RR[0, nRound - 1, 0] = RR(1, nRound - 1, 0)
            RR[1, nRound - 1, 0] = k
        if ha and (Odd == 1):
            # rotate the rounds around by one to make the second round-robin, this reduces 2H or 2A at join
            for i in vbForRange(0, nRound - 1):
                for j in vbForRange(0, hbCourt):
                    RR[0, i + nRound, j] = RR(1, (i + 1) % nRound, j)
                    RR[1, i + nRound, j] = RR(0, (i + 1) % nRound, j)
                byes[i + nRound] = byes((i + 1) % nRound)
        elif not ha and (Odd == 0):
            # rotate the courts around by one so deficient pairs are not repeated on same courts
            for i in vbForRange(0, nRound - 1):
                for j in vbForRange(0, hbCourt):
                    RR[0, i + nRound, j] = RR(1, i, (j + 1) % (hbCourt + 1))
                    RR[1, i + nRound, j] = RR(0, i, (j + 1) % (hbCourt + 1))
        else:
            # Simple Duplication of schedule with first dimension reversed
            for i in vbForRange(0, nRound - 1):
                for j in vbForRange(0, hbCourt):
                    RR[0, i + nRound, j] = RR(1, i, j)
                    RR[1, i + nRound, j] = RR(0, i, j)
    if Rand > 0:
        fn_return_value = RandRR(RR, n, ha, doub, Rand, byes)
    else:
        fn_return_value = RR
    return fn_return_value


def SortVector(v, w, l, r):
    i = Integer()
    j = Integer()
    k = Integer()
    x = Single()
    y = Single()
    # Sort v a vector of reals and apply the same reording to w, a vector of integers
    i = l
    j = r
    x = v((l + r) / 2)
    while (i <= j):
        while (v(i) < x and i < r):
            i = i + 1
        while (x < v(j) and j > l):
            j = j - 1
        if (i <= j):
            y = v(i)
            v[i] = v(j)
            v[j] = y
            k = w(i)
            w[i] = w(j)
            w[j] = k
            i = i + 1
            j = j - 1
    if (l < j):
        SortVector(v, w, l, j)
    if (i < r):
        SortVector(v, w, i, r)


def RandVector(h):
    r = vbObjectInitialize(objtype=Double)
    idx = vbObjectInitialize(objtype=Integer)
    i = Integer()
    # Return a vector containing the integers 0 to h in a randomised order
    r = vbObjectInitialize(((0, h),), Variant)
    idx = vbObjectInitialize(((0, h),), Variant)
    for i in vbForRange(0, h):
        r[i] = Rnd()
        idx[i] = i
    SortVector(r, idx, 0, h)
    fn_return_value = idx
    return fn_return_value


def RandRR(x, n, ha, doub, Rand, byes):
    i = Integer()
    j = Integer()
    k = Integer()
    nRound = Integer()
    seed = Single()
    y = Variant()
    q = Variant()
    r = Variant()
    s = Variant()
    t = Variant()
    b = Variant()
    # Randomise a round robin schedule.
    Rnd()((- 1))
    Randomize(Rand)
    y = x
    q = RandVector(1)
    if doub:
        nRound = (UBound(x, 2) + 1) // 2
    else:
        nRound = UBound(x, 2) + 1
    r = RandVector(nRound - 1)
    s = RandVector(UBound(x, 3))
    t = RandVector(n - 1)
    for i in vbForRange(0, 1):
        for j in vbForRange(0, nRound - 1):
            for k in vbForRange(0, UBound(x, 3)):
                if ha:
                    y[q(i), j, s(k)] = t(x(i, j, k) - 1) + 1
                    if doub:
                        y[q(i), j + nRound, s(k)] = t(x(i, j + nRound, k) - 1) + 1
                else:
                    y[q(i), r(j), s(k)] = t(x(i, j, k) - 1) + 1
                    if doub:
                        y[q(i), r(j) + nRound, s(k)
                          ] = t(x(i, j + nRound, k) - 1) + 1
    if not byes == False:
        b = byes
        for j in vbForRange(0, nRound - 1):
            if ha:
                byes[j] = t(b(j) - 1) + 1
                if doub:
                    byes[j + nRound] = t(b(j + nRound) - 1) + 1
            else:
                byes[r(j)] = t(b(j) - 1) + 1
                if doub:
                    byes[r(j) + nRound] = t(b(j + nRound) - 1) + 1
    fn_return_value = y
    return fn_return_value


#fixture = RoundRobin(n, ha, doub, Rand, byes)
fixture = RoundRobin(8, True, True, 0, False)
print("home teams list for all rounds ][ by away teams list for all round")
print(fixture)
