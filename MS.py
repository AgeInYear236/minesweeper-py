import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageFont, ImageDraw
from PIL import Image, ImageTk
import random
import settings
import pygame
import math

vol=0
opened_cells = 1
T = False
timeConst = 50
time_left = timeConst
prev_time_left = 0
prev_time_ms_left = 0
score = 0
global flag_col
global def_col
flag_col = 'red'
def_col = 'white'

global cw
cw=0
global ch
ch=0

# - - - - - - - - - - EXT
class GameTimer:
    def __init__(self, root, timer_label):
        self.root = root
        self.timer_label = timer_label
        self.timer_running = False
        self.is_countdown = False
        self.elapsed_time = 0
        self.elapsed_milliseconds = 0
        self.time_left = 0

    def start_timer(self, countdown=False, start_time=0):

        self.is_countdown = countdown
        self.timer_running = True
        if countdown:
            self.time_left = int(start_time)
            self.elapsed_milliseconds = int((start_time - self.time_left) * 1000) 
        else:
            self.elapsed_time = 0
            self.elapsed_milliseconds = 0
        self.update_timer()


    def stop_timer(self):
        self.timer_running = False

    def resume_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.elapsed_milliseconds = 0
        self.time_left = 0
        self.update_label()

    def update_timer(self):
        if not self.timer_running:
            return

        if self.is_countdown:
            if self.time_left > 0:
                self.time_left -= 0.01
                if self.time_left <= 0:
                    self.time_left = 0
                    self.stop_timer()
                    self.on_timer_end()
            else:
                self.stop_timer()
        else:
            self.elapsed_time += 0.01 

        self.update_label()
        self.root.after(10, self.update_timer)


    def update_label(self):
        if self.is_countdown:
            time_display = f"Time: {self.time_left:.2f} sec"
        else:
            elapsed_total_time = self.elapsed_time + self.elapsed_milliseconds / 1000
            time_display = f"Time: {elapsed_total_time:.2f} sec"
        self.timer_label.config(text=time_display)


    def on_timer_end(self):
        self.timer_label.config(text="Time's up!")
        display_victory_screen(0)

# - - - - - - - - - - PROPS
def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)

def play_music_once(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    global vol
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()


def load_font(textToLoad, sizeInt):
    font = ImageFont.truetype("Font.ttf", size=sizeInt)
    
    image = Image.new("RGB", (200, 50), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), textToLoad, font=font, fill="black")

    return ImageTk.PhotoImage(image)

def write_time_to_file(time, board_size, mines_count):
    with open("game_times.txt", "a") as file:
        file.write(f"Time: {time} seconds, Board Size: {board_size}, Mines: {mines_count}\n")

def write_score_to_file(board_size, score):
    with open("timed_scores.txt", "a") as file:
        file.write(f"Board Size: {board_size}, Score: {score}\n")

def load_leaderboard():
    leaderboard = []
    try:
        with open("game_times.txt", "r") as file:
            for line in file:
                time_data = line.strip().split(", ")
                if len(time_data) == 3:
                    time_str = time_data[0].replace("Time: ", "")
                    board_size_str = time_data[1].replace("Board Size: ", "")
                    mines_count_str = time_data[2].replace("Mines: ", "")
                    leaderboard.append((time_str, board_size_str, mines_count_str))
    except FileNotFoundError:
        messagebox.showerror("Error", "Leaderboard file not found.")
        return []

    leaderboard.sort(key=lambda x: float(x[0].split()[0]))
    return leaderboard

def load_Tleaderboard():
    leaderboard = []
    try:
        with open("timed_scores.txt", "r") as file:
            for line in file:
                time_data = line.strip().split(", ")
                if len(time_data) == 2:
                    board_size_str = time_data[0].replace("Board Size: ", "")
                    score_str = time_data[1].replace("Score: ", "")
                    leaderboard.append((board_size_str, score_str))
    except FileNotFoundError:
        messagebox.showerror("Error", "Leaderboard file not found.")
        return []

    leaderboard.sort(key=lambda x: int(score_str))
    return leaderboard

