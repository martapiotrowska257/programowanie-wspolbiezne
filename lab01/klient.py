import os
import time

dane_path = "./dane.txt"
wyniki_path = "./wyniki.txt"

def clientInput():
    try:
        n = int(input("Podaj liczbę całkowitą: "))
        with open(dane_path, "w") as dane:
            dane.write(str(n))
    except ValueError:
        print(f"Podany argument nie jest liczbą całkowitą")
        exit(1)

clientInput()

while True:
    if os.path.exists(wyniki_path) and os.path.getsize(wyniki_path) > 0:
        try:
            with open(wyniki_path, "r") as wyniki:
                wynik = wyniki.read().strip()
            with open(wyniki_path, "w") as f:
                pass    # nic nie zapisujemy, plik zostaje wyczyszczony
            print(f"Odpowiedź serwera: {wynik}")
            break
        except Exception as e:
            print(f"Błąd odczytu pliku {e}")

    time.sleep(1)
