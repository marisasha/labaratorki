import tkinter as tk
from tkinter import ttk, font, messagebox
import random
import time
import json
import os


MIN_VAL = 1
MAX_VAL = 100
SCORES_FILE = "game_scores.json"


def center_window(root, w, h):
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

def load_scores():
    """Загружает рекорды из файла"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def add_score(attempts):
    scores = load_scores()
    is_new_score = True
    for score in scores:
        if score == attempts:
            is_new_score == False
            break
    if is_new_score == True:
        scores.append(attempts)
    
    scores.sort()     
    top_scores = scores[:5]
    
    save_scores(top_scores)
    return top_scores

class GuessGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Угадай число ✨")
        self.resizable(False, False)
        center_window(self, 700, 420)  
        
        self.configure(bg="#0f1724")

        self.main_container = tk.Frame(self, bg="#0f1724")
        self.main_container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.main_container, width=700, height=420, 
                               highlightthickness=0, bg="#0f1724")
        self.canvas.pack(fill="both", expand=True)
        
        self._draw_gradient("#0f1724", "#0b6cff")
        
        self.frame = tk.Frame(self.main_container, bg="white", bd=0, 
                             highlightthickness=0, relief="flat")
        
        self.frame.place(relx=0.5, rely=0.5, anchor="center", 
                        width=660, height=340)  # Увеличили ширину
        
        self.shadow_frame = tk.Frame(self.main_container, bg="#333333", bd=0)
        self.shadow_frame.place(relx=0.5, rely=0.5, anchor="center", 
                               width=664, height=344)


        self.frame.lift()

        self.secret = random.randint(MIN_VAL, MAX_VAL)
        self.attempts = 0
        self.game_active = True 
        self.running_confetti = False
        self.confetti_pieces = [] 

        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except:
            pass
            
        # Шрифты
        self.custom_font_big = font.Font(family="Helvetica", size=20, weight="bold")
        self.custom_font_med = font.Font(family="Helvetica", size=12)
        self.custom_font_small = font.Font(family="Helvetica", size=10)
        self.custom_font_score = font.Font(family="Helvetica", size=11, weight="bold")

        self._build_ui()

        self.bind("<Return>", lambda e: self.check_guess())
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.update_idletasks()
        self.update_scores_display()

    def on_close(self):
    
        self.running_confetti = False
        self.destroy()

    def _draw_gradient(self, color1, color2):
        w = 700
        h = 420
        limit = 80
        
        for i in range(limit):
            r = i / (limit - 1)
            col = self._blend_hex(color1, color2, r)
            y1 = int(i * h / limit)
            y2 = int((i + 1) * h / limit)
            self.canvas.create_rectangle(0, y1, w, y2, outline=col, 
                                        fill=col, width=0)

    def _blend_hex(self, a, b, t):
        a = a.lstrip("#")
        b = b.lstrip("#")
        ar = int(a[0:2], 16); ag = int(a[2:4], 16); ab = int(a[4:6], 16)
        br = int(b[0:2], 16); bg = int(b[2:4], 16); bb = int(b[4:6], 16)
        rr = int(ar + (br - ar) * t)
        rg = int(ag + (bg - ag) * t)
        rb = int(ab + (bb - ab) * t)
        return f"#{rr:02x}{rg:02x}{rb:02x}"

    def _build_ui(self):
    
        main_columns = tk.Frame(self.frame, bg="white")
        main_columns.pack(fill="both", expand=True, padx=20, pady=10)
        
    
        left_column = tk.Frame(main_columns, bg="white")
        left_column.pack(side="left", fill="both", expand=True)
        
    
        heading = tk.Label(left_column, text="Угадай число", 
                          font=self.custom_font_big, 
                          bg="white", fg="#0b2545")
        heading.pack(pady=(0, 4))

        sub = tk.Label(left_column,
                       text=f"Я загадал число от {MIN_VAL} до {MAX_VAL}. Сколько попыток понадобится тебе?",
                       font=self.custom_font_med, bg="white", fg="#2b3b4a", 
                       wraplength=300, justify="center")
        sub.pack(pady=(0, 12))

        row = tk.Frame(left_column, bg="white")
        row.pack(pady=(6, 6))

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(row, textvariable=self.entry_var, 
                              font=self.custom_font_med, width=12)
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.focus_set()

        self.check_btn = ttk.Button(row, text="Угадать", command=self.check_guess)
        self.check_btn.pack(side="left")


        self.hint_label = tk.Label(left_column, text="Введите число и нажмите «Угадать»", 
                                   font=self.custom_font_small, bg="white", fg="#6b7280")
        self.hint_label.pack(pady=(8, 6))
        info = tk.Frame(left_column, bg="white")
        info.pack(pady=(6, 6))

        self.attempts_label = tk.Label(info, text="Попыток: 0", 
                                       font=self.custom_font_small, 
                                       bg="white", fg="#111827")
        self.attempts_label.pack(side="left", padx=8)

        self.range_label = tk.Label(info, text=f"Диапазон: {MIN_VAL}–{MAX_VAL}", 
                                    font=self.custom_font_small, 
                                    bg="white", fg="#111827")
        self.range_label.pack(side="left", padx=8)

        bottom = tk.Frame(left_column, bg="white")
        bottom.pack(side="bottom", pady=(12, 0))

        self.new_btn = ttk.Button(bottom, text="Новая игра", command=self.reset_game)
        self.new_btn.pack(side="left", padx=8)

        self.giveup_btn = ttk.Button(bottom, text="Сдаться", command=self.give_up)
        self.giveup_btn.pack(side="left", padx=8)

        self.fx_canvas = tk.Canvas(left_column, width=300, height=90, 
                                   bg="white", highlightthickness=0)
        self.fx_canvas.pack(pady=(10,0))
        

        right_column = tk.Frame(main_columns, bg="white", width=200)
        right_column.pack(side="right", fill="both", padx=(20, 0))
        

        rating_title = tk.Label(right_column, text="🏆 ТОП-5 Рекордов", 
                               font=self.custom_font_score, 
                               bg="white", fg="#0b2545")
        rating_title.pack(pady=(0, 10))
        
        self.scores_frame = tk.Frame(right_column, bg="white")
        self.scores_frame.pack(fill="both", expand=True)
        

        self.scores_label = tk.Label(self.scores_frame, 
                                    text="Еще нет рекордов.\nБудьте первым!",
                                    font=self.custom_font_small, 
                                    bg="white", fg="#6b7280",
                                    justify="center")
        self.scores_label.pack(expand=True)

    def update_scores_display(self):
        """Обновление рекордов"""
        scores = load_scores()
        
        for widget in self.scores_frame.winfo_children():
            widget.destroy()
        
        if not scores:
            tk.Label(self.scores_frame, 
                    text="Еще нет рекордов.\nБудьте первым!",
                    font=self.custom_font_small, 
                    bg="white", fg="#6b7280",
                    justify="center").pack(expand=True)
        else:
            # Отображаем рекорды
            for i, score in enumerate(scores, 1):
                color = "#0b2545"
                if i == 1:
                    color = "#FFD700"  
                elif i == 2:
                    color = "#C0C0C0" 
                elif i == 3:
                    color = "#CD7F32" 
                
                score_text = f"{i}. {score} попыток"
                score_label = tk.Label(self.scores_frame, text=score_text,
                                      font=self.custom_font_small, 
                                      bg="white", fg=color)
                score_label.pack(anchor="w", pady=2)

    def check_guess(self):
        if not self.game_active:
            return
            
        s = self.entry_var.get().strip()
        if not s:
            self._set_hint("Введите число.", "orange")
            return
        try:
            g = int(s)
        except ValueError:
            self._set_hint("Нужно целое число!", "red")
            return

        if g < MIN_VAL or g > MAX_VAL:
            self._set_hint(f"Число должно быть в диапазоне {MIN_VAL}–{MAX_VAL}.", "red")
            return

        # Проверка
        self.attempts += 1
        self.attempts_label.config(text=f"Попыток: {self.attempts}")

        if g == self.secret:
            self._set_hint(f"Ура! Вы угадали число {self.secret} за {self.attempts} попыток 🎉", "green")
            self._celebrate()
            # Сохраняем результат
            top_scores = add_score(self.attempts)
            # Обновляем отображение рекордов
            self.update_scores_display()
            # Деактивируем игру
            self.deactivate_game()
            return
        elif g < self.secret:
            self._set_hint("Больше ↑", "blue")
        else:
            self._set_hint("Меньше ↓", "blue")

        # Маленькая подсказка по близости
        diff = abs(self.secret - g)
        if diff <= 1 and g != self.secret:
            self._set_hint("Очень близко! 🔥", "darkorange")
        self.entry_var.set("")
        self.entry.focus_set()

    def deactivate_game(self):
        """Деактивирует игру после победы"""
        self.game_active = False
        self.check_btn.config(state="disabled")
        self.giveup_btn.config(state="disabled")
        self.entry.config(state="disabled")

    def activate_game(self):
        """Активирует игру"""
        self.game_active = True
        self.check_btn.config(state="normal")
        self.giveup_btn.config(state="normal")
        self.entry.config(state="normal")
        self.entry.focus_set()

    def _set_hint(self, text, color="#333"):
        self.hint_label.config(text=text, fg=color)

    def _reveal_secret(self, lost=False):
        if lost:
            messagebox.showinfo("Игра окончена", f"Загаданное число было: {self.secret}")
            self.reset_game()
        else:
            messagebox.showinfo("Подсказка", f"Загаданное число: {self.secret}")

    def give_up(self):
        if not self.game_active:
            return
        answer = messagebox.askyesno("Сдаться?", "Вы уверены, что хотите сдаться и увидеть число?")
        if answer:
            self._reveal_secret()
            self.reset_game()

    def reset_game(self):
        self.secret = random.randint(MIN_VAL, MAX_VAL)
        self.attempts = 0
        self.attempts_label.config(text="Попыток: 0")
        self.entry_var.set("")
        self._set_hint(f"Новая игра! Загадано число от {MIN_VAL} до {MAX_VAL}.", "#333")
        self.fx_canvas.delete("all")
        self.confetti_pieces.clear()
        self.running_confetti = False
        self.activate_game()

    def _celebrate(self):
        if self.running_confetti:
            return
        self.running_confetti = True
        colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]
        
        w = int(self.fx_canvas['width'])
        h = int(self.fx_canvas['height'])
        

        for i in range(30):
            x = random.randint(10, w-10)
            y = random.randint(-40, 0)
            size = random.randint(6, 14)
            col = random.choice(colors)
            oval = self.fx_canvas.create_oval(x, y, x+size, y+size, 
                                             fill=col, outline="")
            self.confetti_pieces.append({
                'id': oval,
                'speed': random.uniform(1.0, 3.0),
                'drift': random.uniform(-1.5, 1.5),
                'size': size
            })

        start_time = time.time()
        
        def anim_step():
            if not self.running_confetti or time.time() - start_time > 6.0:
                self.running_confetti = False
                self.confetti_pieces.clear()
                return
                
            pieces_to_remove = []
            for i, piece in enumerate(self.confetti_pieces):
                try:
                    coords = self.fx_canvas.coords(piece['id'])
                    if not coords:
                        pieces_to_remove.append(i)
                        continue
                        
                    
                    self.fx_canvas.move(piece['id'], piece['drift'], piece['speed'])
                    
                
                    if coords[1] > h:
                        pieces_to_remove.append(i)
                except Exception:
                    pieces_to_remove.append(i)
            
        
            for index in sorted(pieces_to_remove, reverse=True):
                if index < len(self.confetti_pieces):
                    piece = self.confetti_pieces.pop(index)
                    try:
                        self.fx_canvas.delete(piece['id'])
                    except Exception:
                        pass
            
        
            if self.confetti_pieces:
                self.after(35, anim_step)
            else:
                self.running_confetti = False
        
        anim_step()

    
        self.after(700, lambda: messagebox.showinfo(
            "Победа!", 
            f"Поздравляю! Вы угадали число за {self.attempts} попыток.\nВаш результат сохранён!"
        ))

if __name__ == "__main__":
    app = GuessGame()
    app.mainloop()