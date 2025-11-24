import sysv_ipc
import time
import dictionary

KEY_IN = 11     # kolejka zapytań: Klient -> Serwer
KEY_OUT = 12    # kolejka odpowiedzi: Serwer -> Klient

try:
    mq_in = sysv_ipc.MessageQueue(KEY_IN, flags=sysv_ipc.IPC_CREAT)
    mq_out = sysv_ipc.MessageQueue(KEY_OUT, flags=sysv_ipc.IPC_CREAT)
    print("SERWER: Uruchomiony")

except sysv_ipc.ExistentialError:
    print("SERWER: Błąd przy tworzeniu kolejek")
    exit(1)

try:
    while True:
        message, client_pid = mq_in.receive(True, type=0)  # type=0 powoduje odebranie pierwszej dostępnej wiadomości
        word = message.decode()

        if word == "stop":
            print(f"\nSERWER: Odebrano komendę 'stop' od stoppera PID: {client_pid}.")
            break  # wyjście z pętli while -> przejście do finally

        print(f"SERWER: Odebrano '{word}' od klienta PID: {client_pid}")
        translation = dictionary.DICTIONARY.get(word.lower(), "Nie znam takiego słowa")
        time.sleep(2)

        mq_out.send(translation.encode(), True, type=client_pid)
        print(f"SERWER: Wysłano tłumaczenie do klienta PID: {client_pid}\n")


except sysv_ipc.ExistentialError:
    print("BŁĄD: Problem z dostępem do kolejki.")

finally:
    print("SERWER: Usuwam kolejki.")
    mq_in.remove()
    mq_out.remove()
    print("SERWER: Kolejki usunięte. Zamykam.")
