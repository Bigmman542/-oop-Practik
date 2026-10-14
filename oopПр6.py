class Time:
    SECONDS_IN_DAY = 24 * 3600

    def __init__(self, hours=0, minutes=0, seconds=0):
        if not Time.is_valid(hours, minutes, seconds):
            raise ValueError("Недопустиме значення часу!")
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @staticmethod
    def is_valid(h, m, s):
        return 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60

    def to_seconds(self):
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    @staticmethod
    def from_seconds(total):
        if total < 0 or total >= Time.SECONDS_IN_DAY:
            raise ValueError("Результат виходить за межі доби!")
        return Time(total // 3600, (total % 3600) // 60, total % 60)

    def input_time(self):
        while True:
            try:
                h, m, s = map(int, input(
                    "Введіть години, хвилини, секунди: ").split())
            except ValueError:
                print("Помилка введення! Спробуйте ще раз.")
                continue
            if Time.is_valid(h, m, s):
                self.hours, self.minutes, self.seconds = h, m, s
                return
            print("Час поза допустимими межами (0-23:0-59:0-59)!")

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def print_time(self):
        print(self)

    def time_left(self):
        left = Time.SECONDS_IN_DAY - self.to_seconds()
        print("До завершення доби залишилось: "
              f"{left // 3600:02d}:{(left % 3600) // 60:02d}:{left % 60:02d}")

    def __add__(self, other):
        return Time.from_seconds(self.to_seconds() + other.to_seconds())

    def __sub__(self, other):
        return Time.from_seconds(self.to_seconds() - other.to_seconds())


def main():
    t1 = Time()
    t2 = Time()

    print("Перший час:")
    t1.input_time()
    print("Другий час:")
    t2.input_time()

    print("\nt1 =", t1)
    print("t2 =", t2)

    print("\nt1:", end=" ")
    t1.time_left()
    print("t2:", end=" ")
    t2.time_left()

    try:
        print("\nt1 + t2 =", t1 + t2)
    except ValueError as e:
        print("\nt1 + t2 =", e)

    try:
        print("t1 - t2 =", t1 - t2)
    except ValueError as e:
        print("t1 - t2 =", e)


if __name__ == "__main__":
    main()