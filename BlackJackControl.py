import math
import os
import tkinter as tk
import random

import numpy as np

from BlackJack import BlackJack

FONTS = ["Yu Mincho"]
FONT_IDX = 0
PATH = os.path.dirname(__file__).replace("\\", "/")

STRENGTH = {
    'A': 1,
    **{str(x): x for x in range(2, 11)},
    'J': 11,
    'Q': 12,
    'K': 13
}

class BlackJackControl:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Black Jack")

        self.__blackjack = BlackJackTest()
        self.__stand: int

        # ターン表示フレーム
        self.__round_frame = tk.Frame(self.__root, width=10, height=3)
        self.__round_frame.grid(row=0, column=0)
        tk.Label(self.__round_frame, 
                  text="ROUND",
                  font=(FONTS[FONT_IDX], 15),
                  anchor=tk.E,
                  height=1).grid(row=0, column=0, columnspan=10)
        turnFrame = tk.Frame(self.__round_frame)
        turnFrame.grid(row=1, column=7)
        self.__turn_label = tk.Label(turnFrame, 
                  text="1",
                  font=(FONTS[FONT_IDX], 30),
                  anchor=tk.E).grid(row=0, column=0)
        tk.Label(turnFrame,
                  text="/3",
                  font=(FONTS[FONT_IDX], 20),
                  anchor=tk.SW,
                  height=2).grid(row=0, column=1)

        # トップウィンドウ - スタートボタン周りのフレーム
        self.__startButtonFrame = tk.Frame(self.__root, width=20)
        self.__startButtonFrame.grid(row=0, column=1, padx=100, pady=5)
        tk.Label(self.__startButtonFrame, 
                  text="BET TIME",
                  font=(FONTS[FONT_IDX], 33, "bold"),
                  width=10, height=1).grid(row=0, column=1)
        tk.Button(self.__startButtonFrame, 
                  text="START",
                  relief=tk.SOLID,
                  font=(FONTS[FONT_IDX], 24),
                  foreground='#ffffff',
                  background='#ff0000',
                  command=self.clicked_start,
                  width=10, height=2).grid(row=1, column=1, ipadx=10)
        
        # 空フレーム
        empty = tk.Frame(self.__root)
        empty.grid(row=0, column=2)
        tk.Label(empty, text="", width=10).grid(row=0, column=0)

        # トップウィンドウ
        self.__bet_frame = tk.Frame(self.__root)
        self.__bet_frame.grid(row=1, column=0, columnspan=3)

        # トップウィンドウ - ベット周りのフレーム
        self.__betUserFrame = tk.Frame(self.__bet_frame, width=40)
        self.__betUserFrame.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E)
        colors = ['#ff0000', '#0000dd', '#cccc00']
        self.__betCoinLabel = []
        for user in range(3):
            frame = tk.Frame(self.__betUserFrame)
            frame.grid(row=0, column=user, padx=10, pady=10)

            sizeFrame = tk.Frame(frame, relief=tk.SOLID, borderwidth=1, width=12)
            buttonFrame = tk.Frame(frame)
            sizeFrame.grid(row=2, column=0, padx=5)
            buttonFrame.grid(row=3, column=0)

            tk.Label(frame, 
                     text=f"プレイヤー{user+1}", 
                     foreground=colors[user],
                     font=(FONTS[FONT_IDX], 16)).grid(row=0, column=0, pady=10)
            tk.Label(frame, 
                     text=f"BETCOIN" if random.randint(0, 1000) >= 2 else "BITCOIN", 
                     anchor=tk.SW,
                     font=(FONTS[FONT_IDX], 16),
                     width=22).grid(row=1, column=0)
            bet_coin_label = tk.Label(sizeFrame, 
                     text=f"20",  
                     font=(FONTS[FONT_IDX], 40), 
                     height=2)
            bet_coin_label.grid(row=0, column=0, padx=10)
            coin_onhand_label = tk.Label(sizeFrame,
                     anchor=tk.SW,
                     font=(FONTS[FONT_IDX], 20),
                     text=f"/10",
                     height=2)
            coin_onhand_label.grid(row=0, column=1, padx=10)
            self.__betCoinLabel.append((bet_coin_label, coin_onhand_label))

            tk.Button(buttonFrame, 
                      text="+10",
                      font=(FONTS[FONT_IDX], 13),
                      relief=tk.SOLID,
                      borderwidth=1,
                      command=lambda user = user: self.clicked_increase(user),
                      width=11).grid(row=0, column=0, pady=10, padx=5)
            tk.Button(buttonFrame, 
                      text="-10",
                      font=(FONTS[FONT_IDX], 13),
                      borderwidth=1,
                      relief=tk.SOLID,
                      command=lambda user = user: self.clicked_decrease(user),
                      width=11).grid(row=0, column=1, pady=10, padx=5)

        
        self.__dealer_frame = tk.Frame(self.__root)
        self.__dealer_frame.grid(row=0, column=1)
        self.__dealer_card_canvas = CardCanvas(self.__dealer_frame)
        self.__dealer_card_canvas.grid(row=0, column=0, rowspan=3)
        tk.Label(self.__dealer_frame, 
                 text=f"ディーラー", 
                 foreground="#bb00bb",
                 font=(FONTS[FONT_IDX], 16)).grid(row=0, column=1)
        self.__dealer_strength_label = tk.Label(self.__dealer_frame, 
                                                text="21", 
                                                font=(FONTS[FONT_IDX], 20),
                                                relief=tk.SOLID, 
                                                borderwidth=1,
                                                width=4, 
                                                height=2)
        self.__dealer_strength_label.grid(row=1, column=1, ipadx=5, ipady=5)

        self.__player_frame = tk.Frame(self.__root)
        self.__player_frame.grid(row=1, column=0, columnspan=3)

        self.__player_card_canvas: list[CardCanvas] = []
        self.__player_strength_label: list[tk.Label] = []
        self.__player_draw_button_frame: list[tk.Frame] = []

        for user in range(3):
            frame = tk.Frame(self.__player_frame)
            frame.grid(row=0, column=user, padx=10, pady=10)

            card_canvas = CardCanvas(frame)
            card_canvas.grid(row=1, column=0, rowspan=4)
            self.__player_card_canvas.append(card_canvas)

            tk.Label(frame, 
                     text=f"プレイヤー{user+1}", 
                     foreground=colors[user],
                     font=(FONTS[FONT_IDX], 16)).grid(row=0, column=0, columnspan=2)

            strength_label = tk.Label(frame, 
                                      text="21", 
                                      font=(FONTS[FONT_IDX], 20),
                                      relief=tk.SOLID, 
                                      borderwidth=1,
                                      height=2)
            strength_label.grid(row=5, column=0, columnspan=2, ipadx=10, ipady=2)
            self.__player_strength_label.append(strength_label)

            buttonFrame = tk.Frame(frame)
            buttonFrame.grid(row=1, column=1, rowspan=4)
            self.__player_draw_button_frame.append(buttonFrame)
            
            tk.Button(buttonFrame, 
                      text="Stand",
                      font=(FONTS[FONT_IDX], 13),
                      relief=tk.SOLID,
                      borderwidth=1,
                      width=11).grid(row=0, column=0, pady=10, padx=5)
            tk.Button(buttonFrame, 
                      text="Hit",
                      font=(FONTS[FONT_IDX], 13),
                      borderwidth=1,
                      relief=tk.SOLID,
                      command=lambda user = user: self.clicked_hit(user),
                      width=11).grid(row=1, column=0, pady=10, padx=5)


        # todo: らんきんぐ

        
        self.__mv_topwindow()
        self.__coin_display()
        self.__root.mainloop()

    def clicked_increase(self, user: int):
        self.__blackjack.bet(user, 10)
        self.__coin_display()

    def clicked_decrease(self, user: int):
        self.__blackjack.bet(user, -10)
        self.__coin_display()

    def clicked_start(self):
        cards, strength = self.__blackjack.start()
        self.__mv_gamewindow()
        self.__card_display(cards, strength)

    def clicked_hit(self, user: int):
        cards, strength = self.__blackjack.hit()
        self.__card_display(cards, strength)

    def clicked_stand(self):
        self.__stand += 1
        if not self.__stand % 3 == 0:
            self.__blackjack.stand()
            self.__card_display()
        else:
            self.__blackjack.dealer()
            self.__mv_topwindow()

    def clicked_retry(self):
        self.__blackjack.retry()
        self.__mv_topwindow()

    def clicked_exit(self):
        self.__blackjack.exit()
        self.__fin_program()

    def __mv_topwindow(self):
        self.__player_frame.grid_forget()
        self.__dealer_frame.grid_forget()
        self.__round_frame.grid(row=0, column=0)
        self.__startButtonFrame.grid(row=0, column=1, padx=100, pady=5)
        self.__bet_frame.grid(row=1, column=0, columnspan=3)

    def __mv_gamewindow(self):
        for card_canvas in self.__player_card_canvas:
            card_canvas.clear()
        self.__player_frame.grid(row=1, column=0, columnspan=3)
        self.__dealer_frame.grid(row=0, column=1)
        self.__round_frame.grid(row=0, column=0)
        self.__startButtonFrame.grid_forget()
        self.__bet_frame.grid_forget()

    def __card_display(self, cards, strength):
        coinonhand = self.__blackjack.user_coinonhand
        betcoin = self.__blackjack.user_betcoin
        stand = self.__blackjack.stand
        for user in range(3):
            self.__player_card_canvas[user].set_card(cards[user])
            self.__player_strength_label[user].config(
                text=f"${coinonhand[user]} bet: ${betcoin[user]} {strength[user]}"
            )

        self.__dealer_frame.grid(row=0, column=1)
        

    def __coin_display(self):
        bet_coin = self.__blackjack.get_user_betcoin()
        coin_onhand = self.__blackjack.get_user_coinonhand()
        for idx in range(3):
            label: tk.Label = self.__betCoinLabel[idx]
            label[0].config(text=str(bet_coin[idx]), width=4 + int(max(0, math.log10(max(1, bet_coin[idx]))-3)))
            label[1].config(text=str(coin_onhand[idx]), width=3 + int(max(0, math.log10(max(1, coin_onhand[idx]))-2)))

    def __ranking_display(self):
        pass

    def __fin_program(self):
        pass



class CardCanvas(tk.Canvas):
    MARKS = ["spade", "club", "heart", "diamond"] # 並び順は
    def __init__(self, master):
        super().__init__(master, width=156, height=220)
        self.index = 0
        self.photos = [None, None]

    def clear(self):
        self.delete("all")
        self.photos = [None, None]

    def draw(self):
        if self.photos[1]:
            self.create_image(88, 120, image=self.photos[1])
        if self.photos[0]:
            self.create_image(68, 100, image=self.photos[0])

    def add_card(self, mark: str, strength_str: str):
        strength_int = STRENGTH[strength_str]
        strength = str(strength_int).zfill(2)
        photo = tk.PhotoImage(file=f"{PATH}/cards/card_{mark}_{strength}.png")
        if photo.width() == 204:
            photo = photo.zoom(2).subsample(3)
        self.photos = [photo, self.photos[0]]
        self.draw()
    
    def set_card(self, cards: list):
        for i in range(2):
            card = cards[len(cards)-2+i]
            self.add_card(card[0], card[1])




class Hands:
    def __init__(self):
        self.clear_hands()

    def clear_hands(self):
        self.__hands: list[tuple[str, str]] = []
        self.__strength = 0

    def get_hands_list(self) -> list[tuple[str, str]]:
        return self.__hands
    
    def add_hands(self, suit, number) -> None:
        self.__hands.append((suit, number))

    def cal_hands_strength(self) -> None:
        strength = 0
        ace = 0
        for number in [x[1] for x in self.__hands]:
            if number == 'A':
                ace += 1
            else:
                strength += STRENGTH[number]
        for _ in range(ace):
            if strength + 11 <= 21:
                strength += 11
            else:
                strength += 1
        self.__strength = strength
    
    def get_hands_strength(self) -> int:
        return self.__strength
    

