Завдання 1

import math


s = float(input("Введіть площу квадрата: "))


if s <= 0:
    print("Площа має бути додатним числом")
else:
    a = math.sqrt(s)
    p = 4 * a
    print(f"Периметр квадрата: {p:.2f}")

Завдання 2 

import math


R = float(input("Введіть зовнішній радіус: "))
r = float(input("Введіть внутрішній радіус: "))


if r <= 0 or R <= r:
    print("Помилка: потрібно, щоб 0 < r < R")
else:
    s = math.pi * (R ** 2 - r ** 2)
    print(f"Площа кільця: {s:.2f}")

Завдання 3 

import math


a = float(input("Введіть перший катет: "))
b = float(input("Введіть другий катет: "))


if a > 0 and b > 0:
    c = math.sqrt(a ** 2 + b ** 2)
    p = a + b + c
    print("Трикутник існує")
    print(f"Гіпотенуза: {c:.2f}")
 print(f"Периметр: {p:.2f}")
else:
    print("Такого трикутника не існує (катети мають бути додатними)")

Завдання 4 

n = int(input("Введіть двоцифрове число: "))


if 10 <= abs(n) <= 99:
    m = abs(n)
    tens = m // 10
    units = m % 10
    print(f"Кількість десятків: {tens}")
    print(f"Кількість одиниць: {units}")
    print(f"Сума цифр: {tens + units}")
    print(f"Добуток цифр: {tens * units}")
else:
    print("Це не двоцифрове число")
