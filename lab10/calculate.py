import time
import math
from multiprocessing import Pool, cpu_count


# --- Funkcje pomocnicze bazujące na pierwszePlus.py ---

def czy_pierwsza_zwykla(k):
    """Sprawdza czy liczba jest pierwsza (metoda podstawowa dla generowania mlp)."""
    if k < 2: return False
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True


def generuj_mlp(max_n):
    """Generuje listę Małych Liczb Pierwszych do pierwiastka z max_n."""
    limit = int(math.ceil(math.sqrt(max_n)))
    mlp = []
    for i in range(2, limit + 1):
        if czy_pierwsza_zwykla(i):
            mlp.append(i)
    return mlp


def czy_pierwsza_z_mlp(k, mlp):
    """Szybkie sprawdzanie pierwszości przy użyciu listy mlp."""
    if k < 2: return False
    limit = math.isqrt(k)
    for p in mlp:
        if p > limit:
            break
        if k % p == 0:
            return False
    return True


# --- Logika sekwencyjna ---

def znajdz_blizniacze_w_zakresie(start, end, mlp):
    """
    Szuka par bliźniaczych (p, p+2) w zadanym zakresie [start, end).
    Zwraca listę znalezionych par.
    """
    wyniki = []
    # Optymalizacja: start musi być nieparzysty (liczby pierwsze > 2 są nieparzyste)
    if start % 2 == 0:
        start += 1

    # Pętla co 2, sprawdzamy tylko liczby nieparzyste
    for i in range(start, end, 2):
        # Sprawdzamy czy i oraz i+2 są pierwsze
        # Uwaga: musimy przekazać mlp do funkcji sprawdzającej
        if czy_pierwsza_z_mlp(i, mlp) and czy_pierwsza_z_mlp(i + 2, mlp):
            wyniki.append((i, i + 2))
    return wyniki


# --- Wrapper dla multiprocessing ---

def worker_wrapper(args):
    """
    Funkcja pomocnicza, ponieważ Pool.map przyjmuje tylko jeden argument.
    Rozpakowuje argumenty i wywołuje właściwą funkcję.
    """
    start, end, mlp = args
    return znajdz_blizniacze_w_zakresie(start, end, mlp)


# --- Główny program ---

if __name__ == '__main__':
    # Konfiguracja zakresu - ustawiamy duży zakres, aby zobaczyć różnicę
    L = 1_000_000
    R = 3_000_000  # Zwiększony zakres dla lepszego pomiaru

    print(f"Szukanie liczb bliźniaczych w zakresie <{L}, {R}>")
    print(f"Liczba dostępnych rdzeni CPU: {cpu_count()}")
    print("-" * 40)

    # KROK 1: Generowanie Małych Liczb Pierwszych (wspólne dla obu metod)
    # Musimy mieć pewność, że mlp wystarczy do sprawdzenia liczby R+2
    print("Generowanie listy pomocniczej MLP...")
    start_time = time.time()
    mlp = generuj_mlp(R + 2)
    print(f"MLP gotowe. Czas: {time.time() - start_time:.4f}s")
    print("-" * 40)

    # ---------------------------------------------------------
    # METODA 1: SEKWENCYJNA
    # ---------------------------------------------------------
    print("Rozpoczynam przetwarzanie SEKWENCYJNE...")
    t0 = time.time()

    wynik_seq = znajdz_blizniacze_w_zakresie(L, R, mlp)

    czas_seq = time.time() - t0
    print(f"Znaleziono {len(wynik_seq)} par.")
    print(f"Czas sekwencyjny: {czas_seq:.4f} s")
    print("-" * 40)

    # ---------------------------------------------------------
    # METODA 2: RÓWNOLEGŁA (MULTIPROCESSING)
    # ---------------------------------------------------------
    print("Rozpoczynam przetwarzanie RÓWNOLEGŁE...")
    t0 = time.time()

    # Konfiguracja puli procesów
    num_processes = cpu_count()  # Możesz zmienić na sztywno np. 4
    pool = Pool(processes=num_processes)

    # Podział zakresu na podzadania (chunks)
    step = (R - L) // num_processes
    ranges = []

    current = L
    for i in range(num_processes):
        koniec = current + step
        # Ostatni proces bierze resztę zakresu, żeby nic nie zgubić (np. przez zaokrąglenia)
        if i == num_processes - 1:
            koniec = R

        # Tworzymy krotkę argumentów: (start, koniec, mlp)
        ranges.append((current, koniec, mlp))
        current = koniec

    # Uruchomienie obliczeń
    # Pool.map zwróci listę list wyników [[pary_z_proc_1], [pary_z_proc_2], ...]
    results_list = pool.map(worker_wrapper, ranges)

    pool.close()
    pool.join()

    # Spłaszczenie listy wyników (z listy list do jednej listy)
    wynik_par = []
    for sublist in results_list:
        wynik_par.extend(sublist)

    czas_par = time.time() - t0
    print(f"Znaleziono {len(wynik_par)} par.")
    print(f"Czas równoległy ({num_processes} procesy): {czas_par:.4f} s")

    # ---------------------------------------------------------
    # PODSUMOWANIE
    # ---------------------------------------------------------
    print("-" * 40)
    if czas_par < czas_seq:
        przyspieszenie = czas_seq / czas_par
        print(f"SUKCES! Przyspieszenie: {przyspieszenie:.2f}x")
    else:
        print("Brak przyspieszenia (za mały zakres danych lub narzut procesów).")
