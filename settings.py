# Define and manage global settings for the Minesweeper game
def parse_color_sets(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    set1 = []
    set2 = []
    set3 = []
    set4 = []
    set5 = []
    set6 = []
    set7 = []
    set8 = []
    current_set = None

    for line in lines:
        line = line.strip()
        if line.startswith("Set 1"):
            current_set = set1
        elif line.startswith("Set 2"):
            current_set = set2
        elif line.startswith("Set 3"):
            current_set = set3
        elif line.startswith("Set 4"):
            current_set = set4
        elif line.startswith("Set 5"):
            current_set = set5
        elif line.startswith("Set 6"):
            current_set = set6
        elif line.startswith("Set 7"):
            current_set = set7
        elif line.startswith("Set 8"):
            current_set = set8
        elif line.startswith("#"):
            color_code = line.split()[0]
            current_set.append(color_code)

    return set1, set2, set3, set4, set5, set6, set7, set8

def set_color(new_id):

    set_map = {
        1: set1,
        2: set2,
        3: set3,
        4: set4,
        5: set5
    }
    chosen_set = set_map.get(new_id, "set1")
    return chosen_set

def return_dif(dl):
    return dl

def return_ws(ws):
    return ws

def update_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("dif"):
            global difficulty_level
            difficulty_level = return_dif(line.strip().split('=')[1])

        elif line.startswith("setid"):
            global chosen_set_id
            chosen_set_id = int(line.strip().split('=')[1])

        elif line.startswith("ws"):
            # Find the position of the first double quote (")
            start_index = line.find('"')
            # Find the position of the last double quote (") starting from the end of the string
            end_index = line.rfind('"')
            
            global window_size
            window_size = return_ws(line[start_index + 1:end_index])

        elif line.startswith("mc"):
            global mcb
            mcb=True
            global mine_count
            mine_count = int(line.strip().split('=')[1])

        elif line.startswith("volume"):
            global volume
            volume = float(line.strip().split('=')[1])

file_path = 'colorsets.txt'
set1, set2, set3, set4, set5, set6, set7, set8 = parse_color_sets(file_path)
set_path = 'setts.txt'

chosen_set_id=0
difficulty_level=0
mcb=False
window_size="0x0"
volume = 0
chosen_set = set_color(chosen_set_id)

update_data(set_path)
print(volume)
chosen_set = set_color(chosen_set_id)


if(difficulty_level == "1"):
    board_size=10,10
    if(mcb==False):
        mine_count = 10
elif(difficulty_level == "2"):
    board_size=20,20
    if(mcb==False):
        mine_count=20
elif(difficulty_level == "4"):
    board_size=50,50
    if(mcb==False):
        mine_count=100
else:
    board_size=30,30
    if(mcb==False):
        mine_count=30

fullscreen=False
