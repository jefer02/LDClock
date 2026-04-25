from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, List, Optional, TypeVar


T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """Node for a circular doubly linked list."""

    data: T
    next: Optional["Node[T]"] = None
    previous: Optional["Node[T]"] = None


class CircularDoublyLinkedList(Generic[T]):
    """Manual implementation of a circular doubly linked list."""

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.size: int = 0

    def is_empty(self) -> bool:
        return self.head is None

    def insert_end(self, data: T) -> Node[T]:
        new_node = Node(data=data)

        if self.head is None:
            new_node.next = new_node
            new_node.previous = new_node
            self.head = new_node
            self.size = 1
            return new_node

        tail = self.head.previous
        assert tail is not None

        new_node.next = self.head
        new_node.previous = tail
        tail.next = new_node
        self.head.previous = new_node
        self.size += 1
        return new_node

    def delete_by(self, predicate: Callable[[T], bool]) -> bool:
        if self.head is None:
            return False

        current = self.head
        while True:
            if predicate(current.data):
                if self.size == 1:
                    self.head = None
                    self.size = 0
                    return True

                previous_node = current.previous
                next_node = current.next
                assert previous_node is not None
                assert next_node is not None

                previous_node.next = next_node
                next_node.previous = previous_node

                if current is self.head:
                    self.head = next_node

                self.size -= 1
                return True

            current = current.next
            assert current is not None
            if current is self.head:
                break

        return False

    def find_first(self, predicate: Callable[[T], bool]) -> Optional[T]:
        if self.head is None:
            return None

        current = self.head
        while True:
            if predicate(current.data):
                return current.data

            current = current.next
            assert current is not None
            if current is self.head:
                break

        return None

    def traverse_forward(self) -> List[T]:
        items: List[T] = []
        if self.head is None:
            return items

        current = self.head
        while True:
            items.append(current.data)
            current = current.next
            assert current is not None
            if current is self.head:
                break

        return items

    def traverse_backward(self) -> List[T]:
        items: List[T] = []
        if self.head is None:
            return items

        current = self.head.previous
        assert current is not None
        start = current

        while True:
            items.append(current.data)
            current = current.previous
            assert current is not None
            if current is start:
                break

        return items
