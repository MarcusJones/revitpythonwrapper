""" Misc Geometry Wrappers (Not Part Of Revit API) """

from rpw.db import XYZ
from rpw.base import BaseObject
from rpw.utils.coerce import to_elements, to_element_ids


class PointCollection(BaseObject):
    """
    Provides helpful methods for managing a collection(list) of :any:`Point` instances.

    >>> points = [p1,p2,p3,p4, ...]
    >>> point_collection = PointCollection(points)

    Attributes:
        point_collection.average
        point_collection.min
        point_collection.max
    """
    def __init__(self, points):
        self.points = points if points is not None else []

    def __iter__(self):
        for point in self.points:
            yield point

    @property
    def average(self):
        """ Returns PointElement representing average of point collection.

        >>> points = [XYZ(0,0,0), XYZ(4,4,2)]
        >>> points.average
        (2,2,1)

        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_avg = sum(x_values) / len(x_values)
        y_avg = sum(y_values) / len(y_values)
        z_avg = sum(z_values) / len(z_values)

        return XYZ(x_avg, y_avg, z_avg)

    @property
    def max(self):
        """ Returns PointElement representing MAXIMUM of point collection.

        >>> points = [(0,0,5), (2,2,2)]
        >>> points.max
        (2,2,5)

        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_max = max(x_values)
        y_max = max(y_values)
        z_max = max(z_values)
        return XYZ(x_max, y_max, z_max)

    @property
    def min(self):
        """ Returns PointElement representing MINIMUM of point collection.
        PointElement objects must support X,Y,Z attributes.
        Example:
        points = [(0,0,5), (2,2,2)]
        points.min = (0,0,2)
        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_min = min(x_values)
        y_min = min(y_values)
        z_min = min(z_values)
        return XYZ(x_min, y_min, z_min)

    def sorted_by(self, x_y_z):
        sorted_points = self.points[:]
        sorted_points.sort(key=lambda p: getattr(p, x_y_z))
        return sorted_points

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return super(PointCollection, self).__repr__(data=len(self))


class ElementCollection(BaseObject):

    def __init__(self, elements_or_ids=None):
        self._elements = []
        if elements_or_ids:
            self.add(elements_or_ids)

    def add(self, elements_or_ids=None):
        if not isinstance(elements_or_ids, (list, set)):
            elements_or_ids = [elements_or_ids]
        print('>>>')
        print(elements_or_ids)
        elements = to_elements(elements_or_ids)
        self._elements.extend(elements)

    @property
    def wrapped_elements(self):
        return [Element(x) for x in self._elements]

    @property
    def elements(self):
        return self._elements

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __contains__(self, mixed_list):
        raise NotImplemented

    def __bool__(self):
        return bool(self._elements)

    def __repr__(self, data=None):
        return super(ElementCollection, self).__repr__(data=len(self))

    @property
    def first(self):
        return self[0]

    @property
    def last(self):
        return self[-1]

    # def set(self, mixed_list):
        # raise NotImplemented
        # self._element_ids = to_element_ids(mixed_list)

    def clear(self):
        self._elements = []