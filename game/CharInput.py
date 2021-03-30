class CharInput():
    def __init__(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]

    def update(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]