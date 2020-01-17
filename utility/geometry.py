def distance_line_to_point(line,point):
    ((x0,y0),(x1,y1)) = line
    (x2,y2) = point
    nom = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denom = ((y2 - y1)**2 + (x2 - x1) ** 2) ** 0.5
    result = nom / denom
    return result
