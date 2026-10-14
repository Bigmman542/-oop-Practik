from dataclasses import dataclass

FILENAME = "trains.txt"
TARGET = "Львів"


@dataclass
class Train:
    number: str
    destination: str
    departure: str
    travel_time: str


def create_file():
    n = int(input("Введіть кількість потягів: "))
    with open(FILENAME, "w", encoding="utf-8") as f:
        for i in range(n):
            print(f"\nПотяг №{i + 1}")
            number = input("Номер потяга: ")
            destination = input("Станція призначення: ")
            departure = input("Час відправки (гг:хх): ")
            travel_time = input("Час в дорозі (гг:хх): ")
            f.write(f"{number};{destination};{departure};{travel_time}\n")


def read_file():
    trains = []
    with open(FILENAME, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            number, destination, departure, travel_time = line.split(";")
            trains.append(Train(number, destination, departure, travel_time))
    return trains


def print_to_target(trains):
    found = False
    print(f"\nПотяги до станції {TARGET}:")
    print(f"{'Номер':<8}{'Призначення':<15}{'Відправлення':<14}{'В дорозі':<10}")
    print("-" * 47)
    for t in trains:
        if t.destination.lower() == TARGET.lower():
            print(f"{t.number:<8}{t.destination:<15}{t.departure:<14}{t.travel_time:<10}")
            found = True
    if not found:
        print("Потягів до Львова немає.")


create_file()
trains = read_file()
print_to_target(trains)