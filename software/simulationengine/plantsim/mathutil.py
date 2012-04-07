

def clamp(v, min, max):
    if v < min: return min
    elif v > max: return max
    else: return v

def lerp(a, b, t):
    return a * (1.0 - t) + b * t

