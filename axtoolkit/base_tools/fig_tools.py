class FigTools:
    def __init__(self):
        pass

    def fig_out_path(out_name: str):
        """This function generate the output path of the figure.
        Args:
            out_name (str): The name of the output file.

        Returns:
            str (str): a list of output file paths with different extensions.

        Example:
            >>> fig_out_path('figure_name')
            ['figure_name.svg', 'figure_name.pdf', 'figure_name.png']
        """
        return [f"{fig_tools.FigTools.replace_extension(out_name, ext)}" for ext in ['svg', 'pdf', 'png']]