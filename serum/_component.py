from abc import ABCMeta
import inspect
from .exceptions import InvalidComponent


def _more_than_one_parameter_to_init(dct):
    if '__init__' not in dct:
        return False
    signature = inspect.signature(dct['__init__'])
    return len(signature.parameters) > 1


class _ComponentMeta(ABCMeta):
    def __new__(mcs, name, bases, dct):
        if _more_than_one_parameter_to_init(dct):
            raise InvalidComponent(
                "__init__ method in Components can only take 1 parameter"
            )
        return ABCMeta.__new__(mcs, name, bases, dct)


class Component(metaclass=_ComponentMeta):
    """
    Base class for all injectable types.
    Prevents __init__ method:

    class MyComponent(Component):  # raises: InvalidComponent
        def __init__(self):
            pass

    In addition, Components can be abstract, meaning they
    work with the built abc module:

    class MyAbstractComponent(Component):
        @abstractmethod
        def method(self):
            pass

    MyAbstractComponent()  # raises: TypeError
    """
    pass


__all__ = ['Component']
