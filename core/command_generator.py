def path_to_commands(points, path):
    commands = []

    for index in path:
        x, y = points[index]
        cmd = f"X{int(x)} Y{int(y)}"
        commands.append(cmd)

    # ✅ ADD THIS AFTER LOOP (not inside)
    if len(commands) > 0:
        commands.append(f"X{int(points[path[0]][0])} Y{int(points[path[0]][1])}")

    return commands