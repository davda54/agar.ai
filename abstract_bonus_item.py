from abstract_item import AbstractItem

# items that affect a blob when consumed
class AbstractBonusItem(AbstractItem):
    def __init__(self, position, size):
        super().__init__(position, size)

    def affect(self, blob):
        raise NotImplementedError('subclasses must override affect()!')