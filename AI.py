#! /usr/bin/env python
# -*- coding:utf-8 -*-
import random
from CardsValue import turnCardsOdds
from CardsValue import holeCardsOdds
from CardsValue import flopCardsOdds
from CardsValue import riverCardsOdds

# return action code
# 4: allin
# 3: raise
# 2: call
# 1: check
# 0：fold

myDealDude4 = 8
myFlopDude4 = -3
myTurnDude4 = 0
myRiverDude4 = -3


def setMyDude(d, f, t, r):  # 进行概率微调
    global myDealDude4
    global myFlopDude4
    global myTurnDude4
    global myRiverDude4
    myDealDude4 = d
    myFlopDude4 = f
    myTurnDude4 = t
    myRiverDude4 = r


def deal(nplayer, sb, holecards, mySet, highestSet, myCash, myButton):
    global myDealDude4
    players = nplayer  # players的范围是2到5
    if nplayer > 5:
        players = 5
    if nplayer < 2:
        players = 2

    myOdds = holeCardsOdds(holecards, players)  # 从表中找到相应的概率
    myNiveau = {}
    myNiveau[0] = 43 + myDealDude4 - 6 * (players - 2)
    myNiveau[2] = 54 + myDealDude4 - 7 * (players - 2)
    individualHighestSet = highestSet
    if individualHighestSet > myCash:
        individualHighestSet = myCash

    if myCash / individualHighestSet >= 25:
        myNiveau[0] += (25 - myCash / individualHighestSet) / 10
    else:
        myNiveau[0] += (25 - myCash / individualHighestSet) / 3

    if myCash / individualHighestSet < 11:
        myNiveau[2] += (21 - myCash / individualHighestSet) / 2

    if myOdds >= myNiveau[2]:
        if highestSet >= 12 * sb:
            if myOdds >= myNiveau[2] + 8:
                myAction = 4  # allin
            else:
                if myCash - highestSet <= ((myCash * 1) / 5):  # 筹码太少，直接allin
                    myAction = 4  # allin
                else:
                    myAction = 2  # call
        else:
            myAction = 3  # raise
            raiseValue = ((int(myOdds) - myNiveau[2]) / 2) * 2 * sb
            if myCash / (2 * sb) <= 6 or raiseValue >= (myCash * 4) / 5:
                myAction = 4  # allin

        # 增加随机种子，模糊进场
        cBluff = random.randint(1, 100)
        if cBluff > 90:
            myAction = 2
            if myButton == 2 and mySet == highestSet:
                myAction = 1
        if cBluff > 80 and (myOdds >= myNiveau[2] + 4):
            myAction = 2
            if myButton == 2 and mySet == highestSet:
                myAction = 1
        if cBluff > 70 and (myOdds >= myNiveau[2] + 8):
            myAction = 2
            if myButton == 2 and mySet == highestSet:
                myAction = 1
        if cBluff > 60 and (myOdds >= myNiveau[2] + 12):
            myAction = 2
            if myButton == 2 and mySet == highestSet:
                myAction = 1
    else:

        if myOdds >= myNiveau[0] or (mySet >= highestSet / 2 and myOdds >= myNiveau[0] - 8):
            if myButton == 2 and mySet == highestSet:
                myAction = 1  # 处在大盲，check
            else:
                if myCash - highestSet <= ((myCash * 1) / 5):
                    myAction = 4  # 筹码太少，直接allin
                else:
                    myAction = 2  # call 进场
        else:
            myAction = 0  # 概率太低，fold
            if myButton == 2 and mySet == highestSet:
                myAction = 1  # 处在大盲，check
            if myButton == 1 and myCash / highestSet > 88:
                myAction = 2  # 处在小盲，且代价不大，可以进场打一枪，call

    return myAction


