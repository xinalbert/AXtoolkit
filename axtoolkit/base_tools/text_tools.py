class TextTools:
    def __init__(self):
        pass
    @staticmethod
    def list_contrast(list_in: list) -> list:
        """
        This function calculates the contrast of a list of str.

        Parameters:
        list_in (list): A list of str.

        Returns:
        list: The contrast of the list of str.
        """
        return [f"{i}_{j}" for idx, i in enumerate(list_in) for j in list_in[idx + 1:]]