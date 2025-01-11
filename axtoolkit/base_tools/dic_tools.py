def merge2dicts(dict1, dict2):
    """
    Merge two dictionaries with list values.
    If a key exists in both dictionaries, the values are appended to the list in dict1.
    If a key exists in only one dictionary, it is added to dict1.
    If a key exists in both dictionaries but the values are not lists, a ValueError is raised.
    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.
    Returns:
        dict: The merged dictionary.
    """
    for key in dict2:
        if key in dict1:
            # 如果键在 dict1 中，确保值为列表并追加 dict2 的值
            if not isinstance(dict1[key], list):
                dict1[key] = [dict1[key]]
            dict1[key].append(dict2[key])
        else:
            raise ValueError("Key not found in dict1: {}, tow dicts are not compatible".format(key))
    return dict1