import random

def get_random_color():
    rgb_color = []
    for i in range(3):
        rgb_color.append(hex(random.randint(0, 155))[2:])
    return '#' + ''.join(rgb_color)

