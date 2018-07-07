# contains all blobs that makes up a player and manipulates them
class BlobFamily():
    def __init__(self, blob):
        self.blobs = [blob] # better use some heap to quickly get the largest blob
        self.main_blob = blob
        self.velocity = (0,0)
        self.shoot = False
        self.divide = False

    def update(self, dt):
        for blob in self.blobs:
            blob.move(self.velocity, dt)

    def set_velocity(self, v):
        self.velocity = v

    def shoot(self):
        self.shoot = True

    def divide(self):
        self.divide = True

    def get_blobs(self):
        return self.blobs

