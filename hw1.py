import time
import threading


class ThreadTester(threading.Thread):
    def __init__(self, thread_id, thread_name, wait_time):
        super(ThreadTester, self).__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.wait_time = wait_time

    def run(self):
        self.test(n_iters=5)
        print(f'[{time.strftime("%H:%M:%S", time.gmtime())}] {self.name} has finished execution')

    def test(self, n_iters):
        for _ in range(n_iters):
            time.sleep(self.wait_time)
            print(f'[{time.strftime("%H:%M:%S", time.gmtime())}] Running {self.name}\n')


if __name__ == "__main__":
    thread1 = ThreadTester(1, "First Thread", 1)
    thread2 = ThreadTester(2, "Second Thread", 2)
    thread3 = ThreadTester(3, "Third Thread", 3)

    threads = [thread1, thread2, thread3]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
