from abc import abstractmethod
from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...


Vertex = TypeVar("Vertex", bound=Ordered)
