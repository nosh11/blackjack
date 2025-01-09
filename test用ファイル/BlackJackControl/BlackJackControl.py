from settings import *

import math
import tkinter as tk
import random

from blackjack import BlackJack

class BlackJackControl:
    def __init__(self):
        # ルートウィンドウの設定
        self.__root = tk.Tk()
        self.__root.title("Black Jack")
        
        # BlackJackクラスのインスタンス生成
        self.__bj = BlackJack()

        self.__stand = 0
        self.__lock = False

        # ターン表示フレームの設定
        self.__round_frame = tk.Frame(self.__root, width=10, height=3)
        self.__round_frame.grid(row=0, column=0)
        tk.Label(self.__round_frame, 
                  text="ROUND",
                  font=(FONTS[FONT_IDX], 15),
                  anchor=tk.E,
                  height=1).grid(row=0, column=0, columnspan=10)
        turnFrame = tk.Frame(self.__round_frame)
        turnFrame.grid(row=1, column=7)

        self.__round_label = tk.StringVar(value="1")
        tk.Label(turnFrame, 
                 textvariable=self.__round_label,
                 font=(FONTS[FONT_IDX], 30),
                 anchor=tk.E).grid(row=0, column=0)
        tk.Label(turnFrame,
                  text="/3",
                  font=(FONTS[FONT_IDX], 20),
                  anchor=tk.SW,
                  height=2).grid(row=0, column=1)

        # トップウィンドウ - スタートボタン周りのフレーム設定
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
        
        # 空フレームの設定
        empty = tk.Frame(self.__root)
        empty.grid(row=0, column=2)
        tk.Label(empty, text="", width=10).grid(row=0, column=0)

        # トップウィンドウの設定
        self.__bet_frame = tk.Frame(self.__root)
        self.__bet_frame.grid(row=1, column=0, columnspan=3)

        # トップウィンドウ - ベット周りのフレーム設定
        self.__betUserFrame = tk.Frame(self.__bet_frame, width=40)
        self.__betUserFrame.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E)
        self.__betCoinLabel: list[tuple[tk.Label, tk.Label]] = []
        for user in range(3):
            frame = tk.Frame(self.__betUserFrame)
            frame.grid(row=0, column=user, padx=10, pady=10)

            sizeFrame = tk.Frame(frame, relief=tk.SOLID, borderwidth=1, width=12)
            buttonFrame = tk.Frame(frame)
            sizeFrame.grid(row=2, column=0, padx=5)
            buttonFrame.grid(row=3, column=0)

            tk.Label(frame, 
                     text=f"プレイヤー{user+1}", 
                     foreground=COLORS[user],
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

        
        # ディーラーフレームの設定
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

        # プレイヤーフレームの設定
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
                     foreground=COLORS[user],
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
                      command=self.clicked_stand,
                      width=11).grid(row=0, column=0, pady=10, padx=5)
            tk.Button(buttonFrame, 
                      text="Hit",
                      font=(FONTS[FONT_IDX], 13),
                      borderwidth=1,
                      relief=tk.SOLID,
                      command=self.clicked_hit,
                      width=11).grid(row=1, column=0, pady=10, padx=5)

        # ランキングフレームの設定
        self.__ranking_frame = tk.Frame(self.__root)
        tk.Label(self.__ranking_frame,
                    text="RESULT",
                    font=(FONTS[FONT_IDX], 33, "bold"),
                    width=10, height=1).grid(row=0, column=0, columnspan=2)
        tk.Button(self.__ranking_frame,
                    text="RETRY",
                    relief=tk.SOLID,
                    font=(FONTS[FONT_IDX], 20),
                    foreground='#ffffff',
                    background='#ED7D31',
                    command=self.clicked_retry,
                    width=10, height=1).grid(row=2, column=0, ipadx=10, pady = 10)
        tk.Button(self.__ranking_frame,
                    text="EXIT",
                    relief=tk.SOLID,
                    font=(FONTS[FONT_IDX], 20),
                    foreground='#ffffff',
                    background='#5B9BD5',
                    command=self.clicked_exit,
                    width=10, height=1).grid(row=2, column=1, ipadx=10, pady = 10)
        self.__mv_topwindow()
        self.__coin_display()
        self.__root.mainloop()

    def clicked_increase(self, user: int):
        self.__bj.bet(user, 10)
        self.__coin_display()

    def clicked_decrease(self, user: int):
        self.__bj.bet(user, -10)
        self.__coin_display()

    def clicked_start(self):
        self.__bj.start()
        self.__lock = False
        self.__mv_gamewindow()
        self.__go_to_next_player()
        self.__card_display()

    def clicked_hit(self):
        self.__bj.hit(self.__get_current_player_index())
        self.__go_to_next_player()
        self.__card_display()

    def clicked_stand(self):
        self.stand()
        self.__card_display()

    def clicked_retry(self):
        self.__bj.clear_result()
        self.__mv_topwindow()

    def clicked_exit(self):
        self.__root.destroy()

    def __mv_topwindow(self):
        self.__coin_display()
        self.__player_frame.grid_forget()
        self.__dealer_frame.grid_forget()
        self.__round_frame.grid(row=0, column=0)
        self.__startButtonFrame.grid(row=0, column=1, padx=100, pady=5)
        self.__bet_frame.grid(row=1, column=0, columnspan=3)
        self.__ranking_frame.grid_forget()

    def __mv_gamewindow(self):
        self.__card_display()
        self.__player_frame.grid(row=1, column=0, columnspan=3)
        self.__dealer_frame.grid(row=0, column=1)
        self.__round_frame.grid(row=0, column=0)
        self.__startButtonFrame.grid_forget()
        self.__bet_frame.grid_forget()
        self.__ranking_frame.grid_forget()

    def __round_display(self):
        self.__round_label.set(str(self.__get_round()))

    def __card_display(self):
        self.__round_display()
        bets = self.__bj.get_user_betcoin()
        coins = self.__bj.get_user_coinonhand()
        cards = self.__bj.get_user_hands()
        strength = self.__bj.get_user_strength()

        for user in range(3):
            self.__player_card_canvas[user].update_cards(cards[user])
            self.__player_strength_label[user].config(
                text=f"${coins[user]} bet: ${bets[user]} {strength[user]}"
            )
            if self.__get_current_player_index() == user and (not self.__lock):
                self.__player_draw_button_frame[user].grid(row=1, column=1, rowspan=4)
            else:
                self.__player_draw_button_frame[user].grid_forget()
        
        self.__dealer_display()
    
    def __dealer_display(self):
        self.__dealer_card_canvas.update_cards(self.__bj.get_dealer_hand())
        self.__dealer_strength_label.config(text=f"{self.__bj.get_dealer_strength()}")

    def __draw_dealer_hand(self):
        if self.__bj.get_dealer_strength() >= 17:
            self.__bj.judge()
            self.__stand += 1

            if self.__get_round() > 3:
                self.__root.after(3000, self.__ranking_display)
                return
            else:
                self.__root.after(3000, self.__mv_topwindow)
        else:
            self.__bj.dealer()
            self.__dealer_display()
            self.__root.after(1000, self.__draw_dealer_hand)

    def __coin_display(self):
        self.__round_display()
        bets = self.__bj.get_user_betcoin()
        coins = self.__bj.get_user_coinonhand()
        for idx in range(3):
            bet = bets[idx]
            coin = coins[idx]

            width_0 = 4 + int(max(0, len(str(bet)) - 3))
            width_1 = 3 + int(max(0, len(str(coin)) - 2))

            labels = self.__betCoinLabel[idx]
            labels[0].config(text=str(bet), width=width_0)
            labels[1].config(text=str(coin), width=width_1)

    def __ranking_display(self):
        self.__ranking_frame.grid(row=0, column=0)
        Podium(self.__ranking_frame, self.__bj.ranking()).grid(row=1, column=0, columnspan=2,  padx=100)        

        self.__player_frame.grid_forget()
        self.__dealer_frame.grid_forget()
        self.__round_frame.grid_forget()
        self.__startButtonFrame.grid_forget()
        self.__bet_frame.grid_forget()

    def __get_round(self):
        return self.__stand // 4 + 1
    
    def __get_current_player_index(self):
        return self.__stand % 4

    def __go_to_next_player(self):
        index = self.__get_current_player_index()
        if index == 3:
            self.__lock = True
            self.__draw_dealer_hand()
        else:
            strength = self.__bj.get_user_strength()[index]
            if strength >= 21:
                self.__stand += 1
                self.__go_to_next_player()
            else:
                self.__lock = False
                self.__card_display()
    
    def stand(self):
        # 次のプレイヤーに移る。
        self.__stand += 1
        self.__go_to_next_player()


