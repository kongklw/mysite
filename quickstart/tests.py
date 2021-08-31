from django.test import TestCase


# Create your tests here.
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "{0}".format(self.x + self.y)
        # return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return x + y


if __name__ == '__main__':
    p1 = Point(1, 2)
    p2 = Point(2, 3)
    p3 = Point(3, 4)
    # print(p1, p2, p3)
    # print(p1 + p2 + p3)
