# Game of life

import numpy as np
import tkinter as tk
from tkinter import messagebox
from time import sleep


class Gofengine:
    """ The engine of Game of Life. """

    def __init__(self):
        self._place = (np.zeros((100, 100))) != 0

    def show(self):                                 # not used because it has a GUI
        """ Print the world to the console """

        for row in self.place:
            for column in row:
                print('O', end='') if column else print('.', end='')
            print()
        print()

    def count_neighbor(self, row, column):
        """ Return the number of neighbours
            Input: row: int, column: int
            Output: int """

        count = self.place[row - 1: row + 2, column - 1: column + 2].sum()
        if self.place[row][column]: count -= 1

        return count

    def update_data(self):
        """ Play 1 life cycle and update the world"""

        new_place = np.copy(self.place)

        valid_rows = {i + j for i in sorted(set(self.life[0])) for j in [-1, 0, 1]}
        valid_columns = {i + j for i in sorted(set(self.life[1])) for j in [-1, 0, 1]}

        for row in valid_rows:
            for column in valid_columns:
                count = self.count_neighbor(row, column)
                if count == 3: new_place[row][column] = True
                elif count < 2 or count > 3: new_place[row][column] = False

        self.place = new_place

    def is_empty(self):
        if not self.place.sum(): return True
        return False

    def run(self):                                  # not used because it has a GUI
        """Run the game in the console """

        while True:
            self.resize_place()
            self.show()
            if self.is_empty(): break
            self.update_data()
            sleep(0.2)

    def resize_place(self):
        """ When life closes to the limit, expand the world """

        if min(self.life[0]) < 2: self.place = np.insert(self.place, 0, False, axis=0)
        if min(self.life[1]) < 2: self.place = np.insert(self.place, 0, False, axis=1)

        if max(self.life[0]) == self.place.shape[0] - 1: self.place = np.insert(self.place, self.place.shape[0], False, axis=0)
        if max(self.life[1]) == self.place.shape[1] - 1: self.place = np.insert(self.place, self.place.shape[1], False, axis=1)


    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, new_place):
        self._place = new_place

    @property
    def life(self):
        return np.where(self.place)

    @life.setter
    def life(self, coordinates):
        if coordinates[0] and coordinates[1]: self.place[coordinates[0], coordinates[1]] = True


class Gameoflife(Gofengine):
    """ An application is to animate the game of life"""

    def __init__(self):
        Gofengine.__init__(self)
        self._root = tk.Tk()
        self._root.title('Game of life')
        self._root.geometry('1200x900')
        self._root.resizable(False, False)

        self._pause = False
        self._round = 0

        self._world = tk.LabelFrame(self._root, text= 'World', height=880, width=1000)
        self._world.place(relx=0.01, rely=0.01)

        self._game_place = tk.Canvas(self._world, height=10000, width=1000, background='lightgray')
        self._game_place.place(relheight=1, relwidth=1)

        self._status = tk.LabelFrame(self._root, height=80, width=150, text='Status')
        self._status.place(relx=0.86, rely=0.01)
        self._status_text = tk.Label(self._status, font=('Arial', 15), text="Initialization")
        self._status_text.place(relx=0.1, rely=0.2)

        self._control = tk.LabelFrame(self._root, height=300, width=150, text='Control')
        self._control.place(relx=0.86, rely=0.15)

        tk.Button(self._control, width=11, font=('Arial', 15), text='Play', command=self.run_app).place(relx=0.04, rely=0.05)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Pause', command=self.pause).place(relx=0.04, rely=0.3)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Kill all', command=self.kill).place(relx=0.04, rely=0.55)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Exit', command=self._root.destroy).place(relx=0.04, rely=0.8)

        self._number_of_round = tk.LabelFrame(self._root, height=100, width=150, text='Round')
        self._number_of_round.place(relx=0.86, rely=0.75)
        self._number_of_round_text = tk.Label(self._number_of_round, font=('Arial', 20), text= 0)
        self._number_of_round_text.place(relx=0.2, rely=0.25)

        self._number_of_life = tk.LabelFrame(self._root, height=100, width=150, text='Population')
        self._number_of_life.place(relx=0.86, rely=0.875)
        self._number_of_life_text = tk.Label(self._number_of_life, font=('Arial', 20), text= 0)
        self._number_of_life_text.place(relx=0.2, rely=0.25)

        self._game_place.bind('<Button>', self.add_cell)

    def kill(self):
        """ Reset the place"""
        self.place = (np.zeros((100, 100))) != 0
        self._round = 0
        self._status_text.config(text='Extinction')
        self._status_text.update()

    def pause(self):

        self._pause = True

    def add_cell(self, event):

        self.life = (event.y//10, event.x//10)
        self.update_app()

    def draw_cell(self, column, row):

        self._game_place.create_oval(row-5, column-5, row+5, column+5, width=2, fill='red')

    def update_app(self):

        self._game_place.delete('all')
        self.resize_place()
        [self.draw_cell(i*10, j*10) for i, j in zip(self.life[0], self.life[1])]
        self._game_place.update()

    def run_app(self):
        """ Run the game in the interface """
        self._pause = False

        while True:
            self._round += 1
            if not self._place.sum(): break

            if self._pause:
                self._status_text.config(text='Pause')
                self._status_text.update()
                break

            self.update_app()
            self.update_data()

            self._number_of_round_text.config(text=self._round)
            self._number_of_round_text.update()

            self._number_of_life_text.config(text=self._place.sum())
            self._number_of_life_text.update()

            self._status_text.config(text='Run')
            self._status_text.update()

            if self.is_empty():

                self._round = 0
                self._status_text.config(text='Extinction')
                self._status_text.update()

                messagebox.showinfo(title="End", message="The life is over")
                break

            sleep(0.1)


if __name__ == "__main__":
    game = Gameoflife()

    game._root.mainloop()





