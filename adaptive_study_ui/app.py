"""Local adaptive HCI study interface. Run: python app.py"""
import tkinter as tk
from tkinter import ttk
from model import Session
from ui_components import Surface, Answer

QUESTIONS = [
    ('What does HCI study?', ['Human interaction with computers', 'Only computer hardware', 'Only databases'], 0,
     'Think about people using technology.', 'HCI studies the design and use of interactive systems by people.'),
    ('Which interface adapts automatically?', ['A fixed printed menu', 'Help that changes after repeated errors', 'A manually selected wallpaper'], 1,
     'Look for a change triggered by observed interaction.', 'An adaptive interface changes during use based on a user model or context.'),
    ('Which control supports user autonomy?', ['Hide all settings', 'Force every recommendation', 'Allow a manual override'], 2,
     'The person should retain a choice.', 'Override controls let users correct an inappropriate automated decision.'),
    ('What is a user model?', ['A description of user knowledge or preferences', 'A monitor brand', 'A network cable'], 0,
     'It represents something about the person using the system.', 'A user model represents relevant characteristics inferred or explicitly supplied.'),
    ('What should an AI interface explain?', ['Only its logo', 'Why an adaptation occurred', 'Nothing about its behavior'], 1,
     'Unexpected changes need a reason.', 'An explanation helps the user understand and challenge an adaptation.'),
    ('Which is evidence of effectiveness?', ['An attractive color', 'A developer assumption', 'A controlled usability evaluation'], 2,
     'Think about measuring outcomes with users.', 'Effectiveness requires evaluation; passing software tests does not prove UX improvement.'),
]

