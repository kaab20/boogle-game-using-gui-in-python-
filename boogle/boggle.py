from GUI import Gui
from ex11_utils import dump_json


def on_closing(g):
    """
    closing function
    :param g: Gui object
    :return: save_function calls when user close the game
    """
    def save_score():
        """
        this function save the current score of user in data_base (names.json) and ends the game
        """
        try:
            g.names_dict[g.name][1].append(g.score)
            dump_json("names.json", g.names_dict)
        except:
            pass
        g.root.destroy()
    return save_score


if __name__ == '__main__':
    g = Gui()
    g.root.title('The game')
    g.root.geometry("1280x720")
    g.root.geometry("+%d+%d" % (320, 150))
    g.root.resizable(0, 0)
    g.root.protocol("WM_DELETE_WINDOW", on_closing(g))
    g.start()

