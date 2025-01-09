from src.card import Deck
from src.hand import Hands
from src.user import User

class BlackJack:
    def __init__(self):
        # アトリビュートの初期化
        self.__users = [User(f"プレイヤー{i+1}", 100, 10) for i in range(3)]
        self.__dealer_hands = Hands()
        self.__deck = Deck()

    def bet(self, user_index: int, add_betcoin: int):
        user = self.__users[user_index]

        # ユーザーがベットできるコイン数が10未満の場合、ベットコインを10にする。
        if (user.betcoin + add_betcoin) < 10:
            add_betcoin = 10 - user.betcoin

        # ユーザーのコイン数がベットコインより少ない場合、ベットコインをコイン数に合わせる。
        if (user.coin - add_betcoin) < 0:
            add_betcoin = user.coin

        # ユーザーのベットコインとコイン数を更新する。
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

    def hit(self, user_index: int):
        user = self.__users[user_index]
        # ユーザーにカードを1枚配る。
        user.hands.add_hands(self.__deck.draw_card())
        

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