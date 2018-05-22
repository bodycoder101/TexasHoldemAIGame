import random

from CardsValue import turnCardsOdds
from CardsValue import holeCardsOdds
from CardsValue import flopCardsOdds
from CardsValue import riverCardsOdds

myDealDude4 = 8
myFlopDude4 = -3
myTurnDude4 = 0
myRiverDude4 = -3

def setMyDude(d,f,t,r):
    global myDealDude4
    global myFlopDude4
    global myTurnDude4
    global myRiverDude4
    myDealDude4 = d
    myFlopDude4 = f
    myTurnDude4 = t
    myRiverDude4 = r


def deal(nplayer,sb,holecards,mySet,highestSet,myCash,myButton):
    global myDealDude4
    players = nplayer
    if nplayer>5:
        players=5
    if nplayer<2:
        players=2

    myOdds=holeCardsOdds(holecards,players)
    myNiveau = {}
    myNiveau[0] = 43 + myDealDude4 - 6*(players - 2)
    myNiveau[2] = 54 + myDealDude4 - 7*(players - 2)
    individualHighestSet = highestSet
    if(individualHighestSet > myCash):
        individualHighestSet = myCash

    if myCash/individualHighestSet >= 25:
        myNiveau[0] += (25-myCash/individualHighestSet)/10
    else:
        myNiveau[0] += (25-myCash/individualHighestSet)/3

    if myCash/individualHighestSet < 11:
        myNiveau[2] += (21-myCash/individualHighestSet)/2
    '''
    countHumanPlayers = 0
    for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
        if (*it_c).getMyType() == PLAYER_TYPE_HUMAN:
            countHumanPlayers++


    if countHumanPlayers:

        if countHumanPlayers == 1:

            for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
                if (*it_c).getMyType() == PLAYER_TYPE_HUMAN and  (*it_c).getMyAction() != PLAYER_ACTION_FOLD:
                    aggValue = (int)((( (*it_c).getMyAggressive()*1.0)/7.0 - 1.0/currentHand.getActivePlayerList().size())*21.0)
                    myNiveau[0] -= aggValue
                    myNiveau[2] -= aggValue

        else:
            myNiveau[0] -= 3
            myNiveau[2] -= 3
    '''

    cBluff=random.randint(1,100)
    
    #Tools.GetRand(1, 100, 1, &cBluff)

    if myOdds >= myNiveau[2]:


        if highestSet >= 12*sb:

            if myOdds >= myNiveau[2] + 8:
                myAction = 4

            else:
                if myCash-highestSet <= (myCash*1)/5:
                    myAction = 4
                else:
                    myAction = 2
        else:
            myAction = 3
            raiseValue = ((int(myOdds)-myNiveau[2])/2)*2*sb
            if myCash/(2*sb) <= 6 or raiseValue >= (myCash*4)/5:
                myAction = 4
        '''
        if cBluff > 90:
            myAction = PLAYER_ACTION_CALL
            if(myButton == 3 and mySet == highestSet) myAction = PLAYER_ACTION_CHECK

        if cBluff > 80 and myOdds >= myNiveau[2] + 4:
            myAction = PLAYER_ACTION_CALL
            if(myButton == 3 and mySet == highestSet) myAction = PLAYER_ACTION_CHECK

        if cBluff > 70 and myOdds >= myNiveau[2] + 8:
            myAction = PLAYER_ACTION_CALL
            if(myButton == 3 and mySet == highestSet) myAction = PLAYER_ACTION_CHECK

        if cBluff > 60 and myOdds >= myNiveau[2] + 12:
            myAction = PLAYER_ACTION_CALL
            if(myButton == 3 and mySet == highestSet) myAction = PLAYER_ACTION_CHECK
        '''
    else:

        if myOdds >= myNiveau[0] or (mySet >= highestSet/2 and myOdds >= myNiveau[0]-8):

            if(myButton == 3 and mySet == highestSet):
                myAction = 1
            else:
                if myCash-highestSet <= (myCash*1)/5:
                    myAction = 4
                else:
                    myAction = 2
        else:
            myAction = 0
            if(myButton == 3 and mySet == highestSet):
                myAction = 1
            if myButton == 2 and myCash/highestSet > 25:
                myAction = 2
    '''        
    if (sBluff < 100/((((int)currentHand.getActivePlayerList().size()-2)*6)+3) and myOdds < myNiveau[2] and highestSet == 2*sb and not sBluffStatus) or sBluffStatus:

        sBluffStatus = True
        if highestSet >= 4*sb:
            if myCash-highestSet <= (myCash*1)/6:
                raise = myCash
                myAction = PLAYER_ACTION_RAISE
            else:
                myAction = PLAYER_ACTION_CALL
                if(myButton == 3 and mySet == highestSet) myAction = PLAYER_ACTION_CHECK
        else:
            raise = (sBluff/(8-min(7,(int)(currentHand.getActivePlayerList().size()))))*sb
            if myCash/(2*sb) <= 6 or raise >= (myCash*4)/5:
                raise = myCash
            myAction = PLAYER_ACTION_RAISE
        if (highestSet >= 12*sb and myOdds < myNiveau[0]) or (highestSet >= 20*sb and myOdds < myNiveau[2]):
            myAction = PLAYER_ACTION_FOLD
    '''
    return myAction




