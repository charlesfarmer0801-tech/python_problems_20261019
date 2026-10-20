import math

def circle_or_square(rad, area):
  circle = 2 * 3.14 * rad
  square = math.sqrt(area) * 4
  return circle > square
