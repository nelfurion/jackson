import multiprocessing

class Consumer(multiprocessing.Process):
    def __init__(self, task_lock, task_queue):
        super().__init__()
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.task_lock = task_lock

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.get_task()

            # Poison pill: If the value is Null - exit.
            # if next_task is None:
            #    self.signal_task_finished()

            #    break

            result = next_task()

            self.signal_task_finished()


    def signal_task_finished(self):
        self.task_lock.acquire()
        self.task_queue.task_done()
        self.task_lock.release()

    def get_task(self):
        self.task_lock.acquire()
        next_task = self.task_queue.get()
        self.task_lock.release()

        return next_task