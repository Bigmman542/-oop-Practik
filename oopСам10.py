Задача 1. Табулювання елементарної функції

import math
 
FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tg": math.tan,
    "exp": math.exp,
    "ln": math.log,
    "sqrt": math.sqrt,
    "x^2": lambda x: x * x,
    "x^3": lambda x: x ** 3,
    "1/x": lambda x: 1 / x,
    "arctg": math.atan,
}
 
 
class Tabulator:
    def __init__(self, func, a, b, h):
        if a >= b:
            raise ValueError("Потрібно, щоб a < b.")
        if h <= 0:
            raise ValueError("Крок h має бути додатним.")
        self._func = func
        self._a = a
        self._b = b
        self._h = h
 
    @property
    def points(self):
        count = int((self._b - self._a) / self._h + 1e-9)
        xs = [self._a + i * self._h for i in range(count + 1)]
        if abs(xs[-1] - self._b) > 1e-9:
            xs.append(self._b)
        return xs
 
    def value(self, x):
        try:
            return self._func(x)
        except (ValueError, ZeroDivisionError, OverflowError):
            return None
 
    def table(self):
        return [(x, self.value(x)) for x in self.points]
 
 
def main():
    name = input("Функція (" + ", ".join(FUNCS) + "): ").strip()
    a = float(input("a = ").replace(",", "."))
    b = float(input("b = ").replace(",", "."))
    h = float(input("h = ").replace(",", "."))
 
    tab = Tabulator(FUNCS[name], a, b, h)
    print(f"{'x':>12} | {'f(x)':>12}")
    for x, y in tab.table():
        print(f"{x:>12.6f} | " + ("не визначена" if y is None else f"{y:>12.6f}"))
 
 
if __name__ == "__main__":
    main()

Задача 2. Обчислення інтегралу за методом Сімпсона

import math


FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tg": math.tan,
    "exp": math.exp,
    "ln": math.log,
    "sqrt": math.sqrt,
    "x^2": lambda x: x * x,
    "x^3": lambda x: x ** 3,
    "1/x": lambda x: 1 / x,
    "arctg": math.atan,
}




class SimpsonIntegrator:
    def __init__(self, func, a, b, n=100):
        if a >= b:
            raise ValueError("Потрібно, щоб a < b.")
        self._func = func
        self._a = a
        self._b = b
        self.n = n


    @property
    def n(self):
        return self._n


    @n.setter
    def n(self, value):
        if value < 2 or value % 2:
            raise ValueError("n має бути парним числом >= 2.")
        self._n = value


    def integrate(self, n=None):
        n = n or self._n
        h = (self._b - self._a) / n
        total = self._func(self._a) + self._func(self._b)
        for i in range(1, n):
            total += self._func(self._a + i * h) * (4 if i % 2 else 2)
        return total * h / 3


    @property
    def runge_error(self):
        return abs(self.integrate(2 * self._n) - self.integrate()) / 15




def main():
    name = input("Функція (" + ", ".join(FUNCS) + "): ").strip()
    a = float(input("a = ").replace(",", "."))
    b = float(input("b = ").replace(",", "."))
    n = int(input("n (парне) = "))


    try:
        simpson = SimpsonIntegrator(FUNCS[name], a, b, n)
        result = simpson.integrate(2 * n)
        print(f"S(n)  = {simpson.integrate():.10f}")
        print(f"S(2n) = {result:.10f}")
        print(f"Похибка (Рунге) = {simpson.runge_error:.2e}")
    except (ValueError, ZeroDivisionError) as err:
        print("Помилка:", err)




if __name__ == "__main__":
    main()

Задача 3. Меню з обробниками команд (tkinter) 

import math
import tkinter as tk
from tkinter import ttk, messagebox


FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tg": math.tan,
    "exp": math.exp,
    "ln": math.log,
    "sqrt": math.sqrt,
    "x^2": lambda x: x * x,
    "x^3": lambda x: x ** 3,
    "1/x": lambda x: 1 / x,
    "arctg": math.atan,
}




