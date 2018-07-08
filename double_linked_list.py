class DoubleLinkedListItem:
    def __init__(self, value, previous, next = None):
        self.value = value
        self.previous = previous
        self.next = next

    def get(self): return self.value
    def set(self, value): self.value = value
    def get_previous(self): return self.previous
    def get_next(self): return self.next

class DoubleLinkedList:
    def __init__(self, iterable=None):
        self.first = None
        self.last = None

        if iterable is not None:
            for item in iterable: self.append(item)

    def append(self, value):
        if self.first is None:
            self.first = DoubleLinkedListItem(value, None, None)
            self.last = self.first
        else:
            new = DoubleLinkedListItem(value, self.last, None)
            self.last.next = new
            self.last = new

    def get_first_iterator(self):
        return self.first

    def delete(self, iter):
        if iter.next is not None: iter.next.previous = iter.previous
        else: self.last = iter.previous

        if iter.previous is not None: iter.previous.next = iter.next
        else: self.first = iter.next

    def __iter__(self):
        current = self.first
        while current is not None:
            yield current
            current = current.next