def show_leaderboard():
    leaderboard_frame = tk.Toplevel()
    leaderboard_frame.title("Leaderboard")
    
    leaderboard_data = load_leaderboard()

    grouped_data = {}
    for time, board_size, mines in leaderboard_data:
        if board_size not in grouped_data:
            grouped_data[board_size] = []
        grouped_data[board_size].append((time, mines))

    notebook = ttk.Notebook(leaderboard_frame)
    notebook.pack(expand=True, fill="both")

    for board_size, data in grouped_data.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"{board_size}")

        tree = ttk.Treeview(frame, columns=("Time", "Mines"), show="headings")
        tree.heading("Time", text="Time")
        tree.heading("Mines", text="Mines")

        for time, mines in data:
            tree.insert("", tk.END, values=(time, mines))

        tree.pack(expand=True, fill="both")
    
    back_button = tk.Button(leaderboard_frame, text="Back to Main Menu", command=leaderboard_frame.destroy)
    back_button.pack(pady=10)

def show_Tleaderboard():
    leaderboard_frame = tk.Toplevel()
    leaderboard_frame.title("Leaderboard")
    
    leaderboard_data = load_Tleaderboard()
    grouped_data = {}
    for board_size, score in leaderboard_data:
        if board_size not in grouped_data:
            grouped_data[board_size] = []
        grouped_data[board_size].append(score)

    notebook = ttk.Notebook(leaderboard_frame)
    notebook.pack(expand=True, fill="both")

    for board_size, scores in grouped_data.items():
        scores.sort(reverse=True)

        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"{board_size}")

        tree = ttk.Treeview(frame, columns=("Score",), show="headings")
        tree.heading("Score", text="Score")

        for score in scores:
            tree.insert("", tk.END, values=(score,))

        tree.pack(expand=True, fill="both")
    
    back_button = tk.Button(leaderboard_frame, text="Back to Main Menu", command=leaderboard_frame.destroy)
    back_button.pack(pady=10)

# - - - - - - - - - - BOARD
def create_board(rows, cols, mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]

    for _ in range(mines):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        while board[row][col] == '*':
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
        board[row][col] = '*'

    return board

def update_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                count = count_adjacent(board, i, j)
                if count > 0:
                    board[i][j] = str(count)

def init_board(rows, cols, isBoard):
    global score
    if(T==True):
        global score_label
        score_label.config(text=f"Score: {score}")
    print(rows)
    print (cols)
    width, height = settings.window_size.split('x')

    width = root.winfo_width()
    height = root.winfo_height()
    field_size = (width - 400)

    print(field_size)
    if(rows == 30):
        cell_width = 4 #field_size // cols // 10
        cell_height = 3 #field_size // rows // 10
        font_size = 5
        print(cell_width,cell_height, '30')
    elif(rows==20):
            cell_width = 4 #field_size // cols // 10
            cell_height = 2 #field_size // rows // 20
            font_size = 10
            print(cell_width,cell_height, '20')
    elif(rows==10):
            cell_width = 10 #field_size // cols // 10
            cell_height = 5 #field_size // rows // 20
            font_size = 10
            print(cell_width,cell_height, '10')
    elif(rows==50):
            cell_width = 3 #field_size // cols // 10
            cell_height = 5 #field_size // rows // 20
            font_size = 3
            print(cell_width,cell_height, 'XX')

    print(cell_width)
    print(cell_height)
    global cw
    cw=cell_width
    global ch
    ch=cell_height

    frame = tk.Frame(root, width=field_size, height=field_size, bd=5, relief=tk.SOLID)
    frame_width = frame.winfo_reqwidth()
    frame_height = frame.winfo_reqheight()
    x = (width - frame_width) // 2
    y = (height - frame_height) // 2
    frame.place(x=x, y=y)

    frame.pack()

    global buttons
    buttons = []
    for i in range(rows):
        row_buttons = []
        for j in range(cols):
            button_text = ' ' if isBoard == 0 else ' '
            button_command = on_click if isBoard == 1 else None
            
            button = tk.Button(frame, text=button_text, width=cell_width, height=cell_height, 
                               command=lambda i=i, j=j: button_command(i, j) if button_command else None, 
                               bg=GCS[8], font=("Arial", font_size), padx=0, pady=0)

            if isBoard == 1:
                button.bind("<Button-1>", lambda event, i=i, j=j: flag_cell(event, i, j))
                button.bind("<Button-3>", lambda event, i=i, j=j: flag_cell(event, i, j))

            button.grid(row=i, column=j, padx=2, pady=2)
            row_buttons.append(button)
        buttons.append(row_buttons)
