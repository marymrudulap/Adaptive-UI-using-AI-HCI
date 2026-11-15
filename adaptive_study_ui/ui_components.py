"""Dependency-free rounded surfaces and keyboard-accessible answer controls."""
import tkinter as tk


def rounded(canvas, x1, y1, x2, y2, radius=16, **options):
    points = [x1+radius,y1,x2-radius,y1,x2,y1,x2,y1+radius,
              x2,y2-radius,x2,y2,x2-radius,y2,x1+radius,y2,
              x1,y2,x1,y2-radius,x1,y1+radius,x1,y1]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **options)


class Surface(tk.Canvas):
    def __init__(self, parent, background='#ffffff', surround='#f5f6fa', padding=24, **kw):
        super().__init__(parent, bg=surround, highlightthickness=0, bd=0, **kw)
        self.color, self.padding = background, padding
        self.body = tk.Frame(self, bg=background)
        self.window = self.create_window(padding, padding, anchor='nw', window=self.body)
        self.bind('<Configure>', self.arrange)
        self.body.bind('<Configure>', self.request_height)

    def request_height(self, event=None):
        self.configure(height=self.body.winfo_reqheight() + 2*self.padding)

    def arrange(self, event):
        self.delete('surface')
        rounded(self, 1, 1, event.width-1, event.height-1, 20,
                fill=self.color, outline='#e7e9f0', tags='surface')
        self.tag_lower('surface')
        self.itemconfigure(self.window, width=max(1, event.width-2*self.padding))
        self.after_idle(self.request_height)


class Answer(tk.Canvas):
    def __init__(self, parent, variable, value):
        super().__init__(parent, height=62, bg='white', bd=0,
                         highlightthickness=0, takefocus=True, cursor='hand2')
        self.variable, self.value = variable, value
        self.text, self.state, self.hover, self.focused = '', 'normal', False, False
        self.result = None
        variable.trace_add('write', lambda *_: self.draw())
        self.bind('<Configure>', lambda e: self.draw())
        self.bind('<Enter>', lambda e: self.enter(True))
        self.bind('<Leave>', lambda e: self.enter(False))
        self.bind('<FocusIn>', lambda e: self.focus(True))
        self.bind('<FocusOut>', lambda e: self.focus(False))
        self.bind('<Button-1>', self.choose)
        self.bind('<space>', self.choose)
        self.bind('<Return>', self.choose)
        self.bind('<Down>', lambda e: self.move(1))
        self.bind('<Up>', lambda e: self.move(-1))

    def move(self, direction):
        peers = [w for w in self.master.winfo_children() if isinstance(w, Answer)]
        peers[(self.value + direction) % len(peers)].choose()
        return 'break'

    def focus(self, value):
        self.focused = value
        self.draw()

    def enter(self, value):
        self.hover = value
        self.draw()

    def choose(self, event=None):
        if self.state != 'disabled':
            self.focus_set()
            self.variable.set(self.value)
        return 'break'

    def config(self, **kw):
        for key in ('text', 'state', 'result'):
            if key in kw:
                setattr(self, key, kw.pop(key))
        if kw:
            super().configure(**kw)
        self.draw()

    def draw(self):
        self.delete('all')
        selected = self.variable.get() == self.value
        fill = '#eeedff' if selected else ('#f5f5fc' if self.hover and self.state != 'disabled' else '#ffffff')
        edge = '#7060dd' if selected or self.focused else '#e3e6ef'
        ink = '#4636a8' if selected else '#344054'
        if self.result == 'correct':
            fill, edge, ink = '#ecf9f2', '#37a574', '#176844'
        elif self.result == 'incorrect':
            fill, edge, ink = '#fff1ef', '#dd867c', '#a44138'
        w = max(self.winfo_width(), 200)
        rounded(self, 2, 2, w-2, 60, 12, fill=fill, outline=edge, width=2 if selected or self.focused else 1)
        rounded(self, 16, 15, 48, 47, 7, fill='#7060dd' if selected else '#f2f4f8', outline='')
        self.create_text(32, 31, text=chr(65+self.value), fill='white' if selected else '#667085', font=('Segoe UI', 10, 'bold'))
        self.create_text(62, 31, text=self.text, width=w-115, anchor='w', fill=ink, font=('Segoe UI', 11))
        self.create_oval(w-36, 23, w-20, 39, outline=edge, width=2)
        if selected:
            self.create_oval(w-32, 27, w-24, 35, fill=edge, outline='')
