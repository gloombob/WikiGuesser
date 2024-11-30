import project
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
import webbrowser
import csv
import CTkTable

# MainWindow is the parent class of all other classes
# MainWindow as subclass of the CTk class, no need to define self.root = CTk() as MainWindow already is itself part of the CTk class
class MainWindow(CTk):
    def __init__(self):

        super().__init__()

        self.title("WikiGuesser")
        self.geometry("500x500")

        set_appearance_mode("light") # sets appearance mode to always light

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # construct all the frames
        # self.frames is a dict by which we can access the frames with their respective keys
        self.frames = {}

        # startframe is the frame for the starting page
        # startframe is shown initally
        self.startframe = CTkFrame(self)
        self.frames["startframe"] = self.startframe

        self.startframe.grid(column=0, row=0, sticky="nsew")
        self.active_frame = self.startframe

        self.startframe.configure(fg_color="white")

        self.startframe.grid_columnconfigure(0, weight=1)
        self.startframe.grid_rowconfigure(0, weight=1)
        self.startframe.grid_rowconfigure(1, weight=0)
        self.startframe.grid_rowconfigure(2, weight=0)
        self.startframe.grid_rowconfigure(3, weight=0)
        self.startframe.grid_rowconfigure(4, weight=1)

        self.gameframe = self.GameFrame(self)
        self.gameframe.configure(fg_color="white")
        self.frames["gameframe"] = self.gameframe

        self.scoreboardframe = self.ScoreboardFrame(self)
        self.scoreboardframe.configure(fg_color="white")
        self.frames["scoreboardframe"] = self.scoreboardframe

        self.gameoverframe = self.GameoverFrame(self, 0)
        self.gameoverframe.configure(fg_color="white")
        self.frames["gameoverframe"] = self.gameoverframe

        # set up the logo
        image_path = "wikiguesser.jpg"
        self.image = Image.open(image_path)
        self.logo = CTkImage(self.image, size=(425, 69))

        self.image_label = CTkLabel(self.startframe, image=self.logo, text="")
        self.image_label.grid(pady=20)

        self.startbttn = CTkButton(self.startframe, text="Start game", fg_color="#65166e", hover_color="#1a9c86", corner_radius=100, command=lambda: self.switch_to_frame("gameframe"))
        self.startbttn.grid(column=0, row=1, pady=10)

        self.scoreboardbttn = CTkButton(self.startframe, text="Scoreboard", fg_color="#65166e", hover_color="#1a9c86", corner_radius=100, command=lambda: self.switch_to_frame("scoreboardframe"))
        self.scoreboardbttn.grid(column=0, row=2, pady=10)

        self.exitbttn = CTkButton(self.startframe, text="Exit game", fg_color="#65166e", hover_color="#1a9c86", corner_radius=100, command=self.destroy)
        self.exitbttn.grid(column=0, row=3, pady=10)

        self.mainloop()

    # grid the target frame, remove the previously active frame
    # assign target frame as active frame
    def switch_to_frame(self, target_frame: str):
        frame = self.frames[target_frame]

        self.active_frame.grid_remove()

        frame.grid(column=0, row=0, sticky="nsew")

        self.active_frame = frame

        if self.active_frame == self.scoreboardframe:
            self.scoreboardframe.update_table()
        if self.active_frame == self.gameoverframe:
            self.gameoverframe.reset()

    # used by end_game in GameFrame to pass self.score from GameFrame to GameoverFrame as the value is needed there for saving it to scoreboard.csv
    def update_score(self):
        score = self.gameframe.score
        self.gameoverframe.score = score
        self.gameoverframe.gameover_label.configure(text=f"Gameover! Your score was {self.gameoverframe.score}")

    # class of game frame, instanciated when calling switch_to_gameframe()
    class GameFrame(CTkFrame):
        def __init__(self, parent): # self refers to instance of GameFrame, parent (MainWindow) is passed when instance is created
            super().__init__(parent)

            # define the parent (MainWindow) as attribute of GameFrame; self.parent.attribute lets us access attributes of MainWindow
            self.parent = parent

            # define the frames layout
            self.grid_columnconfigure(1, weight=1, uniform="colsize")
            self.grid_columnconfigure(0, weight=1, uniform="colsize")
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=1)

            self.explain_label = CTkLabel(self, text="Which Wikipedia article has been viewed more often in the last 30 days?", font=("Arial", 15))
            self.explain_label.grid(column=0, row=0, columnspan=2, pady=10)

            # start the game, set score to 0
            self.first_article, self.first_views, self.second_article, self.second_views = project.start_game()
            self.score = 0

            self.score_label = CTkLabel(self, text=f"Score: {self.score}", font=("Arial", 16))
            self.score_label.grid(column=0, row=3, columnspan=2, pady=10)

            # set up buttons to click
            self.leftchoice_bttn = CTkButton(self, text=self.first_article.replace("_", " "), width=100, height=400, fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.answer("left"))
            self.leftchoice_bttn.grid(column=0, row=1, sticky="nsew")

            self.rightchoice_bttn = CTkButton(self, text=self.second_article.replace("_", " "), width=100, height=400, fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.answer("right"))
            self.rightchoice_bttn.grid(column=1, row=1, sticky="nsew")

            # set up butttons to open the wikipedia article
            # IMPORTANT: the urls are updated automatically when this button is clicked, as it accesses the self.first_article / second_article when the button is pressed
            # by then, the article has been updated
            self.openleft_bttn = CTkButton(self, text="Read this article", command=lambda: webbrowser.open(url=f"https://en.wikipedia.org/wiki/{self.first_article}", new=2))
            self.openleft_bttn.grid(column=0, row=2, pady=10)

            self.openright_bttn = CTkButton(self, text="Read this article", command=lambda: webbrowser.open(url=f"https://en.wikipedia.org/wiki/{self.second_article}", new=2))
            self.openright_bttn.grid(column=1, row=2, pady=10)

            self.feedback_label = CTkLabel(self, text="")
            self.feedback_label.grid(column=0, row=4, columnspan=2, pady=10)

        # called by end_game, if wrong answer
        def restart_game(self):
            # update articles and views, reset self.score and feedback to None
            self.first_article, self.first_views, self.second_article, self.second_views = project.start_game()

            # update the buttons with new article names
            self.leftchoice_bttn.configure(text=self.first_article.replace("_", " "))
            self.rightchoice_bttn.configure(text=self.second_article.replace("_", " "))

            # reset score for gameframe to 0
            self.score = 0

            # reset labels
            self.score_label.configure(text=f"Score: 0")
            self.feedback_label.configure(text="")

        # called if wrong answer, update score for gameoverframe, reset labels and get new articles, switch to gameoverframe frame
        def end_game(self):
            # call function from MainWindow that passes self.score from GameFrame to GameoverFrame
            self.parent.update_score()
            self.restart_game()
            self.parent.switch_to_frame("gameoverframe") # self.parent == MainWindow

        def answer(self, choice: str): # choice is str for each button
            # determine which button was pressed
            guess = self.get_guess(choice)
            # compare the guess against the correct answer
            feedback, self.score = project.compare_results(self.first_views, self.second_views, self.score, guess) # returns the result
            # put together feedback for feedback_label
            feedback = feedback + f" {self.first_views:,d} vs. {self.second_views:,d} views"

            # if wrong, reset, open game-over frame
            if feedback.startswith("Wrong!"):
                self.end_game()

            # else: update feedback and score
            # go for next round, update articles and views
            elif feedback.startswith("Correct!"):
                self.feedback_label.configure(text=feedback)
                self.score_label.configure(text=f"Score: {self.score}")

                # call function to run again, update the self. ... values to the new article names and views
                self.first_article, self.first_views, self.second_article, self.second_views = project.start_game(self.second_article, self.second_views)

                # update the text of the buttons
                self.leftchoice_bttn.configure(text=self.first_article.replace("_", " "))
                self.rightchoice_bttn.configure(text=self.second_article.replace("_", " "))

         # converts guess
        def get_guess(self, choice):
                if choice == "left":
                    return 1
                elif choice == "right":
                    return 2

    # Frame that is shown when wrong answer given
    class GameoverFrame(CTkFrame):
        def __init__(self, parent, score):
            super().__init__(parent)

            self.parent = parent # parent == MainWindow
            self.score = score
            self.grid_columnconfigure(0, weight=1)

            self.gameover_label = CTkLabel(self, text=f"Gameover! Your score was {self.score}", text_color="black")
            self.gameover_label.grid(column=0, pady=10)

            # get users name
            self.entername_label = CTkLabel(self, text="Enter name to save your score", text_color="black")
            self.entername_label.grid(column=0, pady=10)

            self.entername_entrybox = CTkEntry(self, placeholder_text="Name...", width=200, text_color="white", fg_color="#65166e")
            self.entername_entrybox.grid(column=0, pady=10)

            # saves entered name to scoreboard.csv
            self.savename_bttn = CTkButton(self, text="Save name", fg_color="#65166e", hover_color="#1a9c86", command = self.save_name)
            self.savename_bttn.grid(column=0, pady=10)

            # switches to gameframe
            self.playagain_bttn = CTkButton(self, text="Play again", fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.parent.switch_to_frame("gameframe"))
            self.playagain_bttn.grid(column=0, pady=10)

            # switches to startframe
            self.exit_bttn = CTkButton(self, text="Return to Start", fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.parent.switch_to_frame("startframe"))
            self.exit_bttn.grid(column=0, pady=10)

        # save_name function, used by savename_bttn
        def save_name(self):
            # get name from entername_entrybox
            if self.entername_entrybox.get() != "":
                self.name = self.entername_entrybox.get()

                # get existing names in "scoreboard.csv" as scoreboard_list, append new entry to list
                with open("scoreboard.csv", "r") as file:
                    reader = csv.DictReader(file)
                    # create list of dictionaries
                    self.scoreboard_list = [entry for entry in reader]

                # append new dict of name and score to scoreboard_list
                self.scoreboard_list.append({"name": self.name, "score": self.score})

                # sort scoreboard_list by score (descending, hence the -)
                self.sorted_scoreboard = sorted(self.scoreboard_list, key=lambda entry: -int(entry["score"]))

                # write only 10 first values "to scoreboard.csv", so 1 (lowest score) falls out
                with open("scoreboard.csv", "w", newline="") as scoreboard_file:
                    fieldnames = ["name", "score"]
                    writer = csv.DictWriter(scoreboard_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for entry in self.sorted_scoreboard[0:10]:
                        writer.writerow({"name": entry["name"], "score": entry["score"]})

                # deactivate savename_bttn after saving name
                self.savename_bttn.configure(state=DISABLED)

            # don't take empty name, display warning message
            else:
                emptyname_msg = CTkMessagebox(title="Enter your name", message="You need to give a name to save your score.", fg_color="white")

        # reset savename button if disabled, delete name from entrybox
        def reset(self):
            if self.savename_bttn.cget("state") == "disabled":
                self.savename_bttn.configure(state=NORMAL)
                self.entername_entrybox.delete(0, "end")

    # frame that displays scoreboard data using a CTkTable
    class ScoreboardFrame(CTkFrame):
        def __init__(self, parent):
            super().__init__(parent)

            self.parent = parent

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=1)

            # read data from scoreboard.csv, assign to self.score_data as list of lists
            with open("scoreboard.csv", "r") as file:
                reader = csv.reader(file)
                self.score_data = [row for row in reader]

            self.scoreboard_table = CTkTable.CTkTable(self, row=11, column=2, header_color="#65166e", colors=["#9ba1ab", "#c4c7cc"], text_color="white", values=self.score_data)
            self.scoreboard_table.pack(expand=True, fill="both", padx=20, pady=20)

            self.return_bttn = CTkButton(self, text="Return to Start", fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.parent.switch_to_frame("startframe"))
            self.return_bttn.pack(pady=10)

        def update_table(self):
            self.scoreboard_table.destroy()
            self.return_bttn.destroy()

            # read scoreboard data to account for changes, construct table again
            with open("scoreboard.csv", "r") as file:
                reader = csv.reader(file)
                self.score_data = [row for row in reader]

            self.scoreboard_table = CTkTable.CTkTable(self, row=11, column=2, header_color="#65166e", colors=["#9ba1ab", "#c4c7cc"], text_color="white", values=self.score_data)
            self.scoreboard_table.pack(expand=True, fill="both", padx=20, pady=20)

            self.return_bttn = CTkButton(self, text="Return to Start", fg_color="#65166e", hover_color="#1a9c86", command=lambda: self.parent.switch_to_frame("startframe"))
            self.return_bttn.pack(pady=10)

project.check_requests()
GUI = MainWindow()