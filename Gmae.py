import MS
import settings

def main():
    mine_count = settings.mine_count
    # Play Minesweeper with a 5x5 board and 5 mines
    MS.play_minesweeper(settings.board_size[0], settings.board_size[1], mine_count, 1)