def flop(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash):
    global myFlopDude4
    players=nplayer
    if nplayer >5:
        players=5
    elif nplayer<2:
        players=2

    myOdds = flopCardsOdds(holecards+boardCards,players)

    if myOdds == -1:
        return -1
    myNiveau = {}

    myNiveau[0] = 53 + myFlopDude4 - 6*(players - 2)

    myNiveau[1] = 56 + myFlopDude4 - 6*(players - 2)

    myNiveau[2] = 69 + myFlopDude4 - 7*(players - 2)

    individualHighestSet = highestSet
    if(individualHighestSet > myCash):
        individualHighestSet = myCash

    '''
    countHumanPlayers = 0
    for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
        if (*it_c).getMyType() == PLAYER_TYPE_HUMAN:
            countHumanPlayers++


    if countHumanPlayers:
        # local or network game and only one human player is active -. set aggValue
        if countHumanPlayers == 1:

            for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
                if (*it_c).getMyType() == PLAYER_TYPE_HUMAN and  (*it_c).getMyAction() != PLAYER_ACTION_FOLD:
                    aggValue = (int)((( (*it_c).getMyAggressive()*1.0)/7.0 - 1.0/currentHand.getActivePlayerList().size())*21.0)
                    myNiveau[0] -= aggValue
                    myNiveau[1] -= aggValue
                    myNiveau[2] -= aggValue


            # network game

        else:
            myNiveau[0] -= 3
            myNiveau[1] -= 3
            myNiveau[2] -= 3
    '''

    cBluff = random.randint(1,100)

    if highestSet > 0:

        if myCash/individualHighestSet >= 25:
            myNiveau[0] += (25-myCash/individualHighestSet)/20
        else:
            myNiveau[0] += (25-myCash/individualHighestSet)/2

        if myCash/individualHighestSet < 11:
            myNiveau[2] += (21-myCash/individualHighestSet)/2

        if myOdds >= myNiveau[2]:

            if highestSet >= 12*sb:
                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:
                    if myCash-highestSet <= (myCash*1)/5:
                        myAction = 4
                    else:
                        myAction = 2

            else:
                myAction = 3
                raiseValue = ((int(myOdds)-myNiveau[2])/5)*2*sb

                if myCash/(2*sb) <= 6 or raiseValue >= (myCash*4.0)/5.0:
                    myAction =4
                

            '''
            if(cBluff > 90) myAction = PLAYER_ACTION_CALL
            if(cBluff > 80 and myOdds >= myNiveau[2] + 4) myAction = PLAYER_ACTION_CALL
            if(cBluff > 70 and myOdds >= myNiveau[2] + 8) myAction = PLAYER_ACTION_CALL
            if(cBluff > 60 and myOdds >= myNiveau[2] + 12) myAction = PLAYER_ACTION_CALL
            '''

        else:

            if myOdds >= myNiveau[0] or (mySet >= highestSet/2 and myOdds >= myNiveau[0]-5) or (myRoundStartCash-myCash > individualHighestSet and myNiveau[0]-3):
                myAction = 2
                if highestSet > (myCash*3.0)/4.0:
                    myAction = 4
            else:
                myAction = 0
    else:
        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds)-myNiveau[1])/8)*2*sb

            if myCash/(2*sb) <= 6:
                myAction = 4

            if bet > (myCash*4.0)/5.0:
                myAction = 4

            
            '''
            if(cBluff > 80) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 70 and myOdds >= myNiveau[1] + 4) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 60 and myOdds >= myNiveau[1] + 8) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 50 and myOdds >= myNiveau[1] + 12) myAction = PLAYER_ACTION_CHECK
            '''
        else:
            myAction = 1
            '''
            if myButton == 1:
                # Position-Bluff generieren
                Tools.GetRand(1, 100, 1, &pBluff)
                if pBluff <= 16:
                    bet = (pBluff/4)*2*sb
                    # bet zu klein
                    if bet == 0:
                        bet = 2*sb

                    # all in bei nur wenigen Chips
                    if myCash/(2*sb) <= 6:
                        bet = myCash

                    # all in bei knappem bet
                    if bet > (myCash*4.0)/5.0:
                        bet = myCash

                    myAction = PLAYER_ACTION_BET
             '''
    '''
    sBluffStatus=False
    if highestSet > 0:

        if sBluffStatus and myOdds < myNiveau[2]:

            if highestSet >= 4*sb:
                myAction = 2
            else:

                Tools.GetRand(1, 8, 1, &rand)
                raise = rand*sb

                if myCash/(2*sb) <= 6 or raise >= (myCash*4)/5:
                    raise = myCash

                myAction = PLAYER_ACTION_RAISE

            if highestSet >= 10*sb:
                myAction = PLAYER_ACTION_FOLD



    else:
        if sBluffStatus and myOdds < myNiveau[1]:

            Tools.GetRand(1, 8, 1, &rand)
            bet = rand*sb

            if bet < 2*sb:
                bet = 2*sb

            if myCash/(2*sb) <= 6:
                bet = myCash

            # all in bei knappem bet
            if bet > (myCash*4.0)/5.0:
                bet = myCash

            myAction = PLAYER_ACTION_BET    
    '''
    return myAction


def turn(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash):
    # type: (object, object, object, object, object, object, object, object, object) -> object
    myOdds = riverCardsOdds(boardCards,holecards)
    global myTurnDude4
    myNiveau={}
    myNiveau[0] = 53 + myTurnDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''
    myNiveau[1] = 56 + myTurnDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''
    myNiveau[2] = 69 + myTurnDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''
    '''
    countHumanPlayers = 0
    for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
        if (*it_c).getMyType() == PLAYER_TYPE_HUMAN:
            countHumanPlayers++
    
    if countHumanPlayers:
         
        if countHumanPlayers == 1:

            for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
                if (*it_c).getMyType() == PLAYER_TYPE_HUMAN and  (*it_c).getMyAction() != PLAYER_ACTION_FOLD:
                    aggValue = (int)((( (*it_c).getMyAggressive()*1.0)/7.0 - 1.0/currentHand.getActivePlayerList().size())*21.0)
                    myNiveau[0] -= aggValue
                    myNiveau[1] -= aggValue
                    myNiveau[2] -= aggValue
        else:
            myNiveau[0] -= 3
            myNiveau[1] -= 3
            myNiveau[2] -= 3
    '''
    individualHighestSet = highestSet
    if(individualHighestSet > myCash):
        individualHighestSet = myCash

    cBluff = random.randint(1,100)

    if highestSet > 0:
        if myCash/individualHighestSet >= 25:
            myNiveau[0] += (25-myCash/individualHighestSet)/10
        else:
            myNiveau[0] += (25-myCash/individualHighestSet)/2

        if myCash/individualHighestSet < 11:
            myNiveau[2] += (21-myCash/individualHighestSet)/2

        if myOdds >= myNiveau[2]:
            if highestSet >= 12*sb:
                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:
                    if myCash-highestSet <= (myCash*1)/5:
                        myAction = 4
                    else:
                        myAction = 2
            else:
                myAction = 3
                raiseValue = ((int(myOdds)-myNiveau[2])/4)*2*sb
                if myCash/(2*sb) <= 6 or raiseValue >= (myCash*4.0)/5.0:
                    myAction = 4
            '''
            if(cBluff > 90) myAction = PLAYER_ACTION_CALL
            if(cBluff > 80 and myOdds >= myNiveau[2] + 5) myAction = PLAYER_ACTION_CALL
            if(cBluff > 70 and myOdds >= myNiveau[2] + 10) myAction = PLAYER_ACTION_CALL
            if(cBluff > 60 and myOdds >= myNiveau[2] + 15) myAction = PLAYER_ACTION_CALL
            '''
        else:  
            if myOdds >= myNiveau[0] or (mySet >= highestSet/2 and myOdds >= myNiveau[0]-5) or (myRoundStartCash-myCash > individualHighestSet and myNiveau[0]-3):
                myAction = 2
                if highestSet > (myCash*3.0)/4.0:
                    myAction = 4
            else:
                myAction = 0
    else:
        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds)-myNiveau[1])/6)*2*sb
            if bet == 0:
                bet = 2*sb

            if myCash/(2*sb) <= 6:
                myAction = 4

            if bet > (myCash*4.0)/5.0:
                myAction = 4

            '''
            if(cBluff > 90) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 80 and myOdds >= myNiveau[2] + 5) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 70 and myOdds >= myNiveau[2] + 10) myAction = PLAYER_ACTION_CHECK
            if(cBluff > 60 and myOdds >= myNiveau[2] + 15) myAction = PLAYER_ACTION_CHECK
            '''
        else:
            myAction = 1
            '''
            if myButton == 1:
                Tools.GetRand(1, 100, 1, &pBluff)
                if pBluff <= 16:
                    bet = (pBluff/4)*2*sb
                     
                    if bet == 0:
                        bet = 2*sb

                    if myCash/(2*sb) <= 6:
                        bet = myCash

                    if bet > (myCash*4.0)/5.0:
                        bet = myCash
                    myAction = PLAYER_ACTION_BET
            '''
    '''
    if highestSet > 0:

        if sBluffStatus and myOdds < myNiveau[2]:

            if highestSet >= 4*sb:
                myAction = PLAYER_ACTION_CALL
            else:
                Tools.GetRand(1, 8, 1, &rand)
                raise = rand*sb

                if myCash/(2*sb) <= 6 or raise >= (myCash*4)/5:
                    raise = myCash
                myAction = PLAYER_ACTION_RAISE

            if highestSet >= 10*sb:
                myAction = PLAYER_ACTION_FOLD

    else:
        if sBluffStatus and myOdds < myNiveau[1]:

            Tools.GetRand(1, 8, 1, &rand)
            bet = rand*sb
             
            if bet < 2*sb:
                bet = 2*sb

             
            if myCash/(2*sb) <= 6:
                bet = myCash

            if bet > (myCash*4.0)/5.0:
                bet = myCash
            myAction = PLAYER_ACTION_BET
    '''
    return myAction

