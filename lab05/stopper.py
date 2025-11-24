import sysv_ipc
import os

KEY_IN = 11    # kolejka zapytań: Klient -> Serwer

try:
    mq_in = sysv_ipc.MessageQueue(KEY_IN)
    print(f"STOPPER ({os.getpid()}): Wysyłam sygnał zatrzymania...")

    mq_in.send(b"stop", type=os.getpid())

    print("STOPPER: Sygnał wysłany. Serwer powinien się zamknąć.")

except sysv_ipc.ExistentialError:
    print("Błąd: Kolejka nie istnieje. Serwer prawdopodobnie nie działa.")