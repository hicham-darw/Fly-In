from webcolors import name_to_rgb
from time import sleep


class Visualizer:
    """Visualizer it's display colored output
    in terminal with escape sequence 
    """

    @classmethod
    def colored_print(cls, move_action: str, color: str | None, connection: str | None) -> None:
        if color is None:
            color = 'white'
        try:
            rgb = name_to_rgb(color.lower())
        except ValueError as e:
            rgb = name_to_rgb('white')
        colored = '\033[38;2;' + str(rgb.red) + ';' + str(rgb.green) + ';' + str(rgb.blue) + 'm' 
        if connection is not None:
            colored += " \033[5m"
        print(colored, end='', flush=True)
        for c in move_action:
            print(c, end='', flush=True)
            sleep(0.02)
        print('\033[0m\033[25m', end='', flush=True)            
