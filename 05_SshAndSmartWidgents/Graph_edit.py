import tkinter as tk
import tkinter.colorchooser 

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

class Application(tk.Frame):
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        '''Create all the widgets'''

class App(Application):
    def create_widgets(self):
        super().create_widgets()
        self.create_text()
        self.create_graph()

    def create_text(self):
        self.text_frame = tk.LabelFrame(self, text='Text')
        self.text_frame.grid(row=0, column=0, sticky='NEWS')
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)
        
        self.text = tk.Text(self.text_frame, undo=True, font='fixed')
        self.text.grid(sticky='NEWS')
        self.text.bind('<KeyRelease>', self.change_object)
        self.text.tag_config('error', background='#aa0000', font='fixed')

    def create_graph(self):
        self.graph_frame = tk.Frame(self)
        self.graph_frame.grid(row=0, column=1, sticky='NEWS')
        self.graph_frame.columnconfigure(5, weight=1)
        self.graph_frame.rowconfigure(1, weight=1)

        self.border_color = '#ff0000'
        self.fill_color = '#0000ff'
        self.mouse_click_flg = False
        self.object_count = 0
        self.selected_item = ()

        self.border_object = tk.Button(self.graph_frame, text='Border', command=self.border_color_shoose)
        self.border_object.grid(column=0, row=0)
        
        self.width_border = tk.StringVar()
        self.width_border.set('1')
        self.width_object = tk.Spinbox(self.graph_frame, textvariable=self.width_border, from_=0, to=99, width=2)
        self.width_object.grid(column=1, row=0)
        
        self.fill_object = tk.Button(self.graph_frame, text='Fill', command=self.fill_color_shoose)
        self.fill_object.grid(column=2, row=0)

        self.color_test = tk.Label(self.graph_frame, background=self.fill_color, foreground=self.border_color,
                                   text='O', font=('Helvetica', '14', 'bold'), width=1)
        self.color_test.grid(column=3, row=0)
        
        self.object_name = tk.StringVar()
        self.object_set = 'oval', 'rectangle'
        self.object_name.set('oval')
        self.object_menu = tk.OptionMenu(self.graph_frame, self.object_name, *self.object_set)
        self.object_menu.grid(column=4, row=0)
        
        self.pos_cursor = tk.StringVar()
        self.pos_label = tk.Label(self.graph_frame, textvariable=self.pos_cursor)
        self.pos_label.grid(column=5, row=0, sticky='WE')
        
        self.Q = tk.Button(self.graph_frame, text='Quit', command=self.master.quit)
        self.Q.grid(column=6, row=0)

        self.create_canvas()

    def create_canvas(self):
        self.graph = tk.Canvas(self.graph_frame, background='#BBBBBB')
        self.graph.grid(column=0, row=1, columnspan=7, sticky='NEWS')
        self.graph.bind('<Button-1>', self.mouse_click)
        self.graph.bind('<Motion>', self.mouse_motion)
        self.graph.bind('<ButtonRelease-1>', self.mouse_release)

    def border_color_shoose(self):
        (_, self.border_color) = tk.colorchooser.askcolor(self.border_color)
        self.color_test.configure(foreground=self.border_color)

    def fill_color_shoose(self):
        (_, self.fill_color) = tk.colorchooser.askcolor(self.fill_color)
        self.color_test.configure(background=self.fill_color)

    def mouse_click(self, event):
        self.mouse_click_flg = True
        self.selected_item = self.graph.find_withtag(tk.CURRENT)
        self.object_init_x = event.x
        self.object_init_y = event.y
        if len(self.selected_item) == 0:
            self.object_count += 1
            if self.object_name.get() == 'oval':
                self.graph.create_oval(event.x, event.y, event.x+1, event.y+1, fill=self.fill_color,
                                       outline=self.border_color, width=self.width_border.get())
            else:
                self.graph.create_rectangle(event.x, event.y, event.x+1, event.y+1, fill=self.fill_color,
                                            outline=self.border_color, width=self.width_border.get())

    def mouse_motion(self, event):
        self.pos_cursor.set(f'{event.x}:{event.y}')
        if self.mouse_click_flg and len(self.selected_item) == 0:
            x0, y0, x1, y1 = self.graph.coords(self.object_count)
            if (event.x - self.object_init_x != 0) and (event.y - self.object_init_y != 0):
                if x0 < self.object_init_x:
                    x1 = x0
                if y0 < self.object_init_y:
                    y1 = y0
                xScale = (event.x - self.object_init_x) / (x1 - self.object_init_x)
                yScale = (event.y - self.object_init_y) / (y1 - self.object_init_y)
                self.graph.scale(self.object_count, self.object_init_x, self.object_init_y, xScale, yScale)
        elif self.mouse_click_flg:
            self.graph.move(self.selected_item[0], event.x-self.object_init_x, event.y-self.object_init_y)
            self.object_init_x = event.x
            self.object_init_y = event.y

    def mouse_release(self, event, insert_str=None):
        self.mouse_click_flg = False
        if len(self.selected_item) == 0 or insert_str:
            x0, y0, x1, y1 = self.graph.coords(self.object_count)
            if not insert_str:
                if self.object_count == int(self.text.index('end').split('.')[0]):
                    self.text.insert('end', '\n')
                insert_str = f'{self.object_name.get()} <{round(x0)} {round(y0)} {round(x1)} {round(y1)}> {self.width_border.get()} {self.border_color} {self.fill_color}\n'
                self.text.insert(f'{self.object_count}.0', insert_str)
            words = insert_str.split(' ')
            print(words)
            self.text.tag_add(f'name[{self.object_count}]', f'{self.object_count}.0', f'{self.object_count}.{len(words[0])}')
            coord_end = sum([len(words[i]) for i in range(5)]) + 3
            self.text.tag_add(f'coords[{self.object_count}]', f'{self.object_count}.{len(words[0])+2}', f'{self.object_count}.{coord_end}')
            width_end = coord_end + len(words[5]) + 2
            self.text.tag_add(f'width[{self.object_count}]', f'{self.object_count}.{coord_end+2}', f'{self.object_count}.{width_end}')
            border_end = width_end + len(words[6]) + 1
            self.text.tag_add(f'border_color[{self.object_count}]', f'{self.object_count}.{width_end+1}', f'{self.object_count}.{border_end}')
            fill_end = border_end + len(words[7]) + 1
            self.text.tag_add(f'fill_color[{self.object_count}]', f'{self.object_count}.{border_end+1}', f'{self.object_count}.{fill_end}')

            self.text.tag_config(f'name[{self.object_count}]', foreground='#0000ff', font='fixed')
            self.text.tag_config(f'coords[{self.object_count}]', foreground='#00bfff', font='fixed')
            self.text.tag_config(f'width[{self.object_count}]', foreground='#b8860b', font='fixed')
            self.text.tag_config(f'border_color[{self.object_count}]', foreground='#228b22', font='fixed')
            self.text.tag_config(f'fill_color[{self.object_count}]', foreground='#ff1493', font='fixed')

        else:
            coord_begin = int(app.text.search('<', f'{self.selected_item[0]}.0')[2:]) + 1
            coord_end = app.text.search('>', f'{self.selected_item[0]}.0')
            self.text.delete(f'{self.selected_item[0]}.{coord_begin}', coord_end)
            x0, y0, x1, y1 = self.graph.coords(self.selected_item[0])
            self.text.insert(f'{self.selected_item[0]}.{coord_begin}', f'{round(x0)} {round(y0)} {round(x1)} {round(y1)}', f'coords[{self.selected_item[0]}]')

    def change_object(self, event):
        if event.keysym in {'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Return'}:
            return
        for item in range(self.object_count):
            self.graph.delete(item + 1)
        self.create_canvas()
        self.object_count = 0
        for i, line in enumerate(self.text.get('1.0', 'end').splitlines()):
            eror_flg = False
            words = line.split(' ')
            error_flg = (len(words) != 8 or words[0] != 'oval' and words[0] != 'rectangle' or
                         words[1][0] != '<' or len(words[1]) < 2 or not is_number(words[1][1:]) or not is_number(words[2]) or not is_number(words[3]) or
                         words[4][-1] != '>' or len(words[4]) < 2 or not is_number(words[4][:-1]) or not words[5].isdigit() or
                         len(words[6]) != 7 or words[6][0] != '#' or not is_hex(words[6][1:]) or
                         len(words[7]) != 7 or words[7][0] != '#' or not is_hex(words[7][1:]))
            if error_flg:
                self.text.tag_add('error', f'{i+1}.0', f'{i+1}.{len(line)}')
            else:
                self.object_count += 1
                if words[0] == 'oval':
                    self.graph.create_oval(words[1][1:], words[2], words[3], words[4][:-1], fill=words[7], outline=words[6], width=words[5])
                else:
                    self.graph.create_rectangle(words[1][1:], words[2], words[3], words[4][:-1], fill=words[7], outline=words[6], width=words[5])
                print(line, self.object_count, self.graph.find_all())
                self.mouse_release(event={}, insert_str=line)
                self.text.tag_remove('error', f'{i+1}.0', f'{i+1}.{len(line)}')

        
app = App(title="Graph edit")
app.mainloop()
