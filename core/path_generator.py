import random

def generate_random_paths(num_points, num_paths=20):
    paths = []

    for _ in range(num_paths):
        path = list(range(num_points))
        random.shuffle(path)
        paths.append(path)

    return paths

def generate_row_wise_path(points):
    # sort points by y first, then x
    sorted_points = sorted(enumerate(points), key=lambda x: (x[1][1], x[1][0]))

    path = [idx for idx, _ in sorted_points]

    return path