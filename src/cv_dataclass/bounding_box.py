"""
The point of this module is to provide a simple class for datasets that can easily be exported to other types.
"""

from dataclasses import dataclass
from shapely.geometry import Polygon


@dataclass
class BoundingBox:  # horizontal
    top_left_x: float
    top_left_y: float
    width: float
    height: float
    category: str = None

    @property
    def area(self):
        return self.width * self.height

    def clean_poly(shapely_poly):
        if not shapely_poly.is_valid:
            print("bad poly corrected")
            buffer_pts = shapely_poly.buffer(0).exterior.coords.xy
            fixed_coords = [[int(buffer_pts[0][i]), int(buffer_pts[1][i])] for i in range(len(buffer_pts[0]))]
            shapely_poly = Polygon(fixed_coords)
        return shapely_poly

    def get_area(coords, category=None):
        """[(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        this makes correction if box not perfect... maybe make "correct" an arugument?
        """
        shapely_poly = BoundingBox.clean_poly(Polygon(coords))

        return shapely_poly.area

    def read_dota_data(coords, category=None):
        """[(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        this makes correction if box not perfect... maybe make "correct" an arugument?
        """
        shapely_poly = Polygon(coords)
        # bad data check and correct
        if not shapely_poly.is_valid:
            buffer_pts = shapely_poly.buffer(0).exterior.coords.xy
            fixed_coords = [[int(buffer_pts[0][i]), int(buffer_pts[1][i])] for i in range(len(buffer_pts[0]))]
            shapely_poly = Polygon(fixed_coords)
        x, y = shapely_poly.exterior.coords.xy
        top_left_x = min(x)
        top_left_y = min(y)
        width = max(x) - top_left_x
        height = max(y) - top_left_y
        return BoundingBox(top_left_x, top_left_y, width, height, category)

    def to_coco(self):  # w h switched in coco vs pascal?
        return self.top_left_x, self.top_left_y, self.width, self.height

    def to_pascal(self):
        return self.top_left_x, self.top_left_y, self.height, self.width

    def to_coords(self):
        """
        Clockwise from top left

        Although it might seem to make more sense to return the x and y coords as tuples,
        the result works better with pycocotools if they are just a long list

        oh wait... maybe they should be list of lists?
        """
        return [
            [
                self.top_left_x,
                self.top_left_y,
                self.top_left_x + self.width,
                self.top_left_y,
                self.top_left_x + self.width,
                self.top_left_y + self.height,
                self.top_left_x,
                self.top_left_y + self.height,
            ]
        ]

    def to_polygon(self):
        return Polygon(self.to_coords())

    def to_int(self):
        pass
