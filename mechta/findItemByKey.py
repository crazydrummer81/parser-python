def findItemByKey(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = findItemByKey(v, key)
            if item is not None:
                return item
