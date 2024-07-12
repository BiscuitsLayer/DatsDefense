def draw_map(input):
    zombie_spawners = input['zpots']
    special_points = []

    minX = zombie_spawners[0]['x']
    minY = zombie_spawners[0]['y']
    maxX = zombie_spawners[0]['x']
    maxY = zombie_spawners[0]['y']

    for point in zombie_spawners:
        minX = min(minX, point['x'])
        minY = min(minY, point['y'])
        maxX = max(maxX, point['x'])
        maxY = max(maxY, point['y'])
        if point['type'] != 'default':
            special_points.append(point)

    sizeX = maxX - minX + 1
    sizeY = maxY - minY + 1

    game_map: str = ('*' * sizeX + '\n') * sizeY
