import multiprocessing

from .summarizer import Summarizer

MAX_CONSUMER_COUNT = multiprocessing.cpu_count() * 2

class MultiProcessSummarizer(Summarizer):
    POISON_PILL = None

    def __init__(self, text_processor, sentence_scorer, Task, Consumer, min_freq=0.1, max_freq=0.9):
        super().__init__(text_processor, sentence_scorer, min_freq, max_freq)

        self.Task = Task
        self.Consumer = Consumer
        self.process_manager = __class__.ProcessManager(Consumer)
        self.sentence_scorer = sentence_scorer

    def summarize_by_input_frequency(self, sentence_count, articles, nj_phrases):
        print('Starting multiprocess summarization...')

        for article in articles:
            print(article['title'])

        self.process_manager._add_tasks(articles, nj_phrases, self.Task)
        self.process_manager._load_consumers()
        #self._add_poison_pills()
        self.process_manager.task_queue.join()

        sentences_scores = self._get_sentences_scores(len(articles))
        best_sentences = self.sentence_scorer.get_best_unique_sentences(sentences_scores, sentence_count)

        # Sometimes the consumers continue to live for a time, after everything else is done
        #self._join_consumers()
        #self.consumers.clear()

        print('Finished multiprocess summarization...')

        return best_sentences

    def _get_sentences_scores(self, articles_count):
        sentences_scores = []

        while articles_count > 0:
            page_sentences_scores = self.process_manager.result_queue.get()
            sentences_scores.extend(page_sentences_scores)

            articles_count -= 1

        return sentences_scores

    class ProcessManager:
        _process_manager = None

        def __init__(self, Consumer):
            # The consumers are able to get tasks from the queue simultaneously
            # Respectively several consumers are finishing the same task
            # The queue can't join, because the number of completed tasks the reaches the number of added
            # Although not all of the added are completed.
            self.task_lock = multiprocessing.Lock()
            self.result_lock = multiprocessing.Lock()
            self.task_queue = multiprocessing.JoinableQueue()
            self.result_queue = multiprocessing.Queue()
            self.consumers = []
            self.Consumer = Consumer

        @classmethod
        def get_instance(cls):
            if not cls._process_manager:
                cls._process_manager = cls()

            return cls._process_manager

        def _add_consumers(self):
            while len(self.consumers) < MAX_CONSUMER_COUNT:
                new_process = self.Consumer(
                    self.task_lock,
                    self.result_lock,
                    self.task_queue,
                    self.result_queue)

                self.consumers.append(new_process)

        def _start_consumers(self):
            for consumer in self.consumers:
                consumer.start()

        def _load_consumers(self):
            self._add_consumers()
            self._start_consumers()

        def _add_tasks(self, articles, nj_phrases, Task):
            for article in articles:
                arguments = {
                    'nj_phrases': nj_phrases,
                    'text': article['text'],
                    'title': article['title']
                }

                # print('Adding task for page: ', arguments['title'])
                task = Task(arguments)
                self.task_queue.put(task)
                print('Manager: task added to queue...')

        '''
            def _join_consumers(self):
                for consumer in self.consumers:
                    consumer.join()

            def _add_poison_pills(self):
                for consumer in self.consumers:
                    self.queue_container.task_queue.put(__class__.POISON_PILL)
        '''