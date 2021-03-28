import tkinter as tk

class InputLabel(tk.Label):
    def __init__(self, master=None):
        self.S = tk.StringVar(value='')
        super().__init__(master, textvariable=self.S, relief=tk.SUNKEN, anchor=tk.W, cursor='xterm', font='TkFixedFont', highlightthickness=2)
        self.bind('<Key>', self.key_logic)
        self.bind('<Button-1>', self.mouse_logic)
        self.grid(row=0, column=0, sticky='WE')

        self.cursor = tk.Frame(self, height=17, width=2, background='grey')
        self.pos_cursor = 0

    def key_logic(self, event):
        print(event)
        if event.keysym == 'Left':
            self.pos_cursor = max(0, self.pos_cursor - 1)
        elif event.keysym == 'Right':
            self.pos_cursor = min(len(self.S.get()), self.pos_cursor + 1)
        elif event.keysym == 'Home':
            self.pos_cursor = 0
        elif event.keysym == 'End':
            self.pos_cursor = len(self.S.get())
        elif event.keysym == 'BackSpace':
            if self.S.get() and self.pos_cursor:
                self.S.set(self.S.get()[:self.pos_cursor - 1] + self.S.get()[self.pos_cursor:])
                self.pos_cursor -= 1
        elif event.char:
            self.S.set(self.S.get()[:self.pos_cursor] + event.char + self.S.get()[self.pos_cursor:])
            self.pos_cursor += 1
        self.cursor.place(x=(self.pos_cursor * 8 + 1), y=2)

    def mouse_logic(self, event):
        self.focus()
        if (event.x // 8 <= len(self.S.get())): 
            self.pos_cursor = event.x // 8
        else:
            self.pos_cursor = len(self.S.get())
        self.cursor.place(x=(self.pos_cursor * 8 + 1), y=2)
        


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Label edit')

    button_quit = tk.Button(window, text='Quit', command=window.quit)
    button_quit.grid(row=1, column=0, sticky='E')

    input_label = InputLabel(window)

    window.mainloop()
