import numpy as np
from Hands import Hands
from Cards import Cards

class BlackJack:
    def __init__(self):
        self.__user_coinonhand = np.array([[100,100,100],['プレイヤー１','プレイヤー２','プレイヤー３']])
        self.__user_betcoin = np.array([10,10,10])
        self.__user_hands = [Hands(), Hands(), Hands()]
        self.__dealer_hands = Hands()
        self.__card = Cards()

    def bet(self, user, betcoin):
        user, bc = user, betcoin
        if not(self.__user_betcoin[user] == 10 and bc < 0):
            self.__user_betcoin[user] += bc
            self.__user_coinonhand[0][user] -= bc
        return self.__user_betcoin
    
    def start(self):
        hand_name: list[Hands] = [self.__user_hands[0], self.__user_hands[1], self.__user_hands[2], self.__dealer_hands]
        userhand_strength = []
        for user in hand_name:
            draw_time = 0
            while draw_time < 2:
                a = self.__card.draw_card()
                user.add_hands(a[0], a[1])
                draw_time += 1
            user.cal_hands_strength()
            userhand_strength.append((user.get_hands_list(), user.get_hands_strength()))
        return userhand_strength

    def hit(self, n):
        self.hit_card = self.__card.draw_card()
        self.hit_user_hands = self.__user_hands[n].get_hand_list()
        self.__user_hands[n].add_hand(self.hit_card)
        self.__user_hands[n].cal_hands_strength()
        return self.hit_user_hands, self.__user_hands[n].get_hands_strength()
    
    def dealer(self):
        hands_strength = self.__dealer_hands.get_hands_strength()
        while hands_strength < 17:
            self.hit_card = self.__card.draw_card()
            self.__dealer_hands.add_hands(self.hit_card)
            self.__dealer_hands.cal_hands_strength()
            hands_strength = self.__dealer_hands.get_hands_strength()
        return self.__dealer_hands.get_hands_list(), self.__dealer_hands.get_hands_strength()

    def renew_coin(self, vod:np.array):
        self.__user_coinonhand[0] = self.__user_coinonhand[0] + self.__user_betcoin * vod

    def ranking(self):
        user_list = []
        coin_list = self.__user_coinonhand.T.tolist()
        for i in sorted(coin_list, key=lambda x: x[0]):
            user_list.append(i[1])
        return user_list
        
    def judge(self):
        d_hand = self.__dealer_hands.get_hand_strength()
        strength_list = []
        judge_list = [0,0,0]
        for i in range(len(judge_list)):
            strength_list[i] = self.__user_hands[i].get_hand_strength()
        if d_hand <= 21:
            for k in range(len(judge_list)):
                if strength_list[k] > d_hand:
                    judge_list[k] = 2
                else:
                    if strength_list[k] == d_hand:
                        judge_list[k] = 1
            if strength_list[k] > 21:
                judge_list[k] = 0
        else:
            for k in range(len(judge_list)):
                if strength_list[k] <= 21:
                    judge_list[k] = 2
                else:
                    judge_list[k] = 0
        self.renew_coin(np.array(judge_list))
        self.__card.reset_cards()
        for k in range(len(judge_list)):
            self.__user_hands[k].clear_hands()
        return self.__user_coinonhand[0]

    def clear_result(self):
        self.__user_coinonhand[0] = [100,100,100]
        self.__user_betcoin = [10,10,10]
        for i in self.__user_hands:
            i.clear_hands()
        self.__dealer_hands.clear_hands()            

    def get_user_coinonhand(self) -> list[int]:
        return [int(x) for x in self.__user_coinonhand[0]]

    def get_user_betcoin(self):
        return self.__user_betcoin