# - - - - - - - - - -

# - - - - - - - - - - MINE LOGIC
def count_adjacent(board, x, y):
    if board[x][y] == '*':
        return 0
    count = 0
    for i in range(max(0, x - 1), min(len(board), x + 2)):
        for j in range(max(0, y - 1), min(len(board[0]), y + 2)):
            if board[i][j] == '*':
                count += 1
    return count

def on_click(row, col):
    if not game_timer.timer_running: 
        game_timer.start_timer() 
        if (T==True):
            game_timer.start_timer(True, time_left)
    if board[row][col] == '*':
        label.config(text="Boom! You hit a mine.")
        display_victory_screen(0)
    else:
        play_music_once("open.mp3")
        open_adjacent(board, row, col)

def increment():
    global opened_cells
    global score_label
    global score
    opened_cells += 1
    score += 10
    score_label.config(text=f"Score: {score}")
    print(score)

# - - - - - - - - - -

# - - - - - - - - - - GAME ITSELF
def open_adjacent(board, row, col):
    if row < 0 or col < 0 or row >= len(board) or col >= len(board[0]) or buttons[row][col]['state'] == 'disabled':
        return
    count = count_adjacent(board, row, col)
    buttons[row][col].config(text=str(count) if count > 0 else ' ', state=tk.DISABLED, bg=GCS[count])
    if(T==True):
        increment()
    if count == 0:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                open_adjacent(board, i, j)

def flag_cell(event, row, col):
    if event.num == 3 and buttons[row][col]['state'] != 'disabled': 
        if buttons[row][col]['text'] == ' ':
            play_music_once("flag.mp3")
            buttons[row][col].config(bg=flag_col, text='Flag')
        else:
            buttons[row][col].config(text=' ', bg=GCS[8], state=tk.NORMAL)
    if check_victory():
            display_victory_screen(1)

# - - - - - - - - - -

# - - - - - - - - - - UI (OTHER)
def check_victory():
    flagged_count = sum(button['text'] == 'Flag' for row in buttons for button in row)
    if flagged_count != mine_count:
        return False

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '*' and buttons[i][j]['text'] != 'Flag':
                return False

    return True

def display_victory_screen(win_status):
    global score
    game_timer.stop_timer()
    total_time = f"{game_timer.elapsed_time: .2f}"    
    board_size = f"{len(board)}x{len(board[0])}"
    mines_count = mine_count

    def restart_game():
        global T
        global timeConst
        global time_left
        victory_window.destroy()
        root.destroy()
        if(T==True):
            time_left = timeConst
            global score
            score = 0
            play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 2)
        else:
            play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 0)

    def load_main_menu():
        victory_window.destroy()
        root.destroy()
        play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 1)

    def play_next():
        global time_left
        global prev_time_left
        global prev_time_ms_left
        prev_time_left = game_timer.time_left
        prev_time_ms_left = game_timer.elapsed_milliseconds
        print(prev_time_left, time_left, " - - - - - - - - : TIMES")
        victory_window.destroy()
        root.destroy()
        play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 2)
        
    def play_sound():
        if(win_status==1):
            play_music_once("win.mp3")
        else:
            play_music_once("mine.mp3")

    victory_window = tk.Toplevel()
    victory_window.title("Victory!" if win_status == 1 else "Defeat!")
    victory_window.geometry("300x200")
    victory_window.resizable(False, False)

    play_sound()

    victory_window.update_idletasks()
    screen_width = victory_window.winfo_screenwidth()
    screen_height = victory_window.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (200 // 2)
    victory_window.geometry(f"300x200+{x}+{y}")

    message = "You win!" if win_status == 1 else "You lose!"
    victory_label = tk.Label(victory_window, text=message, font=("Arial", 20))
    victory_label.pack(padx=20, pady=10)
    global T
    if(T==True and game_timer.time_left != 0 and win_status==1):
        next_button = tk.Button(victory_window, text="Next", command=play_next)
        next_button.pack(pady=10)
    else:
        restart_button = tk.Button(victory_window, text="Restart Game", command=restart_game)
        restart_button.pack(pady=10)

    main_menu_button = tk.Button(victory_window, text="Load Main Menu", command=load_main_menu)
    main_menu_button.pack(pady=10)

    victory_window.grab_set()
    victory_window.protocol("WM_DELETE_WINDOW", lambda: close_game(victory_window))

    if win_status == 1 and T == False:
        write_time_to_file(total_time, board_size, mines_count)
    elif T == True and win_status == 1:
        score += 500 + time_left * 30
        if (game_timer.time_left == 0):
            write_score_to_file(board_size, score)
    elif T == True and win_status == 0:
        write_score_to_file(board_size, score)

def close_game(window):
    window.destroy()
    root.destroy()

# - - - - - - - - - -

def play_minesweeper(rows, cols, mines, a):
    print(settings.board_size[0])
    play_music("Miner.mp3")

    global GCS
    GCS = settings.chosen_set

    global board
    board = create_board(rows, cols, mines)
    update_board(board)

    global root
    root = tk.Tk()
    root.title("Minesweeper")
    root.resizable(False, False) 

    root.iconphoto(False, tk.PhotoImage(file="logo.png"))
    #  custom_cursor = "cursor(3).cur"  # Specify your custom cursor file path
    #  root.config(cursor=f"@{custom_cursor}")  # Use '@' to specify a cursor file

    #  image = Image.open("bgimage.png")  # Use the path to your image
    #  background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root)
    background_label.place(relwidth=1, relheight=1)

    def start_game():
        global T
        T = False
        menu_frame.pack_forget()
        pygame.mixer.music.stop()
        background_label = tk.Label(root, image=None)
        background_label.place(relwidth=1, relheight=1)
        global timer_label
        timer_label = tk.Label(root, text="Time: 0.00 sec", font=("Arial", 14))
        timer_label.pack(pady=10)

        global game_timer
        game_timer = GameTimer(root, timer_label)
        #game_timer.start_timer()
    
        game_frame.pack()
        init_board(rows, cols, 1)

    def start_timed():
        global T
        T = True
        global time_left
        global prev_time_left
        global prev_time_ms_left
        if (prev_time_left != 0):
            time_left = prev_time_left
            time_left = math.ceil(time_left)
            time_left += 10
            #time_left += prev_time_ms_left * 0.0001            - -  - - --  -  - -  -  - -  -  - NE ROBIT !
            #print("MILLISECONDS: - - - - - - - - - - - -", prev_time_ms_left * 0.001)
            # game_timer.elapsed_milliseconds += prev_time_ms_left

        print(time_left, prev_time_left, ":Times!")
        menu_frame.pack_forget()
        pygame.mixer.music.stop()
        background_label = tk.Label(root, image=None)
        background_label.place(relwidth=1, relheight=1)
        global timer_label
        timer_label = tk.Label(root, text=f"Time: {time_left} sec", font=("DEBROSEE", 14))
        timer_label.pack(side="top", padx=10)      
        global score_label
        score_label = tk.Label(root, text=f"Score: {score}", font=("DEBROSEE", 14))
        score_label.pack(side="top", padx=10)
    
        global game_timer
        game_timer = GameTimer(root, timer_label)
        game_timer.time_left = time_left
        # game_timer.start_timer(countdown=True, start_time=timeConst)

    
        game_frame.pack()
        init_board(rows, cols, 1)

    def settings_menu():
        menu_frame.pack_forget()
        settings_frame.pack()

    def lb_menu():
        menu_frame.pack_forget()
        lb_frame.pack()

    def lb_menu_to_main_menu():
        lb_frame.pack_forget()
        menu_frame.pack()

    def display_titles():
        menu_frame.pack_forget()
        title_frame.pack()

    def settings_menu_to_main_menu():
        settings_frame.pack_forget()
        menu_frame.pack()

    def title_menu_to_main_menu():
        title_frame.pack_forget()
        menu_frame.pack()

    def exit_game():
        root.destroy()

    def dropdown_selection_changed(selection):
        index = options.index(selection)
        print(index)
        file_path = 'setts.txt' 
        search_text = "setid="

        new_set_id = index + 1 
        replace_text = f"setid={new_set_id}"

        update_file_line(file_path, search_text, replace_text)
        settings.update_data(file_path)

    def dropdown_menu_dif_func(selection):
        index = difops.index(selection)
        print(index)
        file_path = 'setts.txt'  
        search_text = "dif="

        dif_id = index + 1
        replace_text = f"dif={dif_id}"

        update_file_line(file_path, search_text, replace_text)
        settings.update_data(file_path)
    
    def change_volume(value):
        global vol
        volume = float(value) / 100 
        vol = volume
        pygame.mixer.music.set_volume(volume)
        volume_label.config(text="Volume: {}%".format(int(volume * 100)), font="DEBROSEE")
        print("Volume label: ", "Volume: {}%".format(int(volume * 100)))
        file_path = 'setts.txt'
        search_text = "volume="

        vol_val = volume
        replace_text = f"volume={vol_val}"
        update_file_line(file_path, search_text, replace_text)
        settings.update_data(file_path)

    def update_file_line(file_path, search_text, replace_text):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if line.startswith(search_text):
                   file.write(f"{replace_text}\n")
                else:
                   file.write(line)

    def load_titles_to_label(label, file_path="titles.txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "Titles file not found.")
            return

        formatted_lines = []
        for line in lines:
            parts = line.strip().split(maxsplit=1) 
            if len(parts) == 2:
                title, name = parts
            elif len(parts) == 1: 
                title, name = parts[0], ""
            else:
                continue
            formatted_lines.append(f"{title:<30}{name:>30}")
        label_text = "\n".join(formatted_lines)
        label.config(text=label_text, justify="left", font=("Courier", 12))


    global menu_frame
    menu_frame = tk.Frame(root)
    menu_frame.pack()

    settings_frame = tk.Frame(root)
    lb_frame = tk.Frame(root)
    title_frame = tk.Frame(root)

    logo_label = tk.Label(menu_frame, text="M I N E S W E E P E R", font=("DEBROSEE", 80, "bold"))
    logo_label.pack(pady=20)

    divisor_label = tk.Label(menu_frame, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", font=("DEBROSEE", 20, "bold"))
    divisor_label.pack()

    start_button = tk.Button(menu_frame, text="Start Game", width="15", font=("DEBROSEE", 14, "bold"), command=start_game)
    start_button.pack(pady=20)

    play_timed = tk.Button(menu_frame, text="Timed", width=15, font=("DEBROSEE", 14, "bold"), command=start_timed)
    play_timed.pack(pady=20)

    settings_button = tk.Button(menu_frame, text="Settings", width="15", font=("DEBROSEE", 14, "bold"), command=settings_menu)
    settings_button.pack(pady=10)

    leaderboard_button = tk.Button(menu_frame, text="Leaderboard", width="15", font=("DEBROSEE", 14, "bold"), command=lb_menu)
    leaderboard_button1 = tk.Button(lb_frame, text="Casual", width="15", font=("DEBROSEE", 14, "bold"), command=show_leaderboard)
    leaderboard_button1.pack(pady=10)
    leaderboard_button2 = tk.Button(lb_frame, text="Timed", width="15", font=("DEBROSEE", 14, "bold"), command=show_Tleaderboard)
    leaderboard_button2.pack(pady=10)
    leaderboard_button.pack(pady=10)

    titles_button = tk.Button(menu_frame, text="Titles", width="15", font=("DEBROSEE", 14, "bold"), command=display_titles)
    titles_button.pack(pady=10)

    exit_button = tk.Button(menu_frame, text="Exit", width="15", font=("DEBROSEE", 14, "bold"), command=exit_game)
    exit_button.pack(pady=10)
    
    options = ["Warm and Earthy", "Cool and Calming", "Vibrant and Energetic", "Soft and Pastel", "Dark and Moody"]
    difops = ["Easy", "Medium", "Hard"]#, "Extreme"]
    selected_option = tk.StringVar()
    selected_option_dif = tk.StringVar()
    selected_option.set(options[settings.chosen_set_id - 1])
    selected_option_dif.set(difops[int(settings.difficulty_level) - 1])

    style_label = tk.Label(settings_frame, text="Choose Style:", font=("DEBROSEE", 14))
    style_label.grid(row=0, column=0, sticky="w", padx=20)

    dropdown_menu = tk.OptionMenu(settings_frame, selected_option, *options, command=dropdown_selection_changed)
    dropdown_menu.config(font=("DEBROSEE", 12), width="40")
    dropdown_menu.grid(row=1, column=0, padx=20, pady=10)

    difficulty_label = tk.Label(settings_frame, text="Select Difficulty:", font=("DEBROSEE", 14))
    difficulty_label.grid(row=2, column=0, sticky="w", padx=20)

    dropdown_menu_dif = tk.OptionMenu(settings_frame, selected_option_dif, *difops, command=dropdown_menu_dif_func)
    dropdown_menu_dif.config(font=("DEBROSEE", 12), width="40")
    dropdown_menu_dif.grid(row=3, column=0, padx=20, pady=10)

    volume_label_title = tk.Label(settings_frame, text="Adjust Volume:", font=("DEBROSEE", 14))
    volume_label_title.grid(row=4, column=0, sticky="w", padx=20)

    initial_volume = settings.volume
    slider = ttk.Scale(settings_frame, from_=0, to=100, orient="horizontal", command=change_volume)
    slider.set(initial_volume * 100)
    slider.grid(row=5, column=0, padx=20, pady=10)

    volume_label = tk.Label(settings_frame, width=12, font="DEBROSEE")
    volume_label.config(text="Volume: {}%".format(int(initial_volume * 100)))
    volume_label.grid(row=5, column=1, padx=5)

    title_label = tk.Label(title_frame, text="M I N E S W E E P E R", font=("DEBROSEE", 60, "bold"))
    title_label.pack(pady=10)

    title_text = tk.Label(title_frame, text="", font=("DEBROSEE", 14, "bold"))
    load_titles_to_label(title_text, "titles.txt")
    title_text.pack()



    back_to_main_menu_button = tk.Button(settings_frame, text="Go back to Main Menu", width="20", font=("DEBROSEE", 14, "bold"), command=settings_menu_to_main_menu)
    back_to_main_menu_button.grid(row=6, column=0, padx=20, pady=20)
    back_to_main_menu_button2 = tk.Button(lb_frame, text="Go back to Main Menu", width="20", font=("DEBROSEE", 14, "bold"), command=lb_menu_to_main_menu)
    back_to_main_menu_button2.pack()
    back_to_main_menu_button3 = tk.Button(title_frame, text="Go back to Main Menu", width="20", font=("DEBROSEE", 14, "bold"), command=title_menu_to_main_menu)
    back_to_main_menu_button3.pack()


    global game_frame
    game_frame = tk.Frame(root)

    if(settings.fullscreen!=False):   
        root.attributes("-fullscreen", True)
    else:
        #root.geometry(settings.window_size)  
        window_width, window_height = map(int, settings.window_size.split('x'))
        x_position = (root.winfo_screenwidth() - window_width) // 2 
        y_position = 0 

        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


    global label
    label = tk.Label(root, text="")

    if(a==0):
        start_game()
        return 0
    if(a==2):
        start_timed()
        return 0

    game_frame.pack_forget()
    root.mainloop()

global mine_count
mine_count = settings.mine_count
play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 1)
