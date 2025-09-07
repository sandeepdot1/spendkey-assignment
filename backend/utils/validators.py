from utils.errors import ApiError

def must_be_positive_int(name: str, value):
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise ApiError(f"'{name}' must be an integer", 400)
    if ivalue <= 0:
        raise ApiError(f"'{name}' must be > 0", 400)
    return ivalue
