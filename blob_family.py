class BlobFamily():
    def __init__(self, blob):
        self.blobs = [blob] # better use some heap
        self.main_blob = blob
        self.velocity = (0,0)
        self.shoot = False
        self.divide = False

    def update(self, dt):
        pass

    def set_velocity(self, v_x, v_y):
        self.velocity = (v_x, v_y)

    def shoot(self):
        self.shoot = True

    def divide(self):
        self.divide = True

    def get_blobs(self):
        return self.blobs

