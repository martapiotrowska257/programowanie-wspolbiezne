import threading

def is_prime(k):
    """Funkcja oparta na pierwsze.py do sprawdzania, czy liczba jest pierwsza."""
    if k < 2:
        return False
    for i in range(2, k):
        if i * i > k:
            return True
        if k % i == 0:
            return False
    return True


def find_primes_in_chunk(start, end, result_list, lock, barrier):
    """Funkcja wykonywana przez pojedynczy wątek do znajdowania pierwszych liczb w danym zakresie."""
    local_primes = []

    for i in range(start, end + 1):
        if is_prime(i):
            local_primes.append(i)

    # wzajemne wykluczanie przy zapisie do wspólnej listy
    with lock:
        result_list.extend(local_primes)

    # sygnalizacja zakończenia pracy poprzez barierę
    print(f"Thread for range {start}-{end} reached the barrier.")
    barrier.wait()


def main():
    lower_bound = 2
    upper_bound = 100
    thread_count = 4

    final_primes = []
    lock = threading.Lock()

    # Bariera dla thread_count + 1 (wątki robocze + wątek główny)
    barrier = threading.Barrier(thread_count + 1)

    threads = []

    # Podział zakresu na kawałki dla każdego wątku
    total_range = (upper_bound - lower_bound + 1)
    chunk_size = total_range // thread_count

    for i in range(thread_count):
        start_index = lower_bound + i * chunk_size
        if i == thread_count - 1:   # ostatni wątek bierze resztę zakresu
            end_index = upper_bound
        else:
            end_index = lower_bound + (i + 1) * chunk_size - 1

        t = threading.Thread(
            target=find_primes_in_chunk,
            args=(start_index, end_index, final_primes, lock, barrier)
        )
        threads.append(t)
        t.start()

    # Wątek główny czeka przy barierze, aż wszystkie wątki robocze skończą
    print("Wątek główny czeka na zakończenie obliczeń...")
    barrier.wait()

    # Dołączenie wszystkich wątków
    final_primes.sort()
    print(f"\nPrimes found ({len(final_primes)}):")
    print(final_primes)


if __name__ == "__main__":
    main()