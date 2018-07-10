from abstract_blob import AbstractBlob


class BulletBlob(AbstractBlob):
    INIT_WEIGHT = 14

    def __init__(self, model, position, player_id, force):
        super().__init__(model, position, player_id, self.INIT_WEIGHT, force)