def flop(nplayer, sb, holecards, boardCards, mySet, highestSet, myCash, myButton, myRoundStartCash):
    global myFlopDude4
    players = nplayer
    if nplayer > 5:
        players = 5
    elif nplayer < 2:
        players = 2

    myOdds = flopCardsOdds(holecards + boardCards, players)

    if myOdds == -1:
        return -1

    myNiveau = {}
    myNiveau[0] = 53 + myFlopDude4 - 6 * (players - 2)
    myNiveau[1] = 56 + myFlopDude4 - 6 * (players - 2)
    myNiveau[2] = 69 + myFlopDude4 - 7 * (players - 2)

    individualHighestSet = highestSet
    if individualHighestSet > myCash:
        individualHighestSet = myCash

    if highestSet > 0:
        if myCash / individualHighestSet >= 25:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 20
        else:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 2

        if myCash / individualHighestSet < 11:
            myNiveau[2] += (21 - myCash / individualHighestSet) / 2
        if myOdds >= myNiveau[2]:
            if highestSet >= 12 * sb:
                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:
                    if myCash - highestSet <= (myCash * 1) / 5:
                        myAction = 4
                    else:
                        myAction = 2
            else:
                myAction = 3
                raiseValue = ((int(myOdds) - myNiveau[2]) / 5) * 2 * sb
                if myCash / (2 * sb) <= 6 or raiseValue >= (myCash * 4.0) / 5.0:
                    myAction = 4

            cBluff = random.randint(1, 100)
            if cBluff > 90:
                myAction = 2
            if cBluff > 80 and (myOdds >= myNiveau[2] + 4):
                myAction = 2
            if cBluff > 70 and (myOdds >= myNiveau[2] + 8):
                myAction = 2
            if cBluff > 60 and (myOdds > myNiveau[2] + 12):
                myAction = 2

        else:
            if myOdds >= myNiveau[0] or (mySet >= highestSet / 2 and myOdds >= myNiveau[0] - 5) \
                    or (myRoundStartCash - myCash > individualHighestSet and myNiveau[0] - 3):
                myAction = 2
                if highestSet > (myCash * 3.0) / 4.0:
                    myAction = 4
            else:
                if myButton == 1 and mySet == highestSet:  # 处在小盲位且翻牌圈第一个说话，可以check
                    myAction = 1
                else:
                    myAction = 0
    else:
        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds) - myNiveau[1]) / 8) * 2 * sb

            if myCash / (2 * sb) <= 6:
                myAction = 4

            if bet > (myCash * 4.0) / 5.0:
                myAction = 4

            cBluff = random.randint(1, 100)
            if cBluff > 80:
                myAction = 1
            if cBluff > 70 and (myOdds >= myNiveau[1]+4):
                myAction = 1
            if cBluff > 60 and (myOdds >= myNiveau[1]+8):
                myAction = 1
            if cBluff > 50 and (myOdds >= myNiveau[1]+12):
                myAction = 1

        else:
            myAction = 1
            if myButton == 0:
                cBluff = random.randint(1, 100)
                if cBluff <= 16:
                    bet = (cBluff/4)*2*sb
                    if bet == 0:
                        bet = 2*sb
                    if myCash/(2*sb) <= 6:
                        myAction = 4
                    if bet > (myCash * 4.0/5.0):
                        myAction = 4

    return myAction


