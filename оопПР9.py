import math
import tkinter as tk
from tkinter import messagebox
FUNC_TEXT = "y = sin(x) + 1"


def f(x):
    return math.sin(x) + 1


def df(x):
    return math.cos(x)

MAX_POINTS = 100000


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Табулювання функції")
        self.geometry("720x780")

        self.array = []
        self.array_dy = []

        self._build_form()
        self._build_main_menu()
        self._build_popup_menus()

    def _build_form(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        self.var_a = tk.StringVar(value="0")
        self.var_b = tk.StringVar(value="6,28")
        self.var_h = tk.StringVar(value="0,5")

        for row, (text, var) in enumerate([("Ліва межа", self.var_a),
                                           ("Права межа", self.var_b),
                                           ("Крок", self.var_h)]):
            tk.Label(top, text=text, font=("Arial", 12)).grid(
                row=row, column=0, sticky="w", pady=2)
            tk.Entry(top, textvariable=var, width=14, font=("Arial", 12)).grid(
                row=row, column=1, padx=8, pady=2)

        tk.Label(self, text=FUNC_TEXT, font=("Arial", 16, "bold"),
                 fg="navy").pack(pady=4)

        self.group = tk.LabelFrame(self, text="Виведення", font=("Arial", 12),
                                   padx=10, pady=6)
        self.group.pack(fill="x", padx=10, pady=6)

        self.var_screen = tk.BooleanVar(value=True)
        self.var_array = tk.BooleanVar(value=True)
        self.var_file = tk.BooleanVar(value=False)
        self.var_deriv = tk.BooleanVar(value=False)

        self.checks = [
            (self.var_screen, tk.Checkbutton(self.group, text="На екран",
                                             variable=self.var_screen,
                                             font=("Arial", 12))),
            (self.var_array, tk.Checkbutton(self.group, text="У масив",
                                            variable=self.var_array,
                                            font=("Arial", 12))),
            (self.var_file, tk.Checkbutton(self.group, text="У файл",
                                           variable=self.var_file,
                                           font=("Arial", 12))),
        ]
        for _, cb in self.checks:
            cb.pack(side="left", padx=10)

        tk.Checkbutton(self, text="Похідна", variable=self.var_deriv,
                       font=("Arial", 12)).pack(anchor="w", padx=14)

        memo_frame = tk.Frame(self)
        memo_frame.pack(fill="both", expand=True, padx=10, pady=6)
        self.memo = tk.Text(memo_frame, height=14, wrap="none",
                            font=("Courier New", 11))
        sb_y = tk.Scrollbar(memo_frame, orient="vertical",
                            command=self.memo.yview)
        sb_x = tk.Scrollbar(memo_frame, orient="horizontal",
                            command=self.memo.xview)
        self.memo.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")
        self.memo.pack(side="left", fill="both", expand=True)

        self.chart = tk.Canvas(self, width=680, height=240, bg="white",
                               highlightthickness=1, highlightbackground="gray")
        self.chart.pack(padx=10, pady=6)

        tk.Button(self, text="Нарисувати графік", font=("Arial", 11),
                  command=self.draw_chart).pack(pady=(0, 8))

    def _build_main_menu(self):
        mb = tk.Menu(self)
        calc = tk.Menu(mb, tearoff=0)
        calc.add_command(label="Протабулювати", accelerator="F5",
                         command=self.tabulate)
        calc.add_command(label="Нарисувати графік", accelerator="F6",
                         command=self.draw_chart)
        calc.add_separator()
        calc.add_command(label="Очистити поле виведення", accelerator="Ctrl+L",
                         command=self.clear_memo)
        calc.add_separator()
        calc.add_command(label="Вийти", accelerator="Ctrl+Q", command=self.quit_app)
        mb.add_cascade(label="Обчислення", menu=calc)
        self.config(menu=mb)

        self.bind("<F5>", lambda e: self.tabulate())
        self.bind("<F6>", lambda e: self.draw_chart())
        self.bind("<Control-l>", lambda e: self.clear_memo())
        self.bind("<Control-q>", lambda e: self.quit_app())

    def _build_popup_menus(self):
        self.popup1 = tk.Menu(self, tearoff=0)
        self.popup1.add_command(label="Очистити поле виведення",
                                command=self.clear_memo)
        self.popup1.add_command(label="Вийти", command=self.quit_app)

        self.popup2 = tk.Menu(self, tearoff=0)
        self.popup2.add_command(label="Зняти всі прапорці",
                                command=lambda: self.set_all(False))
        self.popup2.add_command(label="Встановити всі прапорці",
                                command=lambda: self.set_all(True))
        self.popup2.add_command(label="Встановити інверсивно",
                                command=self.invert_all)

        for btn in ("<Button-3>", "<Button-2>"):
            self.bind(btn, self._show_popup1)
            self.group.bind(btn, self._show_popup2)
            for _, cb in self.checks:
                cb.bind(btn, self._show_popup2)

    def _show_popup1(self, event):
        try:
            self.popup1.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup1.grab_release()

    def _show_popup2(self, event):
        try:
            self.popup2.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup2.grab_release()
        return "break"  

    def set_all(self, value):
        for var, _ in self.checks:
            var.set(value)

    def invert_all(self):
        for var, _ in self.checks:
            var.set(not var.get())

    def clear_memo(self):
        self.memo.delete("1.0", "end")          

    def quit_app(self):
        self.destroy()

    @staticmethod
    def _num(s):
        return float(s.strip().replace(",", "."))   

    def _read_params(self):
        try:
            a = self._num(self.var_a.get())
            b = self._num(self.var_b.get())
            h = self._num(self.var_h.get())
        except ValueError:
            messagebox.showerror("Помилка", "Межі та крок мають бути числами.")
            return None
        if h <= 0:
            messagebox.showerror("Помилка", "Крок має бути більшим за 0.")
            return None
        if a > b:
            messagebox.showerror("Помилка",
                                 "Ліва межа не може бути більшою за праву.")
            return None
        n = int((b - a) / h + 1e-9) + 1
        if n > MAX_POINTS:
            messagebox.showerror("Помилка",
                                 f"Забагато точок ({n}). Збільшіть крок.")
            return None
        return a, b, h, n

    def tabulate(self):
        params = self._read_params()
        if params is None:
            return
        a, b, h, n = params
        with_deriv = self.var_deriv.get()

        xs, ys, dys = [], [], []
        for i in range(n):                
            x = a + i * h                  
            xs.append(x)
            ys.append(f(x))
            if with_deriv:
                dys.append(df(x))

        y_max, y_min = ys[0], ys[0]
        x_max, x_min = xs[0], xs[0]
        count = 0
        for x, y in zip(xs, ys):
            if y_max < y:
                y_max, x_max = y, x
            if y_min > y:
                y_min, x_min = y, x
            if 0.5 < y < 1:
                count += 1

        lines = []
        dname = "y'"
        head = f"{'x':>10} {'y':>12}" + (f" {dname:>12}" if with_deriv else "")
        lines.append(f"Табулювання: {FUNC_TEXT}")
        lines.append(head)
        lines.append("-" * len(head))
        for i in range(n):
            row = f"{xs[i]:10.4f} {ys[i]:12.6f}"
            if with_deriv:
                row += f" {dys[i]:12.6f}"
            lines.append(row)
        lines.append("-" * len(head))
        lines.append(f"Кількість точок: {n}")
        lines.append(f"Кількість значень y, де 0,5 < y < 1: {count}")
        lines.append(f"max y = {y_max:.6f} (при x = {x_max:.4f})")
        lines.append(f"min y = {y_min:.6f} (при x = {x_min:.4f})")

        if self.var_array.get():                    
            self.array = list(ys)
            self.array_dy = list(dys)
            lines.append(f"Результати збережено в масив, елементів: {len(self.array)}")

        if self.var_screen.get():
            for line in lines:
                self.memo.insert("end", line + "\n")  
            self.memo.see("end")

        if self.var_file.get():
            try:
                with open("tabulation_result.txt", "w", encoding="utf-8") as fh:
                    fh.write("\n".join(lines) + "\n")
                self.memo.insert("end", "Збережено у файл tabulation_result.txt\n")
            except OSError as e:
                messagebox.showerror("Помилка", f"Не вдалося записати файл: {e}")

        self.draw_chart(xs, ys, dys if with_deriv else None)  

    def draw_chart(self, xs=None, ys=None, dys=None):
        if xs is None:
            params = self._read_params()
            if params is None:
                return
            a, b, h, n = params
            xs = [a + i * h for i in range(n)]
            ys = [f(x) for x in xs]
            dys = [df(x) for x in xs] if self.var_deriv.get() else None

        c = self.chart
        c.delete("all")
        w, hgt = int(c["width"]), int(c["height"])
        ml, mr, mt, mb = 50, 20, 30, 30

        all_y = list(ys) + (list(dys) if dys else [])
        x0, x1 = xs[0], xs[-1]
        y0, y1 = min(all_y), max(all_y)
        if x1 == x0:
            x1 = x0 + 1
        if y1 == y0:
            y1 = y0 + 1
        pad = (y1 - y0) * 0.1
        y0 -= pad
        y1 += pad

        def px(x):
            return ml + (x - x0) / (x1 - x0) * (w - ml - mr)

        def py(y):
            return hgt - mb - (y - y0) / (y1 - y0) * (hgt - mt - mb)

        c.create_rectangle(ml, mt, w - mr, hgt - mb, outline="gray")
        if y0 <= 0 <= y1:
            c.create_line(ml, py(0), w - mr, py(0), fill="black")
        if x0 <= 0 <= x1:
            c.create_line(px(0), mt, px(0), hgt - mb, fill="black")
        for k in range(5):
            yv = y0 + (y1 - y0) * k / 4
            c.create_text(ml - 5, py(yv), text=f"{yv:.2f}", anchor="e",
                          font=("Arial", 8))
            xv = x0 + (x1 - x0) * k / 4
            c.create_text(px(xv), hgt - mb + 12, text=f"{xv:.2f}",
                          font=("Arial", 8))

        def polyline(vals, color):
            pts = []
            for x, y in zip(xs, vals):
                pts += [px(x), py(y)]
            if len(pts) >= 4:
                c.create_line(*pts, fill=color, width=2)
            elif len(pts) == 2:
                c.create_oval(pts[0] - 2, pts[1] - 2, pts[0] + 2, pts[1] + 2,
                              fill=color, outline=color)

        polyline(ys, "blue")
        if dys:
            polyline(dys, "red")

        c.create_text(w / 2, 12, text=f"Графік функції {FUNC_TEXT}",
                      font=("Arial", 11, "bold"))                     
        foot = "синя — y(x)" + ("; червона — похідна y'(x)" if dys else "")
        c.create_text(w / 2, hgt - 8, text=foot, font=("Arial", 8)) 


if __name__ == "__main__":
    App().mainloop()
