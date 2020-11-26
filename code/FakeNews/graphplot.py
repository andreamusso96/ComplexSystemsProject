import networkx as nx
from matplotlib import pyplot as plt
import csv


class ColorMaps:
    """
    class that has some static methods to compute the rgb value for a value x in [0.0,1.0)
    for different color maps
    use ColorMaps.<map-function>(x), where <map-function> is one of the implemented functions in the class:
    plasma, blackbody
    """
    plasma_map = None  # static
    blackbody_map = None  # static
    coolwarm_map = None
    clamp = lambda x: 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

    @staticmethod
    def plasma(x):
        x = ColorMaps.clamp(x)
        if ColorMaps.plasma_map is None:
            ColorMaps.plasma_map = readCMap("cmaps/plasma_float_0256")
        i = int((len(ColorMaps.plasma_map) - 1) * x)  # TODO interpolate
        return ColorMaps.plasma_map[i]

    @staticmethod
    def blackbody(x):
        x = ColorMaps.clamp(x)
        if ColorMaps.blackbody_map is None:
            ColorMaps.blackbody_map = readCMap("cmaps/blackbody_float_0256")
        i = int((len(ColorMaps.blackbody_map) - 1) * x)  # TODO interpolate
        return ColorMaps.blackbody_map[i]

    @staticmethod
    def coolwarm(x):
        x = ColorMaps.clamp(x)
        if ColorMaps.coolwarm_map is None:
            ColorMaps.coolwarm_map = readCMap("cmaps/coolwarm_float_0256")
        i = int((len(ColorMaps.coolwarm_map) - 1) * x)  # TODO interpolate
        return ColorMaps.coolwarm_map[i]


def readCMap(name):
    """
    function that reads triples of values from a .csv file into a list
    """
    my_map = []
    with open(name + ".csv") as cmap:
        reader = csv.reader(cmap, delimiter=',')
        for row in reader:
            if "#" in row[0]:  # comment
                continue
            my_map.append((float(row[1]), float(row[2]), float(row[3])))
    return my_map
