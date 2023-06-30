import math


def get_avg_direction(directions):
    sin_sum = 0
    cos_sum = 0
    for direction in directions:
        sin_sum += math.sin(math.radians(direction))
        cos_sum += math.cos(math.radians(direction))

    return (math.degrees(math.atan2(sin_sum, cos_sum)) + 360) % 360


if __name__ == '__main__':
    d = get_avg_direction([10, 20, 5])
    print(d)
