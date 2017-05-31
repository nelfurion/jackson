from abc import ABCMeta, abstractmethod

class HttpService(metaclass=ABCMeta):
    @abstractmethod
    def get(self, endpoint, arguments):
        pass

    @abstractmethod
    def post(self, endpoint, arguments, body):
        pass