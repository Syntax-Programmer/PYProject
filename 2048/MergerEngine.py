import keyboard
from os import system
from time import sleep
from random import randrange, choice


class MovingLogic:
    """The magic number "4" is the number of rows/cols of the board."""

    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
        self.score = 0

    def Merger(self, list_to_merge: list[str], key_press: str) -> list[str]:
        """Merges similar elements of the row/cols."""
        """How TF it took me 2 weeks to make, WTF."""
        if len(list_to_merge) <= 1:
            return list_to_merge
        merged_list = []
        # The order of merging is reversed in these moves.
        iterated_list = list_to_merge[::-1] if key_press in "sd" else list_to_merge
        # Checks for and avoids double mergers of a single piece.
        last_merged = False
        for elem in iterated_list:
            if merged_list == []:
                merged_list.append(elem)
            elif elem != merged_list[-1] or last_merged:
                merged_list.append(elem)
                last_merged = False
            elif elem == merged_list[-1] and not last_merged:
                merged_list.pop(-1)
                merged_list.append(chr(ord(elem) + 1))
                self.score += 2 ** ((ord(elem) + 1) - 64)
                last_merged = True
        # Here the list is again reversed to make it like its original state.
        return merged_list[::-1] if key_press in "sd" else merged_list

    def HorizontalMoving(self, key_press: str) -> None:
        """Performs the horizontal moving."""
        row_elements = [
            [elem for elem in sub_row if elem != " "] for sub_row in self.board
        ]
        for row_index, sub_row in enumerate(row_elements[:]):
            row_elements[row_index] = self.Merger(
                list_to_merge=sub_row, key_press=key_press
            )
        # Using 'else' statement as exceptions are handled before the function is executed.
        self.board = (
            [[" " for _ in range(4 - len(row))] + row for row in row_elements]
            if key_press == "d"
            else [row + [" " for _ in range(4 - len(row))] for row in row_elements]
        )

    def VerticalMoving(self, key_press: str) -> None:
        """Performs the vertical moving."""
        col_elements = [
            [sub_row[index] for sub_row in self.board if sub_row[index] != " "]
            for index in range(4)
        ]
        for col_index, sub_col in enumerate(col_elements[:]):
            col_elements[col_index] = self.Merger(
                list_to_merge=sub_col, key_press=key_press
            )
        # Using 'else' statement as exceptions are handled before the function is executed.
        col = (
            [[" " for _ in range(4 - len(col))] + col for col in col_elements]
            if key_press == "s"
            else [col + [" " for _ in range(4 - len(col))] for col in col_elements]
        )
        self.board = [[sub_col[index] for sub_col in col] for index in range(4)]


class Board:
    def __init__(self, board: list[list[str]]) -> None:
        self.board = board

    def BoardUpdater(self) -> None:
        """Updates the board and handles loss conditions."""
        sleep(0.05)
        system("cls")
        print("+---+---+---+---+")
        for row_index in range(4):
            row = "|"
            for elements in range(4):
                row += f" {self.board[row_index][elements]} |"
            print(row)
            print("+---+---+---+---+")


class Main(MovingLogic, Board):
    def __init__(self) -> None:
        self.board = [
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ]
        super().__init__(board=self.board)

    def LossConditionChecker(self, board: list[list[str]]) -> bool:
        """Checks if the player has lost the game."""
        """True if the player has lost."""
        if any(" " in row for row in self.board):
            return False
        # How TF can a Normal && Sane person come up with this shit.
        # My Toxic trait says that this can be pulled off in a single any() statement.
        for row_index, sub_row in enumerate(board):
            for elem_index, elem in enumerate(sub_row):
                # WTF is this name. And I like it.
                indices_to_which_the_elem_can_merge_to = [
                    indices
                    for indices in [
                        (row_index, elem_index + 1),
                        (row_index, elem_index - 1),
                        (row_index - 1, elem_index),
                        (row_index + 1, elem_index),
                    ]
                    if all(num in range(4) for num in indices)
                ]
                if any(
                    board[indices[0]][indices[1]] == elem
                    for indices in indices_to_which_the_elem_can_merge_to
                ):
                    return False
        return True

    def GameLoop(self) -> None:
        """The main game loop."""
        # Adding a piece at a random place to begin the game.
        self.board[randrange(4)][randrange(4)] = choice(["A", "B"])
        self.BoardUpdater()
        print(f"Score = {0}")
        while True:
            if self.LossConditionChecker(board=self.board):
                print("Ha you lost")
                break
            key_press = keyboard.read_key().lower()
            # Used to check if the key pressed really changed the board by moving/merging. If not then no new piece shall be added.
            board_cache = self.board.copy()
            if key_press in "ad":
                self.HorizontalMoving(key_press=key_press)
            elif key_press in "ws":
                self.VerticalMoving(key_press=key_press)
            if board_cache == self.board or key_press not in "wasd":
                continue
            while True:
                sq_chosen = [randrange(4), randrange(4)]
                if self.board[sq_chosen[0]][sq_chosen[1]] == " ":
                    self.board[sq_chosen[0]][sq_chosen[1]] = choice(["A", "A", "B"])
                    break
            self.BoardUpdater()
            print(f"Score = {self.score}")
            sleep(0.3)
