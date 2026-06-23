def generate_square(size=100, num_points=40):
    points = []
    step = size / (num_points // 4)

    # Bottom edge (left → right)
    for i in range(num_points // 4):
        x = i * step
        y = 0
        points.append((x, y))

    # Right edge (bottom → top)
    for i in range(num_points // 4):
        x = size
        y = i * step
        points.append((x, y))

    # Top edge (right → left)
    for i in range(num_points // 4):
        x = size - i * step
        y = size
        points.append((x, y))

    # Left edge (top → bottom)
    for i in range(num_points // 4):
        x = 0
        y = size - i * step
        points.append((x, y))

    return points