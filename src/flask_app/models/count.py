from abc import ABC, abstractmethod


class AbstractCountModel(ABC):
    @abstractmethod
    def get_count(self, user_id: str) -> int: ...

    @abstractmethod
    def increment_count(self, user_id: str) -> None: ...

    @abstractmethod
    def decrement_count(self, user_id: str) -> None: ...

    @abstractmethod
    def reset_count(self, user_id: str) -> None: ...

    @abstractmethod
    def add_user(self, user_id: str) -> None: ...

    @abstractmethod
    def remove_user(self, user_id: str) -> None: ...


class CountModelException(Exception):
    pass


class UserCountAlreadyExistException(CountModelException):
    def __init__(self, user_id: str):
        super().__init__(f'user "{user_id}" already exist.')


class UserCountNotFoundException(CountModelException):
    def __init__(self, user_id: str):
        super().__init__(f'user "{user_id}" is not found.')