class StudyApp:
    def __init__(self, root):
        self.root = root
        self.session = Session()
        self.index = 0
        self.used_hint = False
        self.submitted = False
        root.title('Adaptive Study UI')
        root.geometry('1180x860')
        root.minsize(940, 700)
        root.configure(bg='#f5f6fa')
        self.configure_styles()
        sidebar = tk.Frame(root, bg='#171d35', width=228)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text='a /', bg='#171d35', fg='#b9afff', font=('Segoe UI', 32, 'bold')).pack(anchor='w', padx=28, pady=(32, 0))
        tk.Label(sidebar, text='adaptive', bg='#171d35', fg='white', font=('Segoe UI', 22, 'bold')).pack(anchor='w', padx=28)
        tk.Label(sidebar, text='A little practice. More clarity.', bg='#171d35', fg='#a6aec6', font=('Segoe UI', 9)).pack(anchor='w', padx=28, pady=(5, 38))
        tk.Label(sidebar, text='WORKSPACE', bg='#171d35', fg='#818aa7', font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=28, pady=(0, 12))
        tk.Label(sidebar, text='  ◈   Study session', bg='#2c3151', fg='#e6e1ff', font=('Segoe UI', 11, 'bold'), anchor='w', padx=16, pady=14).pack(fill='x', padx=14)
        tk.Label(sidebar, text='HCI FUNDAMENTALS', bg='#171d35', fg='#818aa7', font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=28, pady=(36, 10))
        tk.Label(sidebar, text='6 questions\nOne concept at a time.', bg='#171d35', fg='#c4cbdd', justify='left', font=('Segoe UI', 11), anchor='w').pack(anchor='w', padx=28)
        privacy = tk.Frame(sidebar, bg='#202740', padx=16, pady=18)
        privacy.pack(side='bottom', fill='x', padx=18, pady=24)
        tk.Label(privacy, text='●  Private by design', bg='#202740', fg='#a9e3cb', font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        tk.Label(privacy, text='Runs locally. No account.\nYour history clears on exit.', bg='#202740', fg='#a6aec6', justify='left', font=('Segoe UI', 9)).pack(anchor='w', pady=(8, 0))

        outer = tk.Frame(root, bg='#f5f6fa')
        outer.pack(side='left', fill='both', expand=True)
        scroll = tk.Canvas(outer, bg='#f5f6fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient='vertical', command=scroll.yview)
        scrollbar.pack(side='right', fill='y')
        scroll.pack(fill='both', expand=True)
        scroll.configure(yscrollcommand=scrollbar.set)
        frame = ttk.Frame(scroll, padding=(36, 30), style='Page.TFrame')
        window = scroll.create_window(0, 0, window=frame, anchor='nw')
        scroll.bind('<Configure>', lambda e: scroll.itemconfigure(window, width=e.width))
        frame.bind('<Configure>', lambda e: scroll.configure(scrollregion=scroll.bbox('all')))
        def wheel(event):
            if scroll.bbox('all') and scroll.bbox('all')[3] > scroll.winfo_height():
                scroll.yview_scroll(int(-event.delta / 120), 'units')
        root.bind('<MouseWheel>', wheel)
        top = ttk.Frame(frame, style='Page.TFrame')
        top.pack(fill='x')
        ttk.Label(top, text='WORKSPACE  /  HCI FUNDAMENTALS', style='Eyebrow.TLabel').pack(side='left')
        ttk.Button(top, text='↻  Reset session', command=self.reset).pack(side='right')
        ttk.Label(frame, text='A little practice. More clarity.', style='Title.TLabel').pack(anchor='w', pady=(20, 10))
        ttk.Label(frame, text='A focused space to learn, reflect, and keep moving forward.', style='Subtitle.TLabel').pack(anchor='w', pady=(0, 24))
        bar = ttk.Frame(frame, style='Page.TFrame')
        bar.pack(fill='x', pady=(0, 14))
        ttk.Label(bar, text='YOUR STUDY SESSION', style='Eyebrow.TLabel').pack(side='left')
        self.mode = tk.StringVar(value='Auto')
        menu = ttk.Combobox(bar, textvariable=self.mode, values=['Auto', 'Support', 'Standard', 'Challenge'], state='readonly', width=11, font=('Segoe UI', 10))
        menu.pack(side='right')
        menu.bind('<<ComboboxSelected>>', self.change_mode)
        ttk.Label(bar, text='Learning mode  ', style='Page.TLabel').pack(side='right')

        surface = Surface(frame, padding=24)
        surface.pack(fill='x')
        card = surface.body
        self.status = ttk.Label(card, style='Status.TLabel')
        self.status.pack(anchor='w')
        self.progress = ttk.Progressbar(card, maximum=len(QUESTIONS), style='Study.Horizontal.TProgressbar')
        self.progress.pack(fill='x', pady=(14, 12))
        self.reason = ttk.Label(card, style='Muted.TLabel', wraplength=650)
        self.reason.pack(anchor='w', fill='x')
        self.question = ttk.Label(card, style='Question.TLabel', wraplength=650)
        self.question.pack(anchor='w', fill='x', pady=(26, 6))
        ttk.Label(card, text='Select the answer that fits best.', style='Muted.TLabel').pack(anchor='w', pady=(0, 18))
        self.answer = tk.IntVar(value=-1)
        self.options = []
        for i in range(3):
            button = Answer(card, self.answer, i)
            button.pack(fill='x', pady=5)
            self.options.append(button)
        self.help = ttk.Label(card, style='Help.TLabel', wraplength=620, padding=(14, 12))
        self.help.pack(fill='x', pady=(18, 20))
        controls = ttk.Frame(card, style='Card.TFrame')
        controls.pack(fill='x')
        self.hint_button = ttk.Button(controls, text='✧  Show hint', command=self.hint)
        self.hint_button.pack(side='left')
        self.submit_button = ttk.Button(controls, text='Submit answer  →', command=self.submit, style='Primary.TButton')
        self.submit_button.pack(side='right')
        self.next_button = ttk.Button(controls, text='Next question  →', command=self.next_question, state='disabled')
        self.next_button.pack(side='right', padx=10)
        self.feedback = ttk.Label(card, style='Feedback.TLabel', wraplength=650)
        self.feedback.pack(anchor='w', fill='x', pady=(16, 0))
        ttk.Label(frame, text='ABOUT THIS DEMO', style='Eyebrow.TLabel').pack(anchor='w', pady=(22, 6))
        ttk.Label(frame, text='Trained on 12 synthetic examples. Recommendations are not an ability assessment.\nSession history stays in memory and clears when you reset or exit.', style='Footer.TLabel', wraplength=700).pack(anchor='w')
        card.bind('<Configure>', self.resize_content)
        self.load_question()

    def configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('.', font=('Segoe UI', 10), foreground='#344054')
        style.configure('Page.TFrame', background='#f5f6fa')
        style.configure('Card.TFrame', background='#ffffff')
        style.configure('TLabel', background='#ffffff')
        style.configure('Page.TLabel', background='#f5f6fa', foreground='#667085')
        style.configure('Eyebrow.TLabel', background='#f5f6fa', foreground='#7c8296', font=('Segoe UI', 9, 'bold'))
        style.configure('Title.TLabel', background='#f5f6fa', foreground='#20263e', font=('Segoe UI', 26, 'bold'))
        style.configure('Subtitle.TLabel', background='#f5f6fa', foreground='#7a8194', font=('Segoe UI', 11))
        style.configure('Status.TLabel', foreground='#6c56ce', font=('Segoe UI', 10, 'bold'))
        style.configure('Muted.TLabel', foreground='#7b8293', font=('Segoe UI', 10))
        style.configure('Question.TLabel', foreground='#20263e', font=('Segoe UI', 21, 'bold'))
        style.configure('Help.TLabel', foreground='#686184', background='#f6f4fc', font=('Segoe UI', 10))
        style.configure('Feedback.TLabel', foreground='#227850', font=('Segoe UI', 10))
        style.configure('Error.TLabel', foreground='#ac4b40', font=('Segoe UI', 10))
        style.configure('Footer.TLabel', background='#f5f6fa', foreground='#858b9c', font=('Segoe UI', 9))
        style.configure('TButton', padding=(14, 11), background='#eceef5', foreground='#5e6479', borderwidth=0, relief='flat', font=('Segoe UI', 10, 'bold'), focusthickness=2, focuscolor='#a798ec')
        style.map('TButton', background=[('disabled', '#f5f6f9'), ('pressed', '#dadde9'), ('active', '#e2e4ef')], foreground=[('disabled', '#a1a7b6')])
        style.configure('Primary.TButton', background='#7560d8', foreground='#ffffff')
        style.map('Primary.TButton', background=[('disabled', '#edeaf8'), ('pressed', '#5542ae'), ('active', '#6550c5')], foreground=[('disabled', '#a39ac2'), ('!disabled', '#ffffff')])
        style.configure('TCombobox', padding=7, fieldbackground='#ffffff', arrowsize=12, bordercolor='#e2e4ed', lightcolor='#e2e4ed', darkcolor='#e2e4ed')
        style.map('TCombobox', fieldbackground=[('readonly', '#ffffff')], selectbackground=[('readonly', '#ffffff')], selectforeground=[('readonly', '#344054')])
        style.layout('Study.Horizontal.TProgressbar', [('Horizontal.Progressbar.trough', {'sticky': 'nswe', 'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})]})])
        style.configure('Study.Horizontal.TProgressbar', background='#8b78e5', troughcolor='#efedf8', bordercolor='#efedf8', borderwidth=0, lightcolor='#8b78e5', darkcolor='#8b78e5', thickness=5)

    def resize_content(self, event):
        width = max(260, event.width)
        for label in (self.question, self.reason, self.feedback):
            label.configure(wraplength=width)
        self.help.configure(wraplength=width - 28)

    def adapt(self):
        label, reason = self.session.decision()
        self.status.config(text=f'{label} layout • Question {self.index + 1} of {len(QUESTIONS)}')
        self.reason.config(text=reason)
        q = QUESTIONS[self.index]
        if label == 'Support':
            text = 'Study guide: ' + q[3] + '\nTake your time. Choose one answer, then submit.'
        elif label == 'Challenge':
            text = 'Explain your choice to yourself before submitting. Hints remain available.'
        else:
            text = 'Choose one answer. You can request a hint at any time.'
        self.help.config(text=text)

    def load_question(self):
        q = QUESTIONS[self.index]
        self.progress.configure(value=self.index)
        self.answer.set(-1)
        self.used_hint = self.submitted = False
        self.question.config(text=q[0])
        for button, text in zip(self.options, q[1]):
            button.config(text=text, state='normal', result=None)
        self.feedback.config(text='', style='Feedback.TLabel')
        self.submit_button.config(state='normal')
        self.hint_button.config(state='normal')
        self.next_button.config(state='disabled')
        self.adapt()

    def change_mode(self, _event=None):
        self.session.override = self.mode.get()
        self.adapt()

    def hint(self):
        self.used_hint = True
        self.help.config(text='Hint: ' + QUESTIONS[self.index][3])

    def submit(self):
        if self.submitted:
            return
        if self.answer.get() == -1:
            self.feedback.config(text='Select an answer before submitting.', style='Error.TLabel')
            return
        self.submitted = True
        correct = self.answer.get() == QUESTIONS[self.index][2]
        self.session.record(correct, self.used_hint)
        self.progress.configure(value=self.index + 1)
        self.feedback.configure(style='Feedback.TLabel' if correct else 'Error.TLabel')
        self.feedback.config(text=('Correct. ' if correct else 'Review: ') + QUESTIONS[self.index][4])
        for i, button in enumerate(self.options):
            result = 'correct' if i == QUESTIONS[self.index][2] else ('incorrect' if i == self.answer.get() else None)
            button.config(state='disabled', result=result)
        self.submit_button.config(state='disabled')
        self.hint_button.config(state='disabled')
        self.next_button.config(state='normal')
        # Apply adaptation at the next question boundary to avoid moving focus mid-task.
        if self.index == len(QUESTIONS)-1:
            self.next_button.config(text='Finish')

    def next_question(self):
        if not self.submitted:
            return
        if self.index == len(QUESTIONS)-1:
            label, reason = self.session.decision()
            self.status.config(text='Session complete • Final recommendation: ' + label)
            self.reason.config(text=reason)
            self.next_button.config(state='disabled')
            return
        self.index += 1
        self.load_question()

    def reset(self):
        self.session = Session()
        self.mode.set('Auto')
        self.index = 0
        self.next_button.config(text='Next question')
        self.load_question()

if __name__ == '__main__':
    root = tk.Tk()
    StudyApp(root)
    root.mainloop()
