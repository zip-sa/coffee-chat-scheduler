def deduplicate_and_sort(items: list[str]) -> list[str]:
    """
    remove duplicated List values and sort them

    >>> items = ["b", "a", "b", "a", "c", "b"]
    >>> result = deduplicate_and_sort(items)
    >>> assert result ==["b", "a", "c"]
    """
    return list(dict.fromkeys(items))
