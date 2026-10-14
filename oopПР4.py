def find_min_length(arr):
    return min(len(s) for s in arr)


def print_shortest(arr):
    min_len = find_min_length(arr)
    for i, s in enumerate(arr, start=1):
        if len(s) == min_len:
            print(f"Елемент: «{s}», номер: {i}, довжина: {len(s)}")


def main():
    A = ["яблуко", "кіт", "сонце", "дім", "ліс",
         "місто", "річка", "он", "море", "гора"]

    print("Масив A:", A)
    print_shortest(A)


main()