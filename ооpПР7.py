import math


class Figure:
    name = "Фігура"

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)

    def __del__(self):
        pass

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = float(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = float(value)

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value):
        self.__z = float(value)

    @property
    def size(self):
        return 0.0

    @property
    def size_name(self):
        return "—"

    def volume(self):
        return 0.0

    def surface_area(self):
        return 0.0

    def show(self):
        print(f"[{self.name}] вершина: ({self.x}; {self.y}; {self.z})")

    def edit(self, x=None, y=None, z=None, size=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        if size is not None:
            self.size = size


class Cube(Figure):
    name = "Куб"

    def __init__(self, x=0.0, y=0.0, z=0.0, edge=1.0):
        super().__init__(x, y, z)
        self.__edge = 0.0
        self.edge = edge

    @property
    def edge(self):
        return self.__edge

    @edge.setter
    def edge(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("довжина ребра має бути додатною")
        self.__edge = value

    size = edge
    size_name = "ребро"

    def volume(self):
        return self.__edge ** 3

    def surface_area(self):
        return 6 * self.__edge ** 2

    def show(self):
        super().show()
        print(f"    ребро = {self.edge}, V = {self.volume():.4f}, S = {self.surface_area():.4f}")


class Tetrahedron(Figure):
    name = "Тетраедр"

    def __init__(self, x=0.0, y=0.0, z=0.0, edge=1.0):
        super().__init__(x, y, z)
        self.__edge = 0.0
        self.edge = edge

    @property
    def edge(self):
        return self.__edge

    @edge.setter
    def edge(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("довжина ребра має бути додатною")
        self.__edge = value

    size = edge
    size_name = "ребро"

    def volume(self):
        return self.__edge ** 3 / (6 * math.sqrt(2))

    def surface_area(self):
        return math.sqrt(3) * self.__edge ** 2

    def show(self):
        super().show()
        print(f"    ребро = {self.edge}, V = {self.volume():.4f}, S = {self.surface_area():.4f}")


class Sphere(Figure):
    name = "Куля"

    def __init__(self, x=0.0, y=0.0, z=0.0, radius=1.0):
        super().__init__(x, y, z)
        self.__radius = 0.0
        self.radius = radius

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("радіус має бути додатним")
        self.__radius = value

    size = radius
    size_name = "радіус"

    def volume(self):
        return 4 / 3 * math.pi * self.__radius ** 3

    def surface_area(self):
        return 4 * math.pi * self.__radius ** 2

    def show(self):
        super().show()
        print(f"    радіус = {self.radius}, V = {self.volume():.4f}, S = {self.surface_area():.4f}")


class FigureList:
    def __init__(self):
        self.__items = []

    def __len__(self):
        return len(self.__items)

    def add(self, figure):
        self.__items.append(figure)

    def show_all(self):
        if not self.__items:
            print("Список порожній.")
            return
        for i, fig in enumerate(self.__items, 1):
            print(f"{i}.", end=" ")
            fig.show()

    def get(self, number):
        if not 1 <= number <= len(self.__items):
            raise IndexError("запису з таким номером не існує")
        return self.__items[number - 1]

    def delete(self, number):
        self.get(number)
        del self.__items[number - 1]

    def search_by_type(self, type_name):
        return [f for f in self.__items if f.name.lower() == type_name.lower()]

    def search_by_size(self, value, eps=1e-9):
        return [f for f in self.__items if abs(f.size - value) < eps]

    def search_by_volume(self, min_v, max_v):
        return [f for f in self.__items if min_v <= f.volume() <= max_v]

    def search_by_vertex(self, x, y, z):
        return [f for f in self.__items if (f.x, f.y, f.z) == (x, y, z)]


def read_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Помилка: введіть число.")


def read_positive(prompt):
    while True:
        value = read_float(prompt)
        if value > 0:
            return value
        print("Помилка: значення має бути додатним.")


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Помилка: введіть ціле число.")


def create_figure():
    print("Тип фігури: 1 - Куб, 2 - Тетраедр, 3 - Куля, 0 - за замовчуванням (Куб без параметрів)")
    kind = read_int("Ваш вибір: ")
    if kind == 0:
        return Cube()
    x = read_float("x = ")
    y = read_float("y = ")
    z = read_float("z = ")
    if kind == 1:
        return Cube(x, y, z, read_positive("Довжина ребра = "))
    if kind == 2:
        return Tetrahedron(x, y, z, read_positive("Довжина ребра = "))
    if kind == 3:
        return Sphere(x, y, z, read_positive("Радіус = "))
    raise ValueError("невідомий тип фігури")


def print_found(found):
    if not found:
        print("Нічого не знайдено.")
    for fig in found:
        fig.show()


def search_menu(storage):
    print("Пошук за: 1 - типом, 2 - розміром (ребро/радіус), 3 - діапазоном об'єму, 4 - координатами вершини")
    choice = read_int("Ваш вибір: ")
    if choice == 1:
        print_found(storage.search_by_type(input("Тип (Куб/Тетраедр/Куля): ").strip()))
    elif choice == 2:
        print_found(storage.search_by_size(read_float("Значення: ")))
    elif choice == 3:
        print_found(storage.search_by_volume(read_float("V від: "), read_float("V до: ")))
    elif choice == 4:
        print_found(storage.search_by_vertex(read_float("x = "), read_float("y = "), read_float("z = ")))
    else:
        print("Невірний пункт меню.")


def edit_menu(storage):
    storage.show_all()
    if len(storage) == 0:
        return
    fig = storage.get(read_int("Номер запису для редагування: "))
    print("Редагувати: 1 - координати вершини, 2 - розмір (ребро/радіус)")
    choice = read_int("Ваш вибір: ")
    if choice == 1:
        fig.edit(x=read_float("Нове x = "), y=read_float("Нове y = "), z=read_float("Нове z = "))
    elif choice == 2:
        fig.edit(size=read_positive(f"Нове значення ({fig.size_name}) = "))
    else:
        print("Невірний пункт меню.")
        return
    print("Запис змінено:")
    fig.show()


def main():
    storage = FigureList()
    storage.add(Cube(0, 0, 0, 2))
    storage.add(Tetrahedron(1, 2, 3, 3))
    storage.add(Sphere(-1, 0, 4, 1.5))

    menu = (
        "\n===== МЕНЮ =====\n"
        "1 - Показати всі фігури\n"
        "2 - Додати фігуру\n"
        "3 - Пошук\n"
        "4 - Редагувати запис\n"
        "5 - Видалити запис\n"
        "0 - Вихід"
    )
    while True:
        print(menu)
        try:
            choice = read_int("Ваш вибір: ")
            if choice == 0:
                print("Роботу завершено.")
                break
            elif choice == 1:
                storage.show_all()
            elif choice == 2:
                storage.add(create_figure())
                print("Фігуру додано.")
            elif choice == 3:
                search_menu(storage)
            elif choice == 4:
                edit_menu(storage)
            elif choice == 5:
                storage.show_all()
                storage.delete(read_int("Номер запису: "))
                print("Запис видалено.")
            else:
                print("Невірний пункт меню.")
        except (ValueError, IndexError) as e:
            print("Помилка:", e)
        except EOFError:
            break


if __name__ == "__main__":
    main()