class TextTools:
    def __init__(self):
        pass
    @staticmethod
    def list_contrast(list_in: list, contacter: str = "_") -> list:
        """
        This function is used to generate contrast list from a given list.
        Args:
            list_in: A list of elements.
            contacter: A string used to connect two elements in the contrast list.
        Returns:
            A list of contrast elements.
        """
        return [f"{i}{contacter}{j}" for idx, i in enumerate(list_in) for j in list_in[idx + 1:]]