def river(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash):

    myOdds = riverCardsOdds(boardCards,holecards)
    global myRiverDude4
    myNiveau = {}
    myNiveau[0] = 53 + myRiverDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''

    myNiveau[1] = 56 + myRiverDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''

    myNiveau[2] = 69 + myRiverDude4
    ''' - 6*(currentHand.getActivePlayerList().size() - 2)'''
	
    '''
    countHumanPlayers = 0
    for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
        if (*it_c).getMyType() == PLAYER_TYPE_HUMAN:
            countHumanPlayers++


    if countHumanPlayers:

        if countHumanPlayers == 1:

            for(it_c=currentHand.getActivePlayerList().begin(); it_c!=currentHand.getActivePlayerList().end(); ++it_c)
                if (*it_c).getMyType() == PLAYER_TYPE_HUMAN and  (*it_c).getMyAction() != PLAYER_ACTION_FOLD:
                    aggValue = (int)((( (*it_c).getMyAggressive()*1.0)/7.0 - 1.0/currentHand.getActivePlayerList().size())*21.0)
                    myNiveau[0] -= aggValue
                    myNiveau[1] -= aggValue
                    myNiveau[2] -= aggValue




        else:
            myNiveau[0] -= 3
            myNiveau[1] -= 3
            myNiveau[2] -= 3
    '''

    individualHighestSet = highestSet
    if(individualHighestSet > myCash):
        individualHighestSet = myCash

    if highestSet > 0:
        if myCash/individualHighestSet >= 25:
            myNiveau[0] += (25-myCash/individualHighestSet)/10
        else:
            myNiveau[0] += (25-myCash/individualHighestSet)/2

        if myCash/individualHighestSet < 11:
            myNiveau[2] += (21-myCash/individualHighestSet)/2

        if myOdds >= myNiveau[2]:

            if highestSet >= 12*sb:

                if myOdds >= myNiveau[2] + 15:
                    myAction = 4
                else:

                    if myCash-highestSet <= (myCash*1)/5:
                        myAction = 4
                    else:
                        myAction = 2

            else:
                myAction = 3
                raiseValue = ((int(myOdds)-myNiveau[2])/2)*2*sb
                if myCash/(2*sb) <= 8:
                    myAction =4

        else:

            if myOdds >= myNiveau[0] or (mySet >= highestSet/2 and myOdds >= myNiveau[0]-5) or (myRoundStartCash-myCash > individualHighestSet and myNiveau[0]-3):
                myAction = 2
                if myCash-highestSet <= (myCash*1)/4:
                    myAction = 4
            else:
                myAction = 0
    else:

        if myOdds >= myNiveau[1]:
            myAction = 2
            bet = ((int(myOdds)-myNiveau[1])/3)*2*sb
            if bet == 0:
                bet = 2*sb

            if myCash/(2*sb) <= 6:
                myAction = 4

            if bet > (myCash*4.0)/5.0:
                myAction = 4
        else:
            myAction = 1
            '''
            if myButton == 1:

                Tools.GetRand(1, 100, 1, &pBluff)
                if pBluff <= 20:
                    bet = (pBluff/4)*2*sb

                    if bet == 0:
                        bet = 2*sb


                    if myCash/(2*sb) <= 6:
                        bet = myCash


                    if bet > (myCash*4.0)/5.0:
                        bet = myCash

                    myAction = PLAYER_ACTION_BET
            '''
    '''
    if highestSet > 0:

        if sBluffStatus and myOdds < myNiveau[2]:

            if highestSet >= 4*sb:
                myAction = PLAYER_ACTION_CALL

            else:

                Tools.GetRand(1, 8, 1, &rand)
                raise = rand*sb

                if myCash/(2*sb) <= 6 or raise >= (myCash*4)/5:
                    raise = myCash

                myAction = PLAYER_ACTION_RAISE

            if highestSet >= 10*sb:
                myAction = PLAYER_ACTION_FOLD

    else:
        if sBluffStatus and myOdds < myNiveau[1]:

            Tools.GetRand(1, 8, 1, &rand)
            bet = rand*sb

            if bet < 2*sb:
                bet = 2*sb

            if myCash/(2*sb) <= 6:
                bet = myCash

            if bet > (myCash*4.0)/5.0:
                bet = myCash

            myAction = PLAYER_ACTION_BET
    '''
    return myAction



#print flop(5,10,[1,22],[3,17,5],60,200,700,1,760)
#print deal(5,10,[9,9],10,20,990,3)
