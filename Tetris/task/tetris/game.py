class Tetris:

    def __init__(self, letter, m, n):
        self.letter = letter
        self.letters_dict = {}
        self.m = m  # m is the board width
        self.n = n  # n is the board height
        self.grid = ["-" for _ in range(self.m * self.n)]
        self.rotation = 0
        self.border_points = {"left": [x for x in range(self.m * self.n) if x % self.m == 0],
                              "right": [x for x in range(self.m * self.n) if x % self.m == 9],
                              "bottom": [x for x in range(self.m * self.n - 1, (self.m * self.n) - self.m - 1, -1)][
                                        ::-1]
                              }
        self.static_cells = []

    @property
    def letter_coordinates(self):
        return self.letters_dict[self.letter][self.rotation]

    @classmethod
    def from_string(cls):
        def get_figure():
            _letter = input().strip().upper()
            if _letter == "/EXIT":
                print("Bye bye!")
                exit()
            elif _letter not in 'OISZLJT':
                print("Invalid letter, please choose among 'O' 'I' 'S' 'Z''L' 'J' 'T'")
                return Tetris.from_string()
            return _letter

        def set_dimmensions():
            try:
                dimensions = [int(x) for x in input().split()]
            except ValueError:
                print("Incorrect values provided")
                return set_dimmensions()
            else:
                return dimensions[0], dimensions[1]

        letter = get_figure()
        m, n = set_dimmensions()

        return cls(letter, m, n)

    def reset_dict(self):
        self.letters_dict = {
            "O": [[4, 14, 15, 5]],
            "I": [[4, 14, 24, 34], [3, 4, 5, 6]],
            "S": [[5, 4, 14, 13], [4, 14, 15, 25]],
            "Z": [[4, 5, 15, 16], [5, 15, 14, 24]],
            "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
            "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
            "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
        }

    def place_first_letter(self):
        self.fill_out_grid()
        self.print_grid()
        self.reset_grid()

    def print_grid(self):
        i = 0
        for _ in range(self.n):
            print(" ".join(self.grid[i:i + self.m]))
            i += self.m
        print()

    def fill_out_grid(self, ):
        if self.static_cells:
            for cell in self.static_cells:
                self.grid[cell] = "0"

        # use generator?:
        for y in self.letters_dict[self.letter][self.rotation]:
            try:
                self.grid[y] = "0"
            except IndexError:
                pass

    def reset_grid(self):
        self.grid = ["-" for _ in range(self.m * self.n)]

    def rotate(self):
        # creating back up
        current_rotation = self.rotation
        # rotate
        self.rotation += 1 if (
                self.rotation + 1 <= len(self.letters_dict[self.letter]) - 1 or self.rotation == -1) else 0
        # validate
        if not all([self.is_valid_move(direction="left"), self.is_valid_move(direction="right")]):
            # undo if validation failed
            self.rotation = current_rotation

    def move(self, direction):  # it was left
        direction = "bottom" if direction == "down" else direction
        # +1 if moving right, -1 if moving left.
        offset = {"left": -1, "right": +1, "bottom": self.m}[direction]

        if not self.is_valid_move(direction=direction):
            return

        new_value = [[int(x) + offset for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value

    def is_valid_move(self, direction=None):
        for coordinate in self.letter_coordinates:
            if coordinate in self.border_points[direction] or coordinate in self.static_cells or coordinate in \
                    self.border_points["bottom"]:
                return False
        return True

    def make_static(self):
        # or coodinate is ON static cell. - make it static
        static = False
        for coordinate in self.letter_coordinates:
            if coordinate in self.border_points["bottom"] or coordinate in [x - self.m for x in self.static_cells]:
                static = True
                break

        print(f"Static now is:{static}")
        if static:
            for coordinate in self.letter_coordinates:
                self.static_cells.append(coordinate)
            # self.letter = choice(list(self.letters_dict.keys()))

    def game_over(self):
        return "Full grid condition"

    def drop_row(self):
        control_row = ["-" for _ in range(self.m)]
        last_index = self.m * self.n
        l1 = last_index - self.m
        bottom_row = self.grid[last_index:l1:-1]

        print(bottom_row == last_index)  # IT WORKS!

    def move_it(self):
        while True:
            # add match case?
            action = input("\n")
            if action == "exit":
                exit()

            elif action == "rotate":
                self.rotate()

            elif action == "down":
                pass

            elif action in {"left", "right"}:
                self.move(action)

            elif action == "break":
                self.fill_out_grid()  # for test only
                self.drop_row()
                self.reset_grid()  # for test only

            elif action == "piece":
                self.reset_dict()
                self.letter = input().strip().upper()
                self.rotation = 0
                print("LETTER ADDED", self.letter)
                print("Current letter coordinates:", self.letter_coordinates)
                self.place_first_letter()
                return self.move_it()

                # self.print_grid()
                # the bug is that after all manipulations with the piece, it's final coordinates will be in static_moves. It makes sence to reset original letters coordinates
            else:
                print("Invalid option. Try any of the following options\n'left', 'right', 'down', 'rotate', 'exit': ")
                return self.move_it()

            # down - anyway
            self.move("down")
            self.make_static()
            self.fill_out_grid()
            self.print_grid()
            self.reset_grid()


def main():
    game = Tetris.from_string()
    game.reset_dict()

    game.print_grid()
    game.place_first_letter()
    game.move_it()


if __name__ == "__main__":
    main()
