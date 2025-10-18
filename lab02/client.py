import os
import time
import errno

bufor_path = "./bufor.txt"
lockfile_path = "./lockfile"
end_mark = ";"

def create_lockfile_or_wait(lockfile_path):
    while True:
        try:
            lockfile = os.open(path=lockfile_path, flags=os.O_CREAT | os.O_EXCL | os.O_RDWR)  # os.O_EXCL - wyświetl błąd, jeśli plik już istnieje
            print("Uzyskano dostęp do bufora serwera")
            os.close(lockfile)
            print("Plik zamkowy utworzony")
            break
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            print("Serwer zajęty, proszę czekać...")
            time.sleep(3)

def client():
    client_id = os.getpid()
    client_filename = f"client{client_id}.txt"

    print(f"Klient uruchomiony z ID: {client_id}")

    # tworzymy plik zamkowy lub czekamy, aż będzie dostępny
    create_lockfile_or_wait(lockfile_path)

    print("Wpisz wiadomość do serwera (zakończ pustą linią): ")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    message = "\n".join(lines)

    with open(bufor_path, "w") as bufor:
        bufor.write(client_filename + "\n")
        bufor.write(message + "\n")
        bufor.write(end_mark + "\n")
        
    print("Wiadomość została wysłana do serwera")

    print("Czekam na odpowiedź...")
    while not os.path.exists(client_filename):
        time.sleep(1)

    with open(client_filename, "r") as client_file:
        response = client_file.read().replace(end_mark, "").strip()
        print(f"\nOdpowiedź serwera:\n{response}")
        time.sleep(10)

    # Usuń plik z odpowiedzią
    os.remove(client_filename)


client()


