import os
import sys

dane_path = "./dane.txt"
wyniki_path = "./wyniki.txt"

def calculate(x):
    return x ** 2 + 2 * x + 3

while True:
    if os.path.exists(dane_path) and os.path.getsize(dane_path) > 0:
        try:
            with open(dane_path, "r") as dane:
                n = int(dane.read().strip())
            wynik = calculate(int(n))
            with open(wyniki_path, "w") as wyniki:
                    wyniki.write(str(wynik))
            with open(dane_path, "w") as f:
                pass    # nic nie zapisujemy, plik zostaje wyczyszczony

        except ValueError:
            print(f"Błąd: dane w pliku nie są liczbą całkowitą.")
        except Exception as e:
            print(f"Błąd: {e}")

