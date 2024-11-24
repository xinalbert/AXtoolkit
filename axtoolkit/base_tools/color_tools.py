class ColorTools:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_color(color_fmt='hex'):
        """generate random color，color_fmt in ['rgb', 'hex', 'hsv']
        Args:
            color_fmt: color format, default is 'hex'
        Returns:
            color code of the format
        Example:
            >>> generate_random_color()
            '#7f7f7f'
            >>> generate_random_color('rgb')
            '127,127,127'
            >>> generate_random_color('hsv')
            '0.5,0.5,0.5'

        :param 
            color_fmt: color format, default is 'hex'
        :return: color code of the format
        """
        import random
        if color_fmt == 'rgb':
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return f'{r},{g},{b}'
        elif color_fmt == 'hex':
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return f'#{r:02x}{g:02x}{b:02x}'
        elif color_fmt == 'hsv':
            h = random.random()
            s = random.random()
            v = random.random()
            return f'{h},{s},{v}'
        else:
            return None