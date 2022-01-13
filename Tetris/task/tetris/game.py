class Tetris:

    def __init__(self, m, n):
        self.letter = None
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
        self.static_cells = set()

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

    @property
    def letter_coordinates(self):
        return self.letters_dict[self.letter][self.rotation]

    @classmethod
    def from_string(cls):
        def set_dimmensions():
            try:
                dimensions = [int(x) for x in input().split()]
            except ValueError:
                print("Incorrect values provided")
                return set_dimmensions()
            else:
                return dimensions[0], dimensions[1]

        m, n = set_dimmensions()

        return cls(m, n)

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

        if self.letter:
            for y in self.letters_dict[self.letter][self.rotation]:
                try:
                    self.grid[y] = "0"
                except IndexError:
                    pass

    def reset_grid(self):
        self.grid = ["-" for _ in range(self.m * self.n)]

    def rotate(self):
        # creating back up

        # rotate
        self.rotation += 1 if (
                self.rotation + 1 <= len(self.letters_dict[self.letter]) - 1 or self.rotation == -1) else 0
        # validate
        if not all([self.is_valid_move(direction="left"), self.is_valid_move(direction="right")]):
            # undo if validation failed
            self.rotation -= 1

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
            if coordinate in self.border_points[direction] or coordinate in self.static_cells \
                    or coordinate in self.border_points["bottom"]:
                return False
        return True

    def make_static(self):
        # or coodinate is ON static cell. - make it static
        static = False
        if self.letter:
            in_border_points = lambda x: x in self.border_points["bottom"] or x in [x - self.m for x in self.static_cells]

            hit_the_border = [coordinate for coordinate in self.letter_coordinates if in_border_points(coordinate)]
            if hit_the_border:
                for coordinate in self.letter_coordinates:
                    self.static_cells.add(coordinate)
                self.letter = None  # need to clear letter coordinates once it became static

    def game_end_check(self):
        # print("currently the following cells are static:", self.static_cells)
        for cell in self.static_cells:
            if cell in [x for x in range(self.m)]:
                print("Game Over!")
                exit()

    def drop_row(self):
        def recalculate_static_cells():
            self.static_cells = list(self.static_cells)

            # iterating over the static cells to recalculate
            for cell in range(len(self.static_cells)):
                # avoiding overwritting of occupied static cells
                if self.static_cells[cell] + self.m <= self.m * self.n - 1 and self.static_cells[cell] + self.m not in self.static_cells:
                    # pushing top cells down to be on bottom level of grid or static cells.
                    self.static_cells[cell] += self.m
            self.static_cells = set(self.static_cells)

        self.fill_out_grid()
        original_static_capacity = len(self.static_cells)

        i = 0
        for _ in range(self.n):
            row = self.grid[i:i + self.m]
            row_indexes = [x for x in range(i, i + self.m)]

            if row == ["0" for _ in range(self.m)]:
                for cell_index in row_indexes:
                    self.static_cells.remove(cell_index)
            i += self.m

        if original_static_capacity != len(self.static_cells):
            recalculate_static_cells()

        self.reset_grid()

    def move_it(self):
        while True:
            action = input("\n")
            match action:

                case "exit":
                    exit()

                case "rotate":
                    self.rotate()
                    self.move("down")

                case "down":
                    if self.letter:
                        self.move("down")

                case "left" | "right":  # "|" == "or"
                    self.move(action)
                    self.move("down")

                case "break":
                    self.drop_row()

                case "piece":
                    self.reset_dict()
                    self.letter = input().strip().upper()
                    self.rotation = 0

                case _:
                    print("Invalid option.\nPossible options: 'left', 'right', 'down', 'rotate', 'exit': ")
                    return self.move_it()

            self.fill_out_grid()
            self.make_static()

            self.print_grid()
            if action != "piece":
                self.game_end_check()
            self.reset_grid()


def main():
    game = Tetris.from_string()
    game.reset_dict()

    game.print_grid()

    game.move_it()


if __name__ == "__main__":
    main()
