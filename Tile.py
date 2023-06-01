class Tile:
    def __init__(self, number, x, y, speed, size):
        self.number = number
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.target = [0, 0]
        self.direction = 0
        self.move = False

    def Update(self):
        if self.move and (self.x != self.target[0] or self.y != self.target[1]):
            if self.direction == 0:
                self.y -= self.speed
                if self.y <= self.target[1]:
                    self.y = self.target[1]
                    self.move = False
            elif self.direction == 1:
                self.x -= self.speed
                if self.x <= self.target[0]:
                    self.x = self.target[0]
                    self.move = False
            elif self.direction == 2:
                self.x += self.speed
                if self.x >= self.target[0]:
                    self.x = self.target[0]
                    self.move = False
            else:
                self.y += self.speed
                if self.y >= self.target[1]:
                    self.y = self.target[1]
                    self.move = False
