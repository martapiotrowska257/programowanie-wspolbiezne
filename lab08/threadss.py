import threading
import random

def sum_chunk(data, start_index, end_index, results, index):    # funkcja sumująca fragment listy
    partial_sum = 0
    for i in range(start_index, end_index):
        partial_sum += data[i]
    results[index] = partial_sum


def threaded_sum(data, num_threads):    # funkcja dzieli listę na fragmenty i uruchamia wątki do ich sumowania

    n = len(data)
    threads = []
    results = [0] * num_threads # tworzymy listę o rozmiarze równym liczbie wątków, wypełnioną zerami

    chunk_size = n // num_threads # rozmiar fragmentu dla każdego wątku

    for i in range(num_threads):
        start_index = i * chunk_size
        if i == num_threads - 1:
            end_index = n
        else:
            end_index = (i + 1) * chunk_size

        t = threading.Thread(target=sum_chunk, args=(data, start_index, end_index, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)


def main():
    large_list = [random.randint(1, 100) for _ in range(1000000)]

    thread_count = 4

    print(f"Sumowanie listy o rozmiarze {len(large_list)} przy użyciu {thread_count} wątków...")

    total_sum = threaded_sum(large_list, thread_count)

    # weryfikacja poprawności za pomocą wbudowanej funkcji sum()
    expected_sum = sum(large_list)

    print(f"Wynik wielowątkowy: {total_sum}")
    print(f"Wynik referencyjny: {expected_sum}")

    if total_sum == expected_sum:
        print("Sumowanie zakończone sukcesem.")
    else:
        print("Błąd w sumowaniu.")


if __name__ == "__main__":
    main()