import sysv_ipc
import os
import time
import dictionary
import random

KEY_IN = 11     # kolejka zapytań: Klient -> Serwer
KEY_OUT = 12    # kolejka odpowiedzi: Serwer -> Klient

try:
    mq_in = sysv_ipc.MessageQueue(KEY_IN, flags=0)
    mq_out = sysv_ipc.MessageQueue(KEY_OUT, flags=0)

    polish_words = list(dictionary.DICTIONARY.keys())
    message = random.choice(polish_words)

    for i in range(20):
        mq_in.send(message.encode(), True, type=os.getpid())
        print(f"KLIENT ({os.getpid()}): Wysłano wiadomość do serwera:", message)
        time.sleep(1)

        response, _ = mq_out.receive(True, type=os.getpid())
        translation = response.decode()
        print(f"KLIENT: Otrzymano tłumaczenie od serwera: '{translation}'")

except sysv_ipc.ExistentialError:
    print("Błąd: Kolejka nie istnieje.")
