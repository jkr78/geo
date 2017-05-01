"""Point inside polygon

This module demonstrates a function `point_in_polygon`
writen in pure python (checked with version 3).

Algorithm used: Ray casting
More info:
  - https://en.wikipedia.org/wiki/Point_in_polygon
  - http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html

"""

from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'])


POLYGONS = {
    'crazy': [
        Point(1, 5),
        Point(1, 3),
        Point(2, 1),
        Point(4, -4),
        Point(-4, -4),
        Point(-6, -2),
        Point(-4, 3),
    ],
    'square': [
        Point(0, 0),
        Point(10, 0),
        Point(10, 10),
        Point(0, 10),
    ],
    'bad': [
        Point(0, 0),
        Point(10, 10),
    ],
}


def print_poly(title, poly):
    print('{title} = [{p}]'.format(title=title, p=', '.join(
        ('({x}, {y})'.format(x=x, y=y) for x, y in poly)
    )))


def point_inside_poly(point, poly, check_on_boundary=True):
    n = len(poly)
    if n < 3:
        # Bad polygon, bad
        return False

    inside = False
    p1 = poly[0]
    for i in range(1, n + 1):
        if check_on_boundary:
            # check vertex
            if (point.x, point.y) == p1:
                return True

            # check if point is on a boundary
            p2 = poly[i % n]
            if p1.y == p2.x and p1.y == point.y and \
               point.x > min(p1.x, p2.x) and point.x < max(p1.x, p2.x):
                return True

        # cast the ray
        if point.y > min(p1.y, p2.y):
            if point.y <= max(p1.y, p2.y):
                if point.x <= max(p1.x, p2.x):
                    if p1.y != p2.y:
                        xints = (point.y - p1.y) * \
                            (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                    if p1.x == p2.x or point.x <= xints:
                        inside = not inside
        p1 = p2
    return inside


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Find if point (x, y) is inside the area')

    parser.add_argument('x', type=float, help='')
    parser.add_argument('y', type=float)
    boundry_group = parser.add_mutually_exclusive_group()
    boundry_group.add_argument(
        '-b',
        '--boundary',
        action='store_true',
        dest='check_on_boundary',
        default=True,
        help='check on boundary (default: check)')
    boundry_group.add_argument(
        '-n',
        '--noboundary',
        dest='check_on_boundary',
        action='store_false',
        help='do not check on boundary')
    parser.add_argument(
        '-t',
        '--type',
        dest='poly',
        default='square',
        choices=[
            'crazy',
            'square',
            'bad'],
        help='polygon type (default: square)')
    parser.add_argument(
        '-p',
        '--print',
        action='store_true',
        dest='print_poly',
        default=False,
        help='print area as list')

    args = parser.parse_args()
    if args.print_poly:
        print_poly(args.poly, POLYGONS[args.poly])
    r = point_inside_poly(Point(args.x, args.y), POLYGONS[args.poly])
    if r:
        print('({x}, {y}) is inside the defined area ({poly})'.format(
              x=args.x, y=args.y, poly=args.poly))
    else:
        print('({x}, {y}) is outside the defined area ({poly})'.format(
              x=args.x, y=args.y, poly=args.poly))
