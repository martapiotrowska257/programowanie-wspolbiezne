import os
import time

bufor_path = "bufor.txt"
lockfile_path = "lockfile"
end_mark = ";"

print("Serwer uruchomiony. Oczekiwanie na wiadomości...")

while True:
    if os.path.exists(lockfile_path) and os.path.exists(bufor_path) and os.path.getsize(bufor_path) > 0:
        try:
            with open(bufor_path, "r") as bufor:
                lines = bufor.readlines()

            # pierwsza linia to nazwa pliku klienta
            client_file = lines[0].strip()
            # pozostałe linie to wiadomość (bez znacznika końca)
            message_lines = [line.strip() for line in lines[1:] if line.strip() != end_mark]
            message = "\n".join(message_lines)

            print(f"\n--- Wiadomość od klienta ({client_file}) ---")
            print(message)
            print("--- Koniec wiadomości ---\n")

            print("Wpisz odpowiedź (zakończ pustą linią): ")
            response_lines = []
            while True:
                line = input()
                if line == "":
                    break
                response_lines.append(line)
            response = "\n".join(response_lines)

            with open(client_file, "w") as f:
                f.write(response + "\n")
                f.write(end_mark + "\n")

            print(f"Odpowiedź wysłana do pliku: {client_file}")

            # usuwamy lockfile i czyścimy bufor
            os.remove(lockfile_path)
            with open(bufor_path, "w") as bufor:
                bufor.write("")

        except Exception as e:
            print(f"Błąd: {e}")

    time.sleep(1)
