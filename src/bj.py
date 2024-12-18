from src.card import Deck
from src.hand import Hands
from src.user import User

class BlackJack:
    def __init__(self):
        # アトリビュートの初期化
        self.__users = [User(f"プレイヤー{i+1}", 100, 10) for i in range(3)]
        self.__dealer_hands = Hands()
        self.__deck = Deck()
        self.__current_player_index = 0
        self.__round = 1

    def bet(self, user_index: int, add_betcoin: int):
        user = self.__users[user_index]
        if (user.betcoin + add_betcoin) < 10:
            add_betcoin = 10 - user.betcoin
        if (user.coin - add_betcoin) < 0:
            add_betcoin = user.coin
        user.betcoin += add_betcoin
        user.coin -= add_betcoin
    
    def start(self):
        # 1. ユーザーとディーラーのカードを初期化する。
        for user in self.__users:
            user.hands.clear_hands()
        self.__dealer_hands.clear_hands()

        # 2. デッキを初期化する。
        self.__deck.reset_card()

        # 3. ユーザーとディーラーにカードを2枚ずつ配る。
        for hand in [user.hands for user in self.__users] + [self.__dealer_hands]:
            for _ in range(2):
                hand.add_hands(self.__deck.draw_card())

        # 4. 現在のプレイヤーのインデックスを0に設定する。
        self.__current_player_index = 0
        self.__go_to_next_player()

    def hit(self):
        user = self.__users[self.__current_player_index]
        # ユーザーにカードを1枚配る。
        user.hands.add_hands(self.__deck.draw_card())

        # ユーザーの手札が21を超えた場合、次のプレイヤーに移る。
        self.__go_to_next_player()

    def __go_to_next_player(self):
        if self.__current_player_index < 3 and self.__users[self.__current_player_index].hands.hand_strength >= 21:
            self.__current_player_index += 1
            self.__go_to_next_player()

    def stand(self):
        # 次のプレイヤーに移る。
        self.__current_player_index += 1
        self.__go_to_next_player()
        

    def dealer(self):
        self.__dealer_hands.add_hands(self.__deck.draw_card())
        
    def judge(self):
        dealer_strength = self.__dealer_hands.hand_strength
        user_strength = [self.__users[i].hands.hand_strength for i in range(3)]

        victory_or_defeat = [1, 1, 1]

        if dealer_strength >= 22:
            for i in range(3):
                if user_strength[i] <= 21:
                    victory_or_defeat[i] = 2
        else:
            for i in range(3):
                if user_strength[i] > 21:
                    victory_or_defeat[i] = 0

                elif user_strength[i] > dealer_strength:
                    # ユーザーの勝ちの場合、ベットコインを2倍にする。
                    victory_or_defeat[i] = 2
                elif user_strength[i] == dealer_strength:
                    # 引き分けの場合、ベットコインを返す。
                    victory_or_defeat[i] = 1
                else:
                    # ユーザーの負けの場合、ベットコインを失う。
                    victory_or_defeat[i] = 0
        self.renew_coins(victory_or_defeat)

    def renew_coins(self, victory_or_defeat):
        for i in range(3):
            user = self.__users[i]
            user.coin += user.betcoin * victory_or_defeat[i]
            user.betcoin = 10
        

    def clear_result(self):
        for i in range(3):
            self.__users[i].coin = 100
            self.__users[i].betcoin = 10
        self.__round = 1

    def next_round(self):
        self.__round += 1
        self.__current_player_index = 0

        for user in self.__users:
            if user.coin >= 10:
                user.betcoin = 10
                user.coin -= 10

    def get_ranking(self) -> list[str]:
        # ユーザーのコイン数の降順で、ユーザー名を取得する。
        return [user.name for user in sorted(self.__users, key=lambda x: x.coin, reverse=True)]

    def get_user_coins(self) -> list[int]:
        return [user.coin for user in self.__users]
    
    def get_user_betcoins(self) -> list[int]:
        return [user.betcoin for user in self.__users]
    
    def get_user_hands(self) -> list[list[tuple[str, int]]]:
        return [[(card.suit, card.strength) for card in user.hands.hands] for user in self.__users]
    
    def get_dealer_hands(self) -> list[tuple[str, int]]:
        return [(card.suit, card.strength) for card in self.__dealer_hands.hands]
    
    def get_dealer_strength(self) -> int:
        return self.__dealer_hands.hand_strength
    
    def get_user_strengths(self) -> list[int]:
        return [user.hands.hand_strength for user in self.__users]
    
    def get_user_names(self) -> list[str]:
        return [user.name for user in self.__users]
    
    def get_round(self) -> int:
        return self.__round
    
    def get_current_player_index(self) -> int:
        return self.__current_player_index