class Tabulator:
    def __init__(self, func, a, b, h):
        if a >= b:
            raise ValueError("Потрібно, щоб a < b.")
        if h <= 0:
            raise ValueError("Крок h має бути додатним.")
        self._func = func
        self._a = a
        self._b = b
        self._h = h


    @property
    def points(self):
        count = int((self._b - self._a) / self._h + 1e-9)
        xs = [self._a + i * self._h for i in range(count + 1)]
        if abs(xs[-1] - self._b) > 1e-9:
            xs.append(self._b)
        return xs


    def value(self, x):
        try:
            return self._func(x)
        except (ValueError, ZeroDivisionError, OverflowError):
            return None


    def table(self):
        return [(x, self.value(x)) for x in self.points]




class SimpsonIntegrator:
    def __init__(self, func, a, b, n=100):
        if a >= b:
            raise ValueError("Потрібно, щоб a < b.")
        self._func = func
        self._a = a
        self._b = b
        self.n = n


    @property
    def n(self):
        return self._n


    @n.setter
    def n(self, value):
        if value < 2 or value % 2:
            raise ValueError("n має бути парним числом >= 2.")
        self._n = value


    def integrate(self, n=None):
        n = n or self._n
        h = (self._b - self._a) / n
        total = self._func(self._a) + self._func(self._b)
        for i in range(1, n):
            total += self._func(self._a + i * h) * (4 if i % 2 else 2)
        return total * h / 3


    @property
    def runge_error(self):
        return abs(self.integrate(2 * self._n) - self.integrate()) / 15




class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Табулювання та інтеграл (метод Сімпсона)")
        self.geometry("640x520")


        menu = tk.Menu(self)
        menu.add_command(label="Табулювання", command=self.on_tabulate)
        menu.add_command(label="Інтеграл (Сімпсон)", command=self.on_integrate)
        menu.add_command(label="Вихід", command=self.destroy)
        self.config(menu=menu)


        frm = ttk.Frame(self, padding=8)
        frm.pack(fill=tk.X)
        self.func = ttk.Combobox(frm, values=list(FUNCS), state="readonly", width=8)
        self.func.current(0)
        self.func.grid(row=1, column=0, padx=3)
        self.vars = {}
        for col, (key, text, init) in enumerate(
                [("a", "a", "0"), ("b", "b", "3,14159"),
                 ("h", "крок h", "0,5"), ("n", "n (парне)", "100")], start=1):
            ttk.Label(frm, text=text).grid(row=0, column=col, sticky="w")
            self.vars[key] = tk.StringVar(value=init)
            ttk.Entry(frm, textvariable=self.vars[key], width=10).grid(row=1, column=col, padx=3)
        ttk.Label(frm, text="Функція").grid(row=0, column=0, sticky="w")


        self.out = tk.Text(self, font=("Consolas", 10))
        self.out.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


    def _num(self, key):
        return float(self.vars[key].get().strip().replace(",", "."))


    def _show(self, text):
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, text)


    def on_tabulate(self):
        try:
            tab = Tabulator(FUNCS[self.func.get()], self._num("a"), self._num("b"), self._num("h"))
        except ValueError as err:
            messagebox.showwarning("Помилка", str(err))
            return
        lines = [f"{'x':>12} | {'f(x)':>12}"]
        for x, y in tab.table():
            lines.append(f"{x:>12.6f} | " + ("не визначена" if y is None else f"{y:>12.6f}"))
        self._show("\n".join(lines))


    def on_integrate(self):
        try:
            simpson = SimpsonIntegrator(FUNCS[self.func.get()], self._num("a"),
                                        self._num("b"), int(self.vars["n"].get()))
            result = simpson.integrate(2 * simpson.n)
            self._show(f"S(n)  = {simpson.integrate():.10f}\n"
                       f"S(2n) = {result:.10f}\n"
                       f"Похибка (Рунге) = {simpson.runge_error:.2e}")
        except (ValueError, ZeroDivisionError) as err:
            messagebox.showwarning("Помилка", str(err))




if __name__ == "__main__":
    App().mainloop()
