#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json
import inspect
import hashlib
from websocket import create_connection
from websocket import WebSocketException
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
import ConfigParser
from AI import deal
from AI import flop
from AI import turn
from AI import river
from AI import setMyDude
from colorlog import ColoredFormatter

import sys

reload(sys)
sys.setdefaultencoding('utf8')

totalReloadCount = 2
defaultSB = 10


def main():
    init_logger("Texas.log")

    # read config files
    config = ConfigParser.ConfigParser()
    config.read('Config.ini')
    name = config.get('User', 'name')
    phone_num = config.get('User', 'phonenum')
    password = config.get('User', 'password')
    server = config.get('Server', 'URL')
    ticket = config.get('Server', 'ticket')
    port = config.get('Server', 'port')

    # start playing
    logging.info("Start playing for: " + name)
    player = THPlayer(server, name, phone_num, password, ticket, port)
    player.playGame()


def init_logger(log_file_name):
    # log在文件中的记录，每次重新运行会清空文件内容
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %A %H:%M:%S',
                        filename=log_file_name,
                        filemode='w')
    # log备份回滚
    Rthandler = RotatingFileHandler(log_file_name, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(Rthandler)

    # 在调试界面的log显示
    logFormat = "%(log_color)s%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s%(reset)s | %(log_color)s%(" \
                "message)s%(reset)s "
    formatter = ColoredFormatter(logFormat)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # console = logging.StreamHandler()
    # console.setLevel(logging.InFO)
    # formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)


PointDict = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
ColorDict = {'H': 0, 'S': 1, 'C': 2, 'D': 3}


def interpretCardValue(CardList):
    cardValueList = []
    cardvalue = 0
    for ListValue in CardList:
        if (len(ListValue) == 2) and (ListValue[0] in PointDict.keys()) and (ListValue[1] in ColorDict.keys()):
            pointMetric = PointDict[ListValue[0]]
            colorMetric = ColorDict[ListValue[1]]
            # 将牌面值转换为Value，传入AI处理，cardvalue也是一个List
            cardvalue = pointMetric + colorMetric * 13
        cardValueList.append(cardvalue)
    return cardValueList


class stubAI:
    winPlayer = {}
    playerCards = {}
    actionsForEachPlayer = {}

    def _setDefualtDude(self):  # 根据训练结果进行概率微调
        setMyDude(8, -3, 0, -3)  # 稳健打法 8 -3 0 -3，激进打法 6 -3 0 -3

    def __init__(self, playerName):
        global totalReloadCount
        global defaultSB
        self.playerName = playerName
        self._setDefualtDude()
        self.reloadCount = totalReloadCount
        self.sb = defaultSB

    def _Action(self, data):

        action = 0
        nplayer = 0
        for player in data["game"]["players"]:  # 计算牌桌剩余玩家个数
            if not player["folded"]:
                nplayer += 1

        myButton = 0  # 默认位置是除大小盲之外的位置
        if (data["self"]["playerName"] == data["game"]["smallBlind"]["playerName"]):
            myButton = 1  # 表示我处在小盲位置
        elif (data["self"]["playerName"] == data["game"]["bigBlind"]["playerName"]):
            myButton = 2  # 表示我处在大盲位置

        if data["game"]["roundName"] == "Deal":
            # deal(nplayer,sb,holecards,mySet,highestSet,myCash,myButton)
            action = deal(nplayer, data["game"]["smallBlind"]["amount"], interpretCardValue(data["self"]["cards"]),
                          data["self"]["bet"],
                          data["self"]["bet"] + data["self"]["minBet"],
                          data["self"]["chips"] + self.reloadCount * 1000, myButton)
        elif data["game"]["roundName"] == "Flop":
            # flop(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash):
            action = flop(nplayer, data["game"]["smallBlind"]["amount"], interpretCardValue(data["self"]["cards"]),
                          interpretCardValue(data["game"]["board"]),
                          data["self"]["bet"],
                          data["self"]["bet"] + data["self"]["minBet"],
                          data["self"]["chips"] + self.reloadCount * 1000, myButton,
                          data["self"]["chips"] + self.reloadCount * 1000 + data["self"]["roundBet"] + data["self"]["bet"])
            if action == -1:
                logging.error("Wrong cards value: " + str(data["self"]["cards"]) + " " + str(data["game"]["board"]))
        elif data["game"]["roundName"] == "Turn":
            # turn(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash)
            action = turn(nplayer, data["game"]["smallBlind"]["amount"], interpretCardValue(data["self"]["cards"]),
                          interpretCardValue(data["game"]["board"]),
                          data["self"]["bet"],
                          data["self"]["bet"] + data["self"]["minBet"],
                          data["self"]["chips"] + self.reloadCount * 1000, myButton,
                          data["self"]["chips"] + self.reloadCount * 1000 + data["self"]["roundBet"] + data["self"]["bet"])
        else:
            # river(nplayer,sb,holecards,boardCards,mySet,highestSet,myCash,myButton,myRoundStartCash)
            action = river(nplayer, data["game"]["smallBlind"]["amount"], interpretCardValue(data["self"]["cards"]),
                           interpretCardValue(data["game"]["board"]),
                           data["self"]["bet"],
                           data["self"]["bet"] + data["self"]["minBet"],
                           data["self"]["chips"] + self.reloadCount * 1000, myButton,
                           data["self"]["chips"] + self.reloadCount * 1000 + data["self"]["roundBet"] + data["self"]["bet"])
        return action

    def Bet(self, data, cb_bet):
        for player in data["game"]["players"]:
            if player["playerName"] == self.playerName:
                global totalReloadCount
                self.reloadCount = totalReloadCount - player["reloadCount"]
        action = self._Action(data)
        if action == 4:
            cb_bet("allin")
            logging.info("Bet: allin")
        elif action == 3:
            cb_bet("raise")
            logging.info("Bet: raise")
        elif action == 2:
            cb_bet("bet", data["self"]["minBet"])
            logging.info("Bet: bet minBet")
        elif action == 1:
            cb_bet("check")
            logging.info("Bet: check")
        else:
            cb_bet("fold")
            logging.info("Bet: fold")
        self.sb = data["game"]["smallBlind"]["amount"]

    def Action(self, data, cb_action):  # cb_action相当于函数指针，将函数指针传过来
        for player in data["game"]["players"]:
            if player["playerName"] == self.playerName:
                global totalReloadCount
                self.reloadCount = totalReloadCount - player["reloadCount"]
        action = self._Action(data)
        if action == 4:
            cb_action("allin")  # 相当于调用_sendActionMsg（“allin”）
            logging.info("Action: allin")
        elif action == 3:
            cb_action("raise")
            logging.info("Action: raise")
        elif action == 2:
            cb_action("call")
            logging.info("Action: call")
        elif action == 1:
            cb_action("check")
            logging.info("Action: check")
        else:
            cb_action("fold")
            logging.info("Action: fold")
        self.sb = data["game"]["smallBlind"]["amount"]

    def Reload(self, data, cb_reload):
        global totalReloadCount
        for player in data["players"]:
            if player["playerName"] == self.playerName:
                if player["chips"] / self.sb < 16 and player["reloadCount"] < totalReloadCount:  # 筹码数少于小盲16倍进行reload一次
                    cb_reload()
                    self.reloadCount = totalReloadCount - player["reloadCount"] - 1  # 还剩余的reload次数

    def NewRound(self, data):
        logging.info("new round")
        self.sb = data["table"]["smallBlind"]["amount"]
        for player in data["players"]:
            if player["playerName"] == self.playerName:
                logging.info("remain chips:%s" % player["chips"])
                global totalReloadCount
                self.reloadCount = totalReloadCount - player["reloadCount"]

    def ShowAction(self, data):
        logging.info(data["action"]["playerName"] + " take action: " + data["action"]["action"])
        self.actionsForEachPlayer[data["action"]["playerName"]] = data["action"]["action"]

    def Deal(self, data):
        return

    def RoundEnd(self, data):  # 将所有玩家的牌存入dict中，并打印出来，
        logging.info("round end.")

        # 将两个Dict初始化为空
        self.winPlayer = {}
        self.playerCards = {}

        for player in data["players"]:
            if player["winMoney"] > 0:  # 记录胜利玩家的牌
                self.winPlayer[player["playerName"]] = player["hand"]["cards"]

            if player["isSurvive"]:  # 将所有幸存玩家的牌存入dict
                self.playerCards[player["playerName"]] = player["hand"]["cards"]

        for key in self.winPlayer:
            logging.info("This round %s win, hand cards: %s" % (key, self.winPlayer[key]))

        logging.info("Hand cards for each player:")
        for key in self.playerCards:
            logging.info("Player %s: %s" % (key, self.playerCards[key]))

    def GameOver(self, data):
        logging.info("Game over!")
        logging.info("Rest chips for each player:")
        for player in data["players"]:
            logging.info(str(player["playerName"]) + ": " + str(player["chips"]))


class THPlayer:
    ws = ""
    playerName = ""
    wsServer = ""

    def _sendMsg(self, event, data=None):
        msg = {"eventName": event}
        if data is not None:
            msg["data"] = data
        self.ws.send(json.dumps(msg))

    def _sendJoinMsg(self):
        self._sendMsg("__join",
                      {"playerName": self.playerName,
                       "phoneNumber": self.phoneNum,
                       "password": self.passWordMD5,
                       "ticket": self.ticket,
                       "port": self.port,
                       "isHuman": 0,
                       "danmu": 0,
                       "gameName": "texas_holdem"})

    def _sendActionMsg(self, action, amount=None):
        data = {"action": action}
        if action == "bet":
            data["amount"] = amount
        self._sendMsg("__action", data)

    def _sendReload(self):
        self._sendMsg("__reload")

    def cb__no_supported(self, event, data):
        return

    def cb__new_peer_2(self, event, data):
        logging.info("%s: %s" % (event, data))

    def cb__new_peer(self, event, data):
        logging.info("%s: %s" % (event, data))

    def cb__new_round(self, event, data):
        self.AI.NewRound(data)

    def cb__start_reload(self, event, data):
        self.AI.Reload(data, self._sendReload)

    def cb__deal(self, event, data):
        self.AI.Deal(data)

    def cb__action(self, event, data):
        self.AI.Action(data, self._sendActionMsg)

    def cb__bet(self, event, data):
        self.AI.Bet(data, self._sendActionMsg)

    def cb__show_action(self, event, data):
        self.AI.ShowAction(data)

    def cb__round_end(self, event, data):
        self.AI.RoundEnd(data)

    def cb__game_over(self, event, data):
        self.AI.GameOver(data)

    def __init__(self, server, name, phonenum, password, ticket, port):
        self.wsServer = server
        self.playerName = name
        # self.playerNameMD5 = hashlib.md5(name).hexdigest()
        self.AI = stubAI(self.playerName)
        self.phoneNum = phonenum
        self.passWordMD5 = hashlib.md5(password).hexdigest()
        self.ticket = ticket
        self.port = port

        self.actionList = {}  # 是一个dict，将action和处理action的函数绑定起来
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            # method[0]: 函数名(cb__action)
            # method[0][2:]: cb后面的 __action
            # method[1]: 绑定的函数参数
            if method[0].startswith("cb"):
                self.actionList[method[0][2:]] = method[1]
                # print self.actionList

    def _procEvent(self, event, data):
        if event in self.actionList:
            return self.actionList[event](event, data)  # 根据event字段值，找相应的处理函数
        else:
            self.cb__no_supported(event, data)

    def _playing(self):

        while True:
            # print "wait for event"
            result = self.ws.recv()
            logging.debug(result)
            try:
                msg = json.loads(result)
                self._procEvent(msg["eventName"], msg["data"])
            except ValueError as e:
                logging.error(e)
                continue

    def _quit(self):
        self.ws.close()

    def playGame(self):
        gameOver = False
        self.ws = create_connection(self.wsServer)
        while not gameOver:
            try:
                logging.info("Join game ...")
                self._sendJoinMsg()
                self._playing()
                gameOver = True
            except WebSocketException as e:
                logging.error(e.message)
                logging.error("Reset connection")

                # reset connection
                self.ws.close()
                self.ws = create_connection(self.wsServer)
                continue
            except Exception as e:
                logging.exception(e)
                continue
        self._quit()


if __name__ == '__main__':
    main()
    # interpretCardValue(["3D", "9S", "2H"])
