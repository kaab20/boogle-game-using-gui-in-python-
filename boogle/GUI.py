from ex11_utils import load_json, dump_json, path_to_word, read_words_file, find_neighbors, all_board_coordinates
import tkinter as t
from tkinter import messagebox
from boggle_board_randomizer import randomize_board
import string


class Gui:
    """
    this class represent every GUI element in game
    """
    WIDTH = 1280
    HEIGHT = 720
    NAMES_JSON_FILE = "names.json"
    WORDS_FILE_NAME = "boggle_dict.txt"

    NO_FILLING_MSG = "Please fill name box and password box"
    NO_MATCHES_PASS_MSG = "This password didn't match with your password"
    INVALID_LITTER_MSG = "U have to choose neighbor letter of "
    PLAY_AGAIN_MSG = "Do u wanna play again?"
    WRONG_WORD_GUESS_MSG = "Try to find another word!"

    LETTERS_PATH = "Letters\\"
    MENU_BACKGROUND_PATH = "Backgrounds\\menu_back.png"
    USERNAME_DETAILS_BACKGROUND_PATH = "Backgrounds\\saves_back.png"
    GAME_BACKGROUND_PATH = "Backgrounds\\game_back.png"
    SUFFIX_PNG = ".png"
    MINUTES = 3
    SECONDS = 1

    def __init__(self):
        """
        initialize the game
        """
        self.root = t.Tk()
        self.words = read_words_file(Gui.WORDS_FILE_NAME)
        self.open_photos()
        self.build_menu()

    def open_photos(self):
        """
        this function opens the demanded photos
        """
        self.menu_back = t.PhotoImage(file=Gui.MENU_BACKGROUND_PATH)
        self.saves_back = t.PhotoImage(file=Gui.USERNAME_DETAILS_BACKGROUND_PATH)
        self.game_back = t.PhotoImage(file=Gui.GAME_BACKGROUND_PATH)
        self.letters_photos = dict.fromkeys(string.ascii_uppercase, None)
        for letter in self.letters_photos:
            photo_path = Gui.LETTERS_PATH + letter + Gui.SUFFIX_PNG
            self.letters_photos[letter] = t.PhotoImage(file=photo_path)
        self.letters_photos["QU"] = t.PhotoImage(file=(Gui.LETTERS_PATH + "QU.png"))

    def _build_page(self, back_photo, button_func):
        """
        this function creates page (canvas) with back_photo as background of it, and button_func as button function
        that's calls when user clicks on it
        :param back_photo: PhotoImage object with background image
        :param button_func: button function that's calls when user clicks on it
        """
        self.main_canvas = t.Canvas(self.root, width=Gui.WIDTH, height=Gui.HEIGHT)
        self.main_canvas.create_image(Gui.WIDTH//2, Gui.HEIGHT//2, image=back_photo)
        self.main_canvas.bind("<Button-1>", button_func)
        self.main_canvas.pack()

    def build_menu(self):
        """
        creates menu page
        """
        self._build_page(self.menu_back, self.next_button)
        self.texts()

    def texts(self):
        """
        creates the texts boxes (name - password)
        """
        self.name_text = t.Entry(self.main_canvas, width=30, justify=t.CENTER, bg="#7A7AC5", font=('Times', 20, 'bold'))
        self.name_text.place(x=410, y=275)
        self.passward_text = t.Entry(self.main_canvas, width=30, justify=t.CENTER, bg="#7A7AC5",
                                     font=('Times', 20, 'bold'), show='*')
        self.passward_text.place(x=410, y=415)

    def next_button(self, event):
        """
        next button function that calls when user clicks on "submit" in menu page,
        and checks if the name that user wrote in our database (names.json), if it is checks if password matches with
        his username, if not requests another password, if the name wasn't in our database this function creates
        new user and moves to another page
        :param event: x, y coordinate of user click
        """
        if 378 <= event.x <= 900 and 487 <= event.y <= 583:
            if not self.name_text.get() or not self.passward_text.get():
                messagebox.showerror("Not filled", Gui.NO_FILLING_MSG)
                return
            names = load_json(Gui.NAMES_JSON_FILE)
            self.name = self.name_text.get()
            if self.name_text.get() in names:
                if self.passward_text.get() != names[self.name][0]:
                    messagebox.showerror("Wrong password", Gui.NO_MATCHES_PASS_MSG)
                    return
            else:
                dump_json(Gui.NAMES_JSON_FILE, {self.name: [self.passward_text.get(), []]})
            self.saves_page()

    def saves_page(self):
        """
        this function creates the username details page
        """
        self.main_canvas.destroy()
        self._build_page(self.saves_back, self.start_button)
        self.label_scores = t.Label(self.main_canvas, image=self.game_back, width=430, height=370, fg="white",
                                    compound='center', font=("Roman", 25))
        self.label_scores.place(x=730, y=200)
        self.show_scores()
        self.name_label = t.Label(self.main_canvas, image=self.game_back, text=self.name, font=("Roman", 50), width=400,
                                  height=100, fg="white", compound='center')
        self.name_label.place(x=120, y=280)

    def show_scores(self):
        """
        this function shows last games score if was
        :return:
        """
        self.names_dict = load_json(Gui.NAMES_JSON_FILE)
        scores = ""
        for score in self.names_dict[self.name][1]:
            scores += str(score)
            scores += "\n"
        self.label_scores.config(text=scores)

    def start_button(self, event):
        """
        this function checks if user clicks to start the game, and starts the game accord that
        :param event: x, y coordinate of user click
        """
        if 70 <= event.x <= 588 and 547 <= event.y <= 647:
            self.start_game()

    def start_game(self):
        """
        create game page
        :return:
        """
        # ---------- init game page---------- #
        self.main_canvas.destroy()
        self._build_page(self.game_back, self.submit)
        # ---------- init game basics---------- #
        self.board = randomize_board()
        self.buttons = []
        self.all_cells = all_board_coordinates(self.board)
        self.current_path = []
        self.current_buttons = []
        self.words_guessed = []
        self.score = 0
        self.mins, self.sec = Gui.MINUTES, Gui.SECONDS
        # ---------- init game elements ---------- #
        self.build_board()
        self.build_current_word_label()
        self.build_score_label()
        self.build_words_guessed_label()
        self.build_timer()

    def build_board(self):
        """
        creates board on page
        """
        x = 390  # initial x of first button page
        y = 154  # initial y of first button page
        for i in range(4):
            for j in range(4):
                b = t.Button(self.main_canvas, image=self.letters_photos[self.board[i][j]], bg="purple")
                b.config(command=self.letter_command(i, j, b))
                self.buttons.append(b)
                b.place(x=x, y=y)
                x += 125
            x = 390
            y += 97

    def letter_command(self, i, j, b):
        """
        letter button command that stored i, j and b
        :param i: row number
        :param j: column number
        :param b: Button object
        :return: add_letters function
        """
        def add_letter():
            """
            this function checks if the clicked letter button is legal or not, if it is adds this letter to current word
            """
            if (i, j) not in find_neighbors(self.current_path, self.all_cells):
                messagebox.showwarning("Wrong letter", (Gui.INVALID_LITTER_MSG +
                                                        self.board[self.current_path[-1][0]][self.current_path[-1][1]]))
                return
            self.current_buttons.append(b)
            self.current_path.append((i, j))
            b.config(bg="yellow")
            new_word = self.current_word_label.cget("text") + self.board[i][j]
            self.current_word_label["text"] = new_word
        return add_letter

    def build_current_word_label(self):
        """
        creates current word label
        """
        self.current_word_label = t.Label(self.main_canvas, text="", font=("Arial", 18), fg="White",
                                          image=self.game_back, compound='center', width=300, height=50)
        self.current_word_label.place(x=40, y=220)

    def build_score_label(self):
        """
        creates current score label
        """
        self.score_label = t.Label(self.main_canvas, text="0", font=("Arial", 18), fg="White",
                                   image=self.game_back, compound='center', width=50, height=50)
        self.score_label.place(x=180, y=345)

    def build_words_guessed_label(self):
        """
        creates current words guessed label
        """
        self.words_guessed_label = t.Label(self.main_canvas, text="", font=("Arial", 18), fg="White", image=self.game_back,
                                   compound='center', width=294, height=300)
        self.words_guessed_label.place(x=950, y=250)

    def build_timer(self):
        """
        creates current timer label
        """
        self.timer_label = t.Label(self.main_canvas, text="3:00", font=("Arial", 18), fg="White", image=self.game_back,
                                   compound='center', width=70, height=50)
        self.timer_label.place(x=630, y=40)
        self.time()

    def time(self):
        """
        this function manage the countdown in game, and calls each minute until reaches a zero then calls end_game func
        """
        if self.sec != 0:
            self.sec -= 1
        else:
            self.sec = 59
            self.mins -= 1
        if self.mins == -1:
            self.root.after_cancel(self.timer)
            self.end_game()
            return
        time = str(self.mins) + " : " + str(self.sec)
        if self.sec <= 9:
            time = str(self.mins) + " : 0" + str(self.sec)
        self.timer_label["text"] = time
        self.timer = self.root.after(1000, self.time)

    def end_game(self):
        """
        saves the current score to this user database, and ask him for play again, if he agrees starts a new game,
        else, ends the game
        """
        self.names_dict[self.name][1].append(self.score)
        dump_json("names.json", self.names_dict)
        play_again = messagebox.askyesno("Game Over!", Gui.PLAY_AGAIN_MSG)
        if play_again:
            self.start_game()
        else:
            self.root.destroy()

    def submit(self, event):
        """
        checks if the current word is legal, and adds score upon that, shows error message otherwise
        :param event: x, y coordinate of user click
        """
        if 510 <= event.x <= 768 and 612 <= event.y <= 683:
            word = path_to_word(self.current_path, self.board)
            if word in self.words and self.words[word] is False:
                self.add_score(len(word))
                self.add_guessed_word(word)
            else:
                messagebox.showinfo("Wrong guess", Gui.WRONG_WORD_GUESS_MSG)
            self.reset_current_word()

    def add_score(self, n):
        """
        adds n squared points to user score
        :param n: word length
        """
        self.score += n ** 2
        self.score_label["text"] = str(self.score)

    def add_guessed_word(self, word):
        """
        adds word guessed to words guessed frame (label)
        :param word: guessed word
        """
        self.words[word] = True
        if self.words_guessed and len(self.words_guessed) % 3 == 0:
            self.words_guessed_label["text"] = self.words_guessed_label.cget("text") + "\n"
        self.words_guessed_label["text"] = self.words_guessed_label.cget("text") + word + ", "
        self.words_guessed.append(word)

    def reset_current_word(self):
        """
        resets the current word elements
        """
        for b in self.current_buttons:
            b.config(bg="purple")
        self.current_path = []
        self.current_buttons = []
        self.current_word_label["text"] = ""

    def start(self):
        """
        starts the mainloop of tkinter root
        """
        self.root.mainloop()
