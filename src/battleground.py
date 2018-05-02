import copy
import display
from convex_hull import get_all_vertices, graham_scan
from polygon import interpolate

DEBUG = False


class Battleground(object):
    def __init__(self, mat):
        self._init_from_view(mat)

    def _init_from_view(self, view):
        self.m = len(view)
        self.n = len(view[0])
        self.max_h = max(entry for row in view for entry in row)  # the maximum height

        # check input dimensions
        self._check_valid(view, "input view")

        # initialize terrain and fog
        self.terrain = copy.deepcopy(view)
        self.fog = [[entry == 1 for entry in row] for row in view]

        # find the mountain coordinates
        h_coordinates = {h: [] for h in range(3, self.max_h + 1)}  # h -> list of coordinates that have height h
        for r in range(self.m):
            for c in range(self.n):
                if self.terrain[r][c] >= 3:
                    h_coordinates[self.terrain[r][c]].append((r, c))

        # fill the mountains
        for h in h_coordinates:  # iterate over different heights
            hull_verts = graham_scan(get_all_vertices(h_coordinates[h]))  # all vertices of the convex hull
            mask = interpolate(self.m, self.n, hull_verts, use_wn=True)
            for r in range(self.m):
                for c in range(self.n):
                    if mask[r][c] and self.terrain[r][c] != 2:
                        self.terrain[r][c] = h

        # remove the remaining fog on the terrain
        for r in range(self.m):
            for c in range(self.n):
                if self.terrain[r][c] == 1:
                    self.terrain[r][c] = 0

    def _init_from_terrain_and_fog(self, terrain, fog):
        # the size of the battleground (m * n matrix)
        self.m = len(terrain)
        self.n = len(terrain[0])
        self.max_h = max(entry for row in terrain for entry in row)  # the maximum height

        self._check_valid(terrain, "input terrain")
        self._check_valid(fog, "input fog")

        self.terrain = terrain
        self.fog = fog

    def _check_valid(self, mat, name="input"):
        """
        check whether the input matrix (mat, fog, terrain, etc) is valid (match the dimensions)
        raise a ValueError if invalid.
        """
        if len(mat) != self.m:
            raise ValueError("Input Matrix Shape Mismatch: the {} matrix has {} rows, but self.m={}".
                             format(name, len(mat), self.m))
        for i, row in enumerate(mat):
            if len(row) != self.n:
                raise ValueError("Input Matrix Shape Mismatch: the {} matrix has {} columns at row {}, but self.n={}"
                                 .format(name, len(row), i, self.n))

    def __str__(self):
        return display.get_display(self.terrain)

    def get_view(self, i1=-1, j1=-1, interfere=False, birdseye=True):
        """
        get a view of the battleground for a robot at (i, j)
        when (i1, j1) == (-1, -1) by default, return a view without the robot
        :param i1: coordinate on axis-0/vertical axis (0-indexed)
        :param j1: coordinate on axis-1/horizontal axis (0-indexed)
        :param interfere: if True, the fog in the 3*3 square around (i, j) on the battleground will be removed
        :param birdseye: if True, everything not covered in fog on the battleground will be revealed;
         otherwise, only the 4 adjacent entries will be revealed, and everything else will be covered in fog.
        :return:
        """

        if birdseye:
            view = copy.deepcopy(self.terrain)  # default view: omniscience
            for i in range(self.m):
                for j in range(self.n):
                    if self.fog[i][j]:  # there is fog in the area
                        view[i][j] = 1
        else:  # birdseye disabled
            view = [[1] * self.n for _ in range(self.m)]  # default view: ignorance

        if i1 >= 0 and j1 >= 0:  # not default -> add information
            # get a list of coordinates for valid surrounding blocks
            neighbors = [(i, j) for j in range(max(j1 - 1, 0), min(j1 + 2, self.n)) for i in
                         range(max(i1 - 1, 0), min(i1 + 2, self.m))]

            # update the view matrix
            for i, j in neighbors:
                view[i][j] = self.terrain[i][j]

            # update the fog matrix (only if interfere==True)
            if interfere:
                for i, j in neighbors:
                    self.fog[i][j] = False  # clear the fog out of the way

        return view
