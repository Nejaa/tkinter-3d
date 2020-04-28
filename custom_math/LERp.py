
def lerp(min, max, start, end, unknown):
    return (min*(end-unknown)+max*(unknown-start))/(end-start)
