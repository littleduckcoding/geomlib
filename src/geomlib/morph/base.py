from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from geomlib.point import Point
    from geomlib.vector import Vector

T = TypeVar("T")

class Morph(ABC):

    @abstractmethod
    def apply_point(self, p: "Point") -> "Point":
        pass

    @abstractmethod
    def apply_vector(self, v: "Vector") -> "Vector":
        pass
    
    def apply(self, obj: T) -> T:
        return obj.transform(self)