import math


class Math():

    @staticmethod
    def magnitude(obj1, obj2):
        # Try atan2
        return math.atan2((obj2.rect.centery - obj1.rect.centery), (obj2.rect.centerx - obj1.rect.centerx)) + math.pi