MAX_VIEW_CARD = 5
MOVE_AMOUNT = 20

SIZE = MAX_VIEW_CARD * MOVE_AMOUNT

# 136/2 = 68

class CardCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=136+SIZE, height=200+SIZE)
        self.cards: list[tuple[str, str]] = []

    def draw(self):
        for i, card in enumerate(self.cards):
            mark, strength_str = card

            mark_str, color = MARKS[mark]

            # 右下
            move = MOVE_AMOUNT * i
            x, y = 136+SIZE - move, 200+SIZE - move

            self.create_rectangle(x - 136, y - 200, x, y, fill="white")
            
            self.create_text(x - 116, y - 180, text=strength_str, font=(FONTS[FONT_IDX], 20), fill=color)
            self.create_text(x - 116, y - 150, text=mark_str, font=(FONTS[FONT_IDX], 20), fill=color)
            
            self.create_text(x - 20, y - 20, text=strength_str, font=(FONTS[FONT_IDX], 20), fill=color, angle=180)
            self.create_text(x - 20, y - 50, text=mark_str, font=(FONTS[FONT_IDX], 20), fill=color, angle=180)
            
    def update_cards(self, cards: list[tuple[str, int]]):
        self.delete("all")
        self.cards = cards
        self.draw()

S = 5

class Podium(tk.Frame):
    def __init__(self, master, names: list[str]):
        super().__init__(master, width=150*S, height=80*S)
        tk.Label(self, 
                 text="2", 
                 bg="black", 
                 fg="white",
                 font=(FONTS[FONT_IDX], 30), 
                 width=8, height=5).grid(row=5, column=0, rowspan=5, columnspan=2)
        tk.Label(self, 
                 text="1", 
                 bg="black", 
                 font=(FONTS[FONT_IDX], 30), 
                 fg="white",
                 width=8, height=7).grid(row=3, column=2, rowspan=7, columnspan=2)
        tk.Label(self, 
                 text="3", 
                 bg="black", 
                 font=(FONTS[FONT_IDX], 30), 
                 fg="white",
                 width=8, height=3).grid(row=7, column=4, rowspan=3, columnspan=2)

        POS = [(1, 2), (3, 0), (5, 4)]

        for i in range(3):
            name = names[i]
            tk.Label(self, 
                     text=f"{name}",
                     fg=COLORS[i],
                     font=(FONTS[FONT_IDX], 20)).grid(row=POS[i][0], column=POS[i][1])

if __name__ == "__main__":
    BlackJackControl()