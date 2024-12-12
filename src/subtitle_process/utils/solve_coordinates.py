from typing import List


def solve_coordiante(coordinates: List[List[float]]):
    return {
        "left_top_x": coordinates[0][0],
        "left_top_y": coordinates[0][1],
        "right_top_x": coordinates[1][0],
        "right_top_y": coordinates[1][1],
        "left_bottom_x": coordinates[3][0],
        "left_bottom_y": coordinates[3][1],
        "right_bottom_x": coordinates[2][0],
        "right_bottom_y": coordinates[2][1],
    }