class Cards:
    def __init__(self):
        self.__cards = []
        self.__reset_cards()

    def __reset_cards(self) -> None:
        self.__cards = [(suit, number) for suit in CardCanvas.MARKS for number in STRENGTH.keys()]

    def draw_card(self) -> tuple[str, str]:
        card = random.choice(self.__cards)
        self.__cards.remove(card)
        return card
    
    def reset_cards(self) -> None:
        self.__reset_cards()



class BlackJackTest:
    def __init__(self):
        self.__user_coinonhand = np.array([
            [f"プレイヤー{x}" for x in range(3)],
            [100 for x in range(3)]
        ])
        self.__user_betcoin = [100, 1000, 100000]
        self.__user_hands = [Hands() for _ in range(3)]
        self.__dealer_hands = Hands()
        self.__card = Cards()

    
    def bet(self, user: int, bc):
        if self.__user_betcoin[user] <= 10 and bc < 0:
            return
        elif (self.__user_coinonhand[user] < bc):
            return
        self.__user_betcoin[user] += bc
        self.__user_coinonhand[user] -= bc
        return(self.__user_betcoin)

    def start(self):
        return [[("spade", "J"), ("diamond", "10")], [("spade", "J"), ("diamond", "10")], [("spade", "J"), ("diamond", "10")]], (21, 21, 21)

    def hit(self):
        return [("spade", "J"), ("diamond", "10")], 21

    def stand(self):
        pass

    def dealer(self):
        pass

    def retry(self):
        pass

    def exit(self):
        pass

    def get_user_betcoin(self):
        return self.__user_betcoin
    
    def get_user_coinonhand(self):
        return self.__user_coinonhand


if __name__ == "__main__":
    BlackJackControl()