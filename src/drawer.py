def draw_map(input):
    points = input['zpots']
    special_points = []

    minX = points[0]['x']
    minY = points[0]['y']
    maxX = points[0]['x']
    maxY = points[0]['y']

    for point in points:
        minX = min(minX, point['x'])
        minY = min(minY, point['y'])
        maxX = max(maxX, point['x'])
        maxY = max(maxY, point['y'])
        if point['type'] != 'default':
            special_points.append(point)

    sizeX = maxX - minX + 1
    sizeY = maxY - minY + 1

    game_map: str = ('*' * sizeX + '\n') * sizeY
    
    for point in special_points:
        game_map
    print(game_map)