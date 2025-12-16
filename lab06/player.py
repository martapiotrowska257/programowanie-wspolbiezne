import sysv_ipc
import os
import sys
import time

KEY_SEM1 = 123
KEY_SEM2 = 124
KEY_SM1 = 125
KEY_SM2 = 126

NULL_CHAR = '\0'

CARDS = ["A", "B", "C"]
TURNS = 3

my_score = 0
opponent_score = 0

def get_choice(player_name):
    while True:
        choice = input(f"[{player_name}] Wybierz literę A, B lub C: ").strip().upper()
        if choice in CARDS:
            return choice
        print("Nieprawidłowy wybór. Wpisz A, B lub C.")

def clean_memory_string(byte_data):
    return byte_data.decode().strip(NULL_CHAR)

try:
    # --- GRACZ 1 (TWORZENIE ZASOBÓW) ---
    # próba utworzenia semafora 1 -> jeśli się uda, jesteś Graczem 1
    sem1 = sysv_ipc.Semaphore(KEY_SEM1, flags=sysv_ipc.IPC_CREX, initial_value=0)
    player_role = 1
    print("[GRACZ 1]: Uruchomiony jako pierwszy. Tworzę pozostałe zasoby.")

    # tworzymy resztę zasobów (Gracz 1 jest właścicielem)
    sem2 = sysv_ipc.Semaphore(KEY_SEM2, flags=sysv_ipc.IPC_CREX, initial_value=0)
    sm1 = sysv_ipc.SharedMemory(KEY_SM1, flags=sysv_ipc.IPC_CREX, size=10)
    sm2 = sysv_ipc.SharedMemory(KEY_SM2, flags=sysv_ipc.IPC_CREX, size=10)
    print("GRACZ 1: Zasoby utworzone. Czekam na Gracza 2...")

    time.sleep(2)

except sysv_ipc.ExistentialError:
    # --- GRACZ 2 (PODŁĄCZANIE SIĘ DO ZASOBÓW) ---
    # jeśli zasoby istnieją, jesteś Graczem 2
    player_role = 2
    print("[GRACZ 2]: Dołączam do gry.")

    try:
        sem1 = sysv_ipc.Semaphore(KEY_SEM1)
        sem2 = sysv_ipc.Semaphore(KEY_SEM2)
        sm1 = sysv_ipc.SharedMemory(KEY_SM1)
        sm2 = sysv_ipc.SharedMemory(KEY_SM2)

    except sysv_ipc.ExistentialError:
        print("Błąd: Nie znaleziono zasobów Gracza 1. Uruchom najpierw Gracza 1.")
        sys.exit(1)

print(f"\n--- ZACZYNAMY GRĘ (Jesteś [Graczem {player_role}]) ---")

try:
    for turn in range(1, TURNS + 1):
        print(f"\n--- TURA {turn}/{TURNS} ---")

        if player_role == 1:
            # Gracz 1 wybiera i zapisuje swój wybór w sm1
            my_choice = get_choice("GRACZ 1")
            sm1.write(my_choice.encode())

            sem1.release()  # zwalniamy semafor -> Gracz 2 może teraz działać
            print("GRACZ 1: Wybór zapisany. Czekam na ruch Gracza 2...")

            # Gracz 1 czeka, aż Gracz 2 zapisze swój wybór w sm2 i odczyta nasz wybór z sm1
            sem2.acquire()

            # odczyt wyboru Gracza 2 z sm2
            opp_choice = clean_memory_string(sm2.read(1))
            print(f"GRACZ 1: Gracz 2 wybrał: {opp_choice}")

        else:  # player_role == 2
            print("GRACZ 2: Czekam na ruch Gracza 1...")
            sem1.acquire()

            # Gracz 2 wybiera i zapisuje (nie znając wyboru gracza 1, bo jeszcze go nie odczytał) w sm2
            my_choice = get_choice("GRACZ 2")
            sm2.write(my_choice.encode())

            # Gracz 2 odczytuje wybór Gracza 1 z sm1
            opp_choice = clean_memory_string(sm1.read(1))
            print(f"GRACZ 2: Gracz 1 wybrał: {opp_choice}")

            # Sygnalizujemy Graczowi 1, że skończyliśmy (zapisaliśmy swoje i odczytaliśmy jego)
            sem2.release()

        # --- LOGIKA PUNKTACJI ---
        if my_choice == opp_choice:
            # wygrywa Gracz 2 (te same litery)
            winner = 2
            if player_role == 2:
                print("WYNIK: Trafiłeś! Wygrywasz tę turę.")
                my_score += 1
            else:
                print("WYNIK: Przeciwnik trafił! Przegrywasz tę turę!")
                opponent_score += 1
        else:
            # wygrywa Gracz 1 (różne litery)
            winner = 1
            if player_role == 1:
                print("WYNIK: Przeciwnik nie trafił! Wygrywasz tę turę.")
                my_score += 1
            else:
                print("WYNIK: Nie trafiłeś! Przegrywasz tę turę!")
                opponent_score += 1

        print(f"STAN GRY -> Ty: {my_score} | Przeciwnik: {opponent_score}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    # --- CZYSZCZENIE ZASOBÓW ---
    if player_role == 1:
        # Gracz 1 jako twórca jest odpowiedzialny za sprzątanie
        # Czekamy chwilę, by upewnić się, że Gracz 2 zdążył wyświetlić wynik ostatniej tury
        time.sleep(1)
        print("\nGRACZ 1: Koniec gry. Usuwam zasoby IPC.")
        try:
            sm1.remove()
            sm2.remove()
            sem1.remove()
            sem2.remove()
        except:
            pass
    else:
        print("Koniec gry.")