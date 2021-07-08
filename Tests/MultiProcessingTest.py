from multiprocessing import Process, Lock, Value
import time

def continuous_update(number, lock):
    while True:
        time.sleep(0.01)
        with lock:
            number.value += 1

if __name__ == '__main__':
    num = Value('i', 0)

    lock = Lock()

    procs = []
    for p in range(0, 100):
        procs.append(Process(target=continuous_update, args=(num, lock)))
        procs[p].start()

    while num.value < 10000:
        print(num.value)

    for p in procs:
        p.join()

    print(num.value)