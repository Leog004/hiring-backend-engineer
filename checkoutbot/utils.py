def checkIfInteger(**kwargs):
    for arg in kwargs.values():
        if not isinstance(arg, int) or arg < 0:
            return False
    
    return True
