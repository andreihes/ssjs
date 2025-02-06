''' Super Simple Type Cast '''


import abc


class Cast(abc.ABC):
    @abc.abstractmethod
    def sign(self) -> type: pass

    @abc.abstractmethod
    def cast(self, obj: object) -> object: pass
