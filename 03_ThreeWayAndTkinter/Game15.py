import tkinter as tk
from tkinter import messagebox
from random import shuffle

def position_in_sequence(sequence, x=0):
    for i in range(len(sequence)):
        if sequence[i] == x:
            return i

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.grid()
        for i in range(4):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i + 1, weight=1)
        self.create_buttons()

    def create_buttons(self):
        self.new_btn = tk.Button(self, text='New', command=self.new_game)
        self.new_btn.grid(column=0, columnspan=2, row=0, sticky='NS')
        self.exit_btn = tk.Button(self, text='Exit', command=self.quit)
        self.exit_btn.grid(column=2, columnspan=2, row=0, sticky='NS')
        self.buttons = []
        for i in range(1, 16):
            self.buttons.append(tk.Button(self, text=str(i)))
            self.buttons[i - 1]['command'] = lambda i=i: self.move_button(i)

    def new_game(self):
        self.sequence = list(range(1, 16))
        N = 0
        shuffle(self.sequence)
        for i in range(15):
            for j in self.sequence[self.sequence[i] + 1:]:
                if j < i:
                    N += 1
        if N % 2:
            self.sequence[0], self.sequence[1] = self.sequence[1], self.sequence[0]
        self.sequence.append(0)
        for i in range(15):
            self.buttons[self.sequence[i] - 1].grid(row=(i // 4) + 1, column=(i % 4), sticky='NEWS')
        self.check_win()

    def move_button(self, num_button):
        pos_0 = position_in_sequence(self.sequence)
        pos_button = position_in_sequence(self.sequence, num_button)
        if (abs(pos_button - pos_0) == 1) or (abs(pos_button - pos_0) == 4):
            self.sequence[pos_button], self.sequence[pos_0] = 0, self.sequence[pos_button]
            self.buttons[num_button - 1].grid(row=(pos_0 // 4) + 1, column=(pos_0 % 4), sticky='NEWS')
            self.check_win()

    def check_win(self):
        if self.sequence[:-1] == list(range(16))[1:]:
            tk.messagebox.showinfo('Game 15', 'You win')
            self.quit()

if __name__ == '__main__':
    game = Game()
    game.title('Game 15')
    game.mainloop()