class Tetris:
    def __init__(self, letter, m, n):
        self.letter = letter
        self.m = m  # m is the board width
        self.n = n  # n is the board height
        self.grid = ["-" for _ in range(self.m * self.n)]
        self.rotation = 0
        self.border_points = {"left": [x for x in range(self.m * self.n) if x % self.m == 0],
                              "right": [x for x in range(self.m * self.n) if x % self.m == 9],
                              "bottom": [x for x in range(self.m * self.n - 1,  (self.m * self.n) - self.m - 1, -1)][::-1]
                              }


    @property
    def letter_coordinates(self):
        return self.letters_dict[self.letter][self.rotation]

    @staticmethod
    def set_dimmensions():
        try:
            dimensions = [int(x) for x in input().split()]
        except ValueError:
            print("Incorrect values provided")
            return Tetris.set_dimmensions()
        else:
            return dimensions[0], dimensions[1]

    letters_dict = {
        "O": [[4, 14, 15, 5]],
        "I": [[4, 14, 24, 34], [3, 4, 5, 6]],
        "S": [[5, 4, 14, 13], [4, 14, 15, 25]],
        "Z": [[4, 5, 15, 16], [5, 15, 14, 24]],
        "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
        "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
        "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
    }

    def print_grid(self):
        i = 0
        for _ in range(self.n):
            print(" ".join(self.grid[i:i + self.m]))
            i += self.m
        print()

    def fill_out_grid(self, rotation_variant):
        # use generator?:
        for y in self.letters_dict[self.letter][rotation_variant]:
            try:
                self.grid[y] = "0"
            except IndexError:
                pass

    def reset_grid(self):
        self.grid = ["-" for _ in range(self.m * self.n)]

    def print_piece(self):
        self.print_grid()

        current_rotation = 0
        while current_rotation != 4:
            for pos in range(len(self.letters_dict[self.letter])):
                self.fill_out_grid(pos)
                current_rotation += 1
                self.print_grid()
                self.reset_grid()

    def rotate(self):
        # print(len(self.letters_dict[self.letter]))
        if self.rotation + 1 <= len(self.letters_dict[self.letter]) - 1:
            self.rotation += 1
        else:
            self.rotation = 0
        # print("CURRENT SELF ROTATION", self.rotation)


    def down(self):
        if not self.is_valid_move(direction="bottom"):
            return

        new_value = [[int(x) + self.m for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value

    def move_left(self):
        if not self.is_valid_move(direction="left"):
            return

        new_value = [[int(x) - 1 for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value

    def move_right(self):
        if not self.is_valid_move(direction="right"):
            return

        new_value = [[int(x) + 1 for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value

    def is_valid_move(self, letter_coordinates=None, direction=None):
        if not letter_coordinates:
            letter_coordinates = self.letter_coordinates

        for coordinate in letter_coordinates:
            if coordinate in self.border_points[direction] or coordinate in self.border_points["bottom"]:  # this will cause block on the last offset
                return False
        return True

    def move_it(self):
        # print(self.border_points)

        # allow moving before figure hits the floor and block movement then.

        self.print_grid()

        rotation = 0
        self.fill_out_grid(rotation)
        self.print_grid()
        self.reset_grid()

        while True:
            action = input("\n")
            # self.down()


            if action == "exit":
                exit()
                """
        
            elif not self.is_valid_move(direction="bottom"):
                self.print_grid()
                """

            elif action == "rotate":
                new_rotation = self.rotation + 1 if self.rotation + 1 <= len(self.letters_dict[self.letter]) - 1 else 0
                if self.is_valid_move(letter_coordinates=self.letters_dict[self.letter][new_rotation], direction="left"):
                    if self.is_valid_move(letter_coordinates=self.letters_dict[self.letter][new_rotation], direction="right"):
                        self.rotate()
                else:
                    pass

            elif action == "down":
                pass

            elif action == "left":
                self.move_left()


            elif action == "right":
                self.move_right()


            # down - anyway
            self.down()
            self.fill_out_grid(self.rotation)
            self.print_grid()
            self.reset_grid()


def main():
    # while True:
    letter = input().strip().upper()
    if letter == "/exit":
        print("Bye bye!")
        exit()

    m, n = Tetris.set_dimmensions()
    game = Tetris(letter, m, n)
    # game.print_piece()
    game.move_it()


if __name__ == "__main__":
    main()
