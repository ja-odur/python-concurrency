from threading import Thread, Lock
import time


class BankAccount:
    def __init__(self, delay=0):
        self.balance = 0
        self.delay = delay

    def deposit(self, amount):
        bal = self.balance
        time.sleep(self.delay)
        self.balance = bal + amount

    def withdraw(self, amount):
        bal = self.balance
        time.sleep(self.delay)
        self.balance = bal - amount


b1 = BankAccount(delay=1)

t1 = Thread(target=b1.deposit, args=(100, ))
t2 = Thread(target=b1.withdraw, args=(50, ))

t1.start()
t2.start()

t1.join()
t2.join()

print('b1 balance', b1.balance)


# using threading.Lock
# other locks include RLock, Semaphore, BoundedSemaphore
# dont use locks for atomic operations such as replacing the value instead of update,
# reading values without modifying, appending to a list
class BankAccountWithLock:
    def __init__(self, delay=0):
        self.balance = 0
        self.delay = delay
        self.lock = Lock()

    def deposit(self, amount):
        with self.lock:
            bal = self.balance
            time.sleep(self.delay)
            self.balance = bal + amount

    def withdraw(self, amount):
        with self.lock:
            bal = self.balance
            time.sleep(self.delay)
            self.balance = bal - amount


b2 = BankAccountWithLock(delay=1)

t1 = Thread(target=b2.deposit, args=(100, ))
t2 = Thread(target=b2.withdraw, args=(50, ))

t1.start()
t2.start()

t1.join()
t2.join()

print('b2 balance', b2.balance)

