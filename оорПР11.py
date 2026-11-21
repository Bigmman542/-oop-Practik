import math
import re

F = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "ln": math.log, "sqrt": math.sqrt}
R = {
    "sin": lambda u: ("call", "cos", u),
    "cos": lambda u: ("neg", ("call", "sin", u)),
    "tan": lambda u: ("bin", "/", ("num", 1), ("bin", "^", ("call", "cos", u), ("num", 2))),
    "exp": lambda u: ("call", "exp", u),
    "ln": lambda u: ("bin", "/", ("num", 1), u),
    "sqrt": lambda u: ("bin", "/", ("num", 1), ("bin", "*", ("num", 2), ("call", "sqrt", u))),
}
P = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def parse(text):
    t = re.findall(r"\d+\.?\d*|[a-z]+|[-+*/^()]|\S", text.lower().replace(",", ".")) + [None]
    p = [0]

    def eat():
        if t[p[0]] is None:
            raise ValueError("Вираз обірвано")
        p[0] += 1
        return t[p[0] - 1]

    def need(c):
        if eat() != c:
            raise ValueError(f"Очікувався символ {c}")

    def expr():
        n = term()
        while t[p[0]] in ("+", "-"):
            op = eat()
            n = ("bin", op, n, term())
        return n

    def term():
        n = unary()
        while t[p[0]] in ("*", "/"):
            op = eat()
            n = ("bin", op, n, unary())
        return n

    def unary():
        if t[p[0]] == "-":
            eat()
            return ("neg", unary())
        n = atom()
        if t[p[0]] == "^":
            eat()
            return ("bin", "^", n, unary())
        return n

    def atom():
        k = eat()
        if re.fullmatch(r"\d+\.?\d*", k):
            return ("num", float(k))
        if k in F:
            need("(")
            a = expr()
            need(")")
            return ("call", k, a)
        if k == "x":
            return ("var",)
        if k in ("pi", "e"):
            return ("num", math.pi if k == "pi" else math.e)
        if k == "(":
            a = expr()
            need(")")
            return a
        raise ValueError(f"Недопустимий елемент: {k}")

    tree = expr()
    if t[p[0]] is not None:
        raise ValueError("Зайві символи у виразі")
    return tree


def ev(n, x):
    k = n[0]
    if k == "num":
        return n[1]
    if k == "var":
        return x
    if k == "neg":
        return -ev(n[1], x)
    if k == "call":
        return F[n[1]](ev(n[2], x))
    a, b = ev(n[2], x), ev(n[3], x)
    if n[1] == "/" and b == 0:
        raise ZeroDivisionError("Ділення на нуль")
    op = n[1]
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    return a ** b


def num(v):
    return ("num", v)


def isn(n, v=None):
    return n[0] == "num" and (v is None or n[1] == v)


def neg(a):
    return num(-a[1]) if isn(a) else ("neg", a)


def mk(op, a, b):
    if isn(a) and isn(b) and not (op == "/" and b[1] == 0):
        return num(ev(("bin", op, a, b), 0))
    if op == "+" and (isn(a, 0) or isn(b, 0)):
        return b if isn(a, 0) else a
    if op == "-" and isn(b, 0):
        return a
    if op == "-" and isn(a, 0):
        return neg(b)
    if op == "*" and (isn(a, 0) or isn(b, 0)):
        return num(0)
    if op == "*" and (isn(a, 1) or isn(b, 1)):
        return b if isn(a, 1) else a
    if op == "/" and (isn(a, 0) or isn(b, 1)):
        return num(0) if isn(a, 0) else a
    if op == "^" and (isn(b, 0) or isn(b, 1)):
        return num(1) if isn(b, 0) else a
    return ("bin", op, a, b)


def d(n):
    k = n[0]
    if k in ("num", "var"):
        return num(0 if k == "num" else 1)
    if k == "neg":
        return neg(d(n[1]))
    if k == "call":
        return mk("*", R[n[1]](n[2]), d(n[2]))
    op, u, v = n[1], n[2], n[3]
    du, dv = d(u), d(v)
    if op in "+-":
        return mk(op, du, dv)
    if op == "*":
        return mk("+", mk("*", du, v), mk("*", u, dv))
    if op == "/":
        return mk("/", mk("-", mk("*", du, v), mk("*", u, dv)), mk("^", v, num(2)))
    if isn(v):
        return mk("*", mk("*", v, mk("^", u, num(v[1] - 1))), du)
    return mk("*", n, mk("+", mk("*", dv, ("call", "ln", u)), mk("/", mk("*", v, du), u)))


def derivative(n, order=1):
    for _ in range(order):
        n = d(n)
    return n


def to_s(n, p=0):
    k = n[0]
    if k == "num":
        v = n[1]
        t = str(int(v)) if v == int(v) else f"{v:.4g}"
        return f"({t})" if v < 0 and p else t
    if k == "var":
        return "x"
    if k == "neg":
        t = "-" + to_s(n[1], 4)
        return f"({t})" if p else t
    if k == "call":
        return f"{n[1]}({to_s(n[2])})"
    q = P[n[1]]
    sp = " " if n[1] in "+-" else ""
    t = f"{to_s(n[2], q + (n[1] == '^'))}{sp}{n[1]}{sp}{to_s(n[3], q + (n[1] != '^'))}"
    return f"({t})" if q < p else t


def table(f, a, b, h):
    d1, d2 = derivative(f, 1), derivative(f, 2)
    rows = []
    for i in range(int((b - a) / h + 1e-9) + 1):
        x = a + i * h
        rows.append((x, ev(f, x), ev(d1, x), ev(d2, x)))
    return rows


def main():
    while True:
        text = input("f(x) = ").strip()
        if not text:
            break
        try:
            f = parse(text)
            d1, d2 = derivative(f, 1), derivative(f, 2)
            x0 = float(input("x0 = ").replace(",", "."))
            print("f'(x)  =", to_s(d1))
            print("f''(x) =", to_s(d2))
            print(f"f({x0}) = {ev(f, x0):.6f}")
            print(f"f'({x0}) = {ev(d1, x0):.6f}")
            print(f"f''({x0}) = {ev(d2, x0):.6f}")
        except (ValueError, ZeroDivisionError, OverflowError) as err:
            print("Помилка:", err)


if __name__ == "__main__":
    main()
