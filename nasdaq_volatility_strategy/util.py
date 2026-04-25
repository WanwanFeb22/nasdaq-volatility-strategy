COLOR_CODE = {
    'Red': '\033[91m',
    'Green': '\033[92m',
    'Blue': '\033[94m',
    'Cyan': '\033[96m',
    'White': '\033[97m',
    'Yellow': '\033[93m',
    'Magenta': '\033[95m',
    'Black ': '\033[90m',
    }

def color_print(msg, color=None):
    """
    Print colored messages in the terminal for better readability.
    """

    if color:
        color_code = COLOR_CODE[color]
        print(f'{color_code}{msg}\033[0m')
    else:
        color_code = COLOR_CODE['Green']
        print(f'{color_code}{msg}\033[0m')
