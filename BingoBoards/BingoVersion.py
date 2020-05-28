from BingoBoards.util.dir import dir
from BingoBoards.util.FileReader import FileReader
import numpy as np
import zipfile
import os


TEMPORARY_DIR = 'BingoBoards/TEMP'
ROW_IDS = np.array(['row1', 'row2', 'row3', 'row4', 'row5', 'col1', 'col2', 'col3', 'col4', 'col5', 'tlbr', 'bltr'])

ROW_INDICES = {'row1': [0, 1, 2, 3, 4], 'row2': [5, 6, 7, 8, 9], 'row3': [10, 11, 12, 13, 14],
               'row4': [15, 16, 17, 18, 19], 'row5': [20, 21, 22, 23, 24], 'col1': [0, 5, 10, 15, 20],
               'col2': [1, 6, 11, 16, 21], 'col3': [2, 7, 12, 17, 22], 'col4': [3, 8, 13, 18, 23],
               'col5': [4, 9, 14, 19, 24], 'tlbr': [0, 6, 12, 18, 24], 'bltr': [4, 8, 12, 16, 20]}


class BingoVersion:
    goal_list = {}
    boards = []

    def __init__(self, version):

        if not os.path.isfile(f'BingoBoards/Versions/{version}.bingo'):
            raise ValueError(f"'{version}' is not a supported version.")

        reader = FileReader()

        with zipfile.ZipFile(f'BingoBoards/Versions/{version}.bingo', 'a') as zip_file:
            zip_file.extractall('BingoBoards')

        self.goal_list = np.load(TEMPORARY_DIR + '/goal_list.npy', allow_pickle=True).item()
        board_string = reader.file_to_string(TEMPORARY_DIR + '/boards.txt')

        #dir.rm(TEMPORARY_DIR)

        self.boards = board_string.split('\n')

    def get_board(self, seed):

        if seed < 0 or seed > 1e6 or not isinstance(seed, int):
            raise ValueError(f"'{str(seed)}' is not a valid seed.")

        board = self.boards[seed].split(' ')

        for i in range(len(board)):
            board[i] = self.goal_list[board[i]]

        return board

    def get_row(self, seed, row_id):
        if row_id not in ROW_IDS:
            raise ValueError(f"'{row_id}' is not a valid Row ID.")

        row_ids = ROW_INDICES[row_id]
        board = self.get_board(seed)
        goals = [board[id] for id in row_ids]

        return goals
