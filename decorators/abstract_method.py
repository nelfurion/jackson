def abstract_method(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('Call to abstract method ', repr(method))

    default_abstract_method.__name__ = method.__name__
    return default_abstract_method
