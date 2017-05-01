"""Point inside polygon

This module demonstrates a function `point_in_polygon`
using `shapely` library.
More info: http://toblerity.org/shapely/manual.html#object.contains

It is possible to use `Matplotlib`s path module but it does
not support checking poin on boundary.
In any case it worth nothing to code it if needed.
More info: http://matplotlib.org/api/path_api.html#matplotlib.path.Path.contains_point
"""

from collections import namedtuple

import shapely.geometry
import shapely.geometry.polygon


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
    point = shapely.geometry.Point(*point)
    poly = shapely.geometry.polygon.Polygon(poly)
    inside = poly.contains(point)
    if check_on_boundary:
        inside = poly.touches(point) or inside
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
