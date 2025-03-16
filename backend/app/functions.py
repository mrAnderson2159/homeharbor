def flat_singleton_list(lst: list[tuple[str]]) -> list[str]:
    """
    Appiattisce una lista di tuple in una lista di stringhe.

    :param lst: Lista di tuple da appiattire.
    :return: Lista di stringhe.
    """
    return [item[0] for item in lst]
