# TexasHoldemAIGame 的相关整理
此程序为参加趋势科技德州扑克AI大赛相关的代码和接口
## 规则整理
1. playerName是唯一标识
2. 在每一轮（除第1轮外）开始的时候， 服务器会发送询问玩家是否要索取筹码， 每局比赛中每次可以索取 1000 筹码， 最多索取 2 次
3. 牌面值：
	- 第1个字符为数字: 取值为: 2~9， T(10)， J(J)， Q(Q)， K(K)， A(Ace)
	- 第2个字符为花色: 分别为 H(红心)， S(黑桃)， C(草花)， D(方块)
	- 服务器给的值例如：2H、TS（前面是牌面、后面是花色）
4. 牌局当前的状态：
   Deal（还未发公共牌, 也就是preFlop）， Flop（第1次发3张公共牌）， Turn（发第4张公共牌）， River（发第5张公共牌）
5. 服务器只向客户端发送**两种**不同的消息
	- 需采取“action”
    包含两个动作，需要玩家行动和需要玩家押注
		- `"eventName" : "__action"`
		请求玩家决策：“call”“check”“raise”“fold”“allin”“bet（作用类似call，bet中的amount数额加上玩家当前已下注额不得小于当前最大数额）”
		- `"eventName" : "__bet"`
		需要玩家下注，仅可以决策bet，但可以选择bet的数值，文档中说又可以其他决策？

	- 通知当前牌桌的状态，是**广播消息**（在四个阶段的发牌信息、玩家的决策信息、每一轮结束后所有玩家的状态、游戏结束的广播消息等）
6. 每局比赛中每次可以索取 1000 筹码， 最多索取 2 次
7. action中相关字段
```json
{
    "eventName" : "__action",
    "data" : {
        "tableNumber" : 1,
        "self" : {
            "playerName" : "bobi",
            "chips" : 1000,
            "folded" : false,
            "allIn" : false,
            "isSurvive" : true,
            "roundBet" : 0, //
            "bet" : 10,
            "minBet" : 10,
            "cards" : ["JC", "KS"]
        },
        "game" : {
            "smallBlind": {
                "playerName" : "bobi",
                "amount" : 10
            },
            "bigBlind": {
                "playerName" : "cicy",
                "amount" : 20
            },
            "board" : [XX, XX, XX],
            "raiseCount" : 0,
            "betCount" : 1,
            "roundName" : "Deal", // 其它可能的值为 : "Flop", "Turn", "River"
            "players" :[
				...
			]
		}
    }
}
```

## Join game

使用websocket包接入

```python
global ws
hasn_md5 = hashlib.md5()
hasn_md5.update('<Your Password>')
password_md5 = hasn_md5.hexdigest()
   ws = create_connection("ws://ai.cad-stg.trendmicro.com:<Copy From Website：port>")

ws.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": "<Your Name>",
                "phoneNumber": "<Your PhoneNum>",
                "password": password_md5,
                "ticket": "<Copy From Website>",
                "port": '<Copy From Website>',
                "isHuman": 0,
                "danmu": 0,
                "gameName": "texas_holdem"
            }
        }))
```
## 代码说明
此仓库中代码相关说明，包括配置和决策

### AI决策返回代码说明
| return action code | 动作说明          |
| ------------------ | ----------------- |
| 0                  | fold              |
| 1                  | check             |
| 2                  | call              |
| 3                  | raise             |
| 4                  | allin             |
| -1                 | wrong cards value |

### 玩家牌桌位置说明
| myButton code | 位置说明                           |
| ------------- | ---------------------------------- |
| 0             | 表示玩家的位置是除大小盲之外的位置 |
| 2             | 表示玩家处在小盲位置               |
| 3             | 表示玩家处在大盲位置               |
