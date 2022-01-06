class Tetris:
    def __init__(self, letter, m, n):
        self.letter = letter
        self.m = m  # m is the board width
        self.n = n  # n is the board height
        self.grid = ["-" for _ in range(self.m * self.n)]
        self.rotation = 0

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
        self.fill_out_grid(self.rotation)


    def down(self):
        # print(self.letters_dict[self.letter])
        # add try - except to handle textures ?
        new_value = [[int(x) + self.m for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value
        # print(self.letters_dict[self.letter])

    def move_left(self):
        new_value = [[int(x) - 1 for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value

    def move_right(self):
        new_value = [[int(x) + 1 for x in variant] for variant in self.letters_dict[self.letter]]
        self.letters_dict[self.letter] = new_value




    def move_it(self):
        self.print_grid()

        rotation = 0
        self.fill_out_grid(rotation)
        self.print_grid()
        self.reset_grid()


        while True:
            action = input("\n")
            # down - anyway
            self.down()
            if action == "exit":
                exit()

            elif action == "rotate":
                self.rotate()

            elif action == "down":
                self.fill_out_grid(self.rotation)

            elif action == "left":
                self.move_left()
                self.fill_out_grid(self.rotation)

            elif action == "right":
                self.move_right()
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
