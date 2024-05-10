class SingletonMetaclass(type):

    _instances = {}

    def __call__(cls, *args: tuple, **kwargs: dict):
        instances = cls._instances

        if cls not in instances:
            instances[cls] = super(SingletonMetaclass, cls).__call__(*args, **kwargs)

        return instances[cls]


class Singleton(metaclass=SingletonMetaclass):
    pass
