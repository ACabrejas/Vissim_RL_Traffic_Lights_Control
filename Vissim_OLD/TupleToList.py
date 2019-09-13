# Function to convert a nested tuple to a nested list
def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple