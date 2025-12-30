import settings
import MS
import tkinter as tk
import subprocess

def start_game():
    subprocess.Popen(["python", "MS.py"])

def exit_game(root):
    root.destroy()

# Create the main menu interface
root = tk.Tk()
root.title("Minesweeper Menu")

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=lambda: exit_game(root))
exit_button.pack(pady=5)

root.mainloop()
