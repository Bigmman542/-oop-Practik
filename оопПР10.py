import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
 
 
class Telement(ABC):
    def __init__(self, left=None, right=None):
        self._left = left
        self._right = right
 
    @abstractmethod
    def rezult(self) -> float:
        pass
 
 
class Number(Telement):
    def __init__(self, f):
        super().__init__(None, None)
        self._f = float(f)
 
    def rezult(self):
        return self._f
 
 
class Plus(Telement):
    def rezult(self):
        return self._left.rezult() + self._right.rezult()
 
 
class Mult(Telement):
    def rezult(self):
        return self._left.rezult() * self._right.rezult()
 
 
def form(s, variables):
    s = s.replace(" ", "").replace(",", ".")
    p = s.find("+")
    if p > 0:
        return Plus(form(s[:p], variables), form(s[p + 1:], variables))
    p = s.find("*")
    if p > 0:
        return Mult(form(s[:p], variables), form(s[p + 1:], variables))
    if s in variables:
        return Number(variables[s])
    return Number(float(s))
 
 
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Обчислення виразу")
        self.resizable(False, False)
 
        self.v3 = tk.StringVar()
        self.v4 = tk.StringVar()
        pad = {"padx": 6, "pady": 4}
 
        ttk.Label(self, text="Вираз для x:").grid(row=0, column=0, sticky="e", **pad)
        self.e1 = ttk.Entry(self, width=30)
        self.e1.grid(row=0, column=1, **pad)
        ttk.Label(self, text="Вираз f(x):").grid(row=1, column=0, sticky="e", **pad)
        self.e2 = ttk.Entry(self, width=30)
        self.e2.grid(row=1, column=1, **pad)
        ttk.Label(self, text="Знаків після крапки:").grid(row=2, column=0, sticky="e", **pad)
        self.cb = ttk.Combobox(self, values=[str(i) for i in range(9)],
                               width=5, state="readonly")
        self.cb.set("2")
        self.cb.grid(row=2, column=1, sticky="w", **pad)
        self.cb.bind("<<ComboboxSelected>>", self.calculate)
        ttk.Label(self, text="x =").grid(row=3, column=0, sticky="e", **pad)
        ttk.Entry(self, textvariable=self.v3, state="readonly", width=30).grid(row=3, column=1, **pad)
        ttk.Label(self, text="f(x) =").grid(row=4, column=0, sticky="e", **pad)
        ttk.Entry(self, textvariable=self.v4, state="readonly", width=30).grid(row=4, column=1, **pad)
        ttk.Button(self, text="Обчислити", command=self.calculate).grid(row=5, column=0, **pad)
        ttk.Button(self, text="Вихід", command=self.destroy).grid(row=5, column=1, sticky="e", **pad)
 
    def calculate(self, event=None):
        dec = int(self.cb.get())
        try:
            x = form(self.e1.get(), {}).rezult()
            self.v3.set(f"{x:.{dec}f}")
            fx = form(self.e2.get(), {"x": x}).rezult()
            self.v4.set(f"{fx:.{dec}f}")
        except ValueError:
            self.v3.set("")
            self.v4.set("Помилка у виразі")
 
 
if __name__ == "__main__":
    App().mainloop()