def turn(nplayer, sb, holecards, boardCards, mySet, highestSet, myCash, myButton, myRoundStartCash):
    global myTurnDude4
    myOdds = turnCardsOdds(boardCards, holecards)

    myNiveau = {}
    myNiveau[0] = 53 + myTurnDude4
    myNiveau[1] = 56 + myTurnDude4
    myNiveau[2] = 69 + myTurnDude4
    individualHighestSet = highestSet
    if individualHighestSet > myCash:
        individualHighestSet = myCash

    if highestSet > 0:
        if myCash / individualHighestSet >= 25:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 10
        else:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 2

        if myCash / individualHighestSet < 11:
            myNiveau[2] += (21 - myCash / individualHighestSet) / 2

        if myOdds >= myNiveau[2]:
            if highestSet >= 12 * sb:
                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:
                    if myCash - highestSet <= (myCash * 1) / 5:
                        myAction = 4
                    else:
                        myAction = 2
            else:
                myAction = 3
                raiseValue = ((int(myOdds) - myNiveau[2]) / 4) * 2 * sb
                if myCash / (2 * sb) <= 6 or raiseValue >= (myCash * 4.0) / 5.0:
                    myAction = 4

            cBluff = random.randint(1, 100)
            if cBluff > 90:
                myAction = 2
            if cBluff > 80 and (myOdds >= myNiveau[2] + 5):
                myAction = 2
            if cBluff > 70 and (myOdds >= myNiveau[2] + 10):
                myAction = 2
            if cBluff > 60 and (myOdds >= myNiveau[2] + 15):
                myAction = 2

        else:
            if myOdds >= myNiveau[0] or (mySet >= highestSet / 2 and myOdds >= myNiveau[0] - 5) \
                    or (myRoundStartCash - myCash > individualHighestSet and myNiveau[0] - 3):
                myAction = 2
                if highestSet > (myCash * 3.0) / 4.0:
                    myAction = 4
            else:
                myAction = 0
    else:
        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds) - myNiveau[1]) / 6) * 2 * sb
            if bet == 0:
                bet = 2 * sb

            if myCash / (2 * sb) <= 6:
                myAction = 4

            if bet > (myCash * 4.0) / 5.0:
                myAction = 4

            cBluff = random.randint(1, 100)
            if cBluff > 90:
                myAction = 1
            if cBluff > 80 and (myOdds >= myNiveau[2] + 5):
                myAction = 1
            if cBluff > 70 and (myOdds >= myNiveau[2] + 10):
                myAction = 1
            if cBluff > 60 and (myOdds >= myNiveau[2] + 15):
                myAction = 1
        else:
            myAction = 1
            if myButton == 0:
                cBluff = random.randint(1, 100)
                if cBluff <= 16:
                    bet = (cBluff / 4) * 2 * sb
                    if bet == 0:
                        bet = 2 * sb
                    if myCash / (2 * sb) <= 6:
                        myAction = 4
                    if bet > (myCash * 4.0 / 5.0):
                        myAction = 4

    return myAction


def river(nplayer, sb, holecards, boardCards, mySet, highestSet, myCash, myButton, myRoundStartCash):
    myOdds = riverCardsOdds(boardCards, holecards)
    global myRiverDude4
    myNiveau = {}

    myNiveau[0] = 53 + myRiverDude4
    myNiveau[1] = 56 + myRiverDude4
    myNiveau[2] = 69 + myRiverDude4
    individualHighestSet = highestSet

    if individualHighestSet > myCash:
        individualHighestSet = myCash

    if highestSet > 0:
        if myCash / individualHighestSet >= 25:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 10
        else:
            myNiveau[0] += (25 - myCash / individualHighestSet) / 2

        if myCash / individualHighestSet < 11:
            myNiveau[2] += (21 - myCash / individualHighestSet) / 2

        if myOdds >= myNiveau[2]:
            if highestSet >= 12 * sb:
                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:
                    if myCash - highestSet <= (myCash * 1) / 5:
                        myAction = 4
                    else:
                        myAction = 2
            else:
                myAction = 3
                raiseValue = ((int(myOdds) - myNiveau[2]) / 2) * 2 * sb
                if myCash / (2 * sb) <= 8:
                    myAction = 4
        else:

            if myOdds >= myNiveau[0] or (mySet >= highestSet / 2 and myOdds >= myNiveau[0] - 5) \
                    or (myRoundStartCash - myCash > individualHighestSet and myNiveau[0] - 3):
                myAction = 2
                if myCash - highestSet <= (myCash * 1) / 4:
                    myAction = 4
            else:
                myAction = 0
    else:

        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds) - myNiveau[1]) / 3) * 2 * sb
            if bet == 0:
                bet = 2 * sb

            if myCash / (2 * sb) <= 6:
                myAction = 4

            if bet > (myCash * 4.0) / 5.0:
                myAction = 4
        else:
            myAction = 1
            if myButton == 0:
                cBluff = random.randint(1, 100)
                if cBluff <= 16:
                    bet = (cBluff / 4) * 2 * sb
                    if bet == 0:
                        bet = 2 * sb
                    if myCash / (2 * sb) <= 6:
                        myAction = 4
                    if bet > (myCash * 4.0 / 5.0):
                        myAction = 4

    return myAction

# print flop(5,10,[1,22],[3,17,5],60,200,700,1,760)
# print deal(5,10,[9,9],10,20,990,3)
