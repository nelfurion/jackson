import multiprocessing

from .summarizer import Summarizer

CONSUMERS_LOCK = multiprocessing.Lock()

CONSUMERS = []
CONSUMERS_COUNT = multiprocessing.cpu_count()

RESULT_QUEUES = {}

class MultiProcessSummarizer(Summarizer):
    POISON_PILL = None

    def __init__(self, text_processor, sentence_scorer, Task, Consumer, min_freq=0.1, max_freq=0.9):
        super().__init__(text_processor, sentence_scorer, min_freq, max_freq)

        self.consumers = []
        self.max_consumer_count = multiprocessing.cpu_count()
        self.Task = Task
        self.Consumer = Consumer
        self.queue_container = __class__.QueueContainer()
        self.sentence_scorer = sentence_scorer
        self.queue_container.return_lock.acquire()
        RESULT_QUEUES[self.queue_container.result_queue] = self.queue_container.return_lock

    def summarize_by_input_frequency(self, sentence_count, articles, nj_phrases):
        print('Starting multiprocess summarization for articles:')
        for article in articles:
            print(article['title'])

        self._tasks_count = len(articles)
        self._add_tasks(
            articles,
            nj_phrases,
            self.queue_container.result_lock,
            self.queue_container.result_queue,
            result_callback,
            self.queue_container.return_lock)

        if len(CONSUMERS) < CONSUMERS_COUNT:
            self._load_consumers()

        print('Added consumers')

        # self._add_poison_pills()
        self.queue_container.task_queue.join()

        print('Joined task queue')

        self.queue_container.return_lock.acquire()
        sentences_scores = self._get_sentences_scores(len(articles))
        self.queue_container.return_lock.release()

        best_sentences = self.sentence_scorer.get_best_unique_sentences(sentences_scores, sentence_count)

        # Sometimes the consumers continue to live for a time, after everything else is done
        # self._join_consumers()
        # self.consumers.clear()

        return best_sentences

    def _get_sentences_scores(self, articles_count):
        sentences_scores = []

        while articles_count > 0:
            page_sentences_scores = self.queue_container.result_queue.get()
            sentences_scores.extend(page_sentences_scores)

            articles_count -= 1

        return sentences_scores

    def _add_tasks(self, articles, nj_phrases, result_lock, result_queue, result_callback, return_lock):
        for article in articles:
            arguments = {
                'result_lock': result_lock,
                'result_queue': result_queue,
                'return_lock': return_lock,
                'tasks_count': len(articles),
                'nj_phrases': nj_phrases,
                'text': article['text'],
                'title': article['title']
            }

            task = self.Task(arguments)
            self.queue_container.task_queue.put(task)

            print('Added tasks')

    def _join_consumers(self):
        for consumer in self.consumers:
            consumer.join()

    def _add_consumers(self):
        while len(CONSUMERS) < CONSUMERS_COUNT:
            new_process = self.Consumer(
                self.queue_container.task_lock,
                self.queue_container.task_queue)

            CONSUMERS_LOCK.acquire()
            if len(CONSUMERS) < CONSUMERS_COUNT:
                CONSUMERS.append(new_process)
            else:
                break
            CONSUMERS_LOCK.release()

    def _start_consumers(self):
        for consumer in self.consumers:
            consumer.start()

    def _load_consumers(self):
        self._add_consumers()
        self._start_consumers()

    def _add_poison_pills(self):
        for consumer in self.consumers:
            self.queue_container.task_queue.put(__class__.POISON_PILL)

    class QueueContainer:
        def __init__(self):
            # The consumers are able to get tasks from the queue simultaneously
            # Respectively several consumers are finishing the same task
            # The queue can't join, because the number of completed tasks the reaches the number of added
            # Although not all of the added are completed.
            self.return_lock = multiprocessing.Lock()
            self.task_lock = multiprocessing.Lock()
            self.result_lock = multiprocessing.Lock()
            self.task_queue = multiprocessing.JoinableQueue()
            self.result_queue = multiprocessing.Queue()

def result_callback(result_queue, tasks_count):
    if result_queue.qsize() >= tasks_count:
        RESULT_QUEUES[result_queue].release()