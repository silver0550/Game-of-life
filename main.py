# Game of life

import numpy as np
import tkinter as tk
from tkinter import messagebox
from time import sleep


class Gofengine:

    def __init__(self):
        self._place = (np.zeros((100, 100))) != 0

    def show(self):
        for row in self._place:
            for column in row:
                print('O', end='') if column else print('.', end='')
            print()
        print()

    def count_neighbor(self, row, column):

        count = self._place[row-1:row+2, column-1:column+2].sum()
        if self._place[row][column]: count -= 1

        return count

    def update_data(self):

        new_place = np.copy(self._place)

        self.valid_rows = {i + j for i in sorted(set(self.life[0])) for j in [-1, 0, 1]}
        self.valid_columns = {i + j for i in sorted(set(self.life[1])) for j in [-1, 0, 1]}

        for row in self.valid_rows:
            for column in self.valid_columns:
                count = self.count_neighbor(row, column)
                if count == 3: new_place[row][column] = True
                elif count < 2 or count > 3: new_place[row][column] = False

        self._place = new_place

    def is_empty(self):
        if not self._place.sum(): return True
        return False

    def run(self): # nincs rá szükség
        while True:

            self.resize_place()
            self.show()
            if self.is_empty(): break
            self.update_data()
            sleep(0.5)

    def resize_place(self):
        if min(self.life[0]) == 1: self._place = np.insert(self._place, 0, 0, axis=0)
        if min(self.life[1]) == 1: self._place = np.insert(self._place, 0, 0, axis=1)

        if max(self.life[0]) == self._place.shape[0] - 1: self._place = np.insert(self._place, self._place.shape[0], 0, axis=0)
        if max(self.life[1]) == self._place.shape[1] - 1: self._place = np.insert(self._place, self._place.shape[1], 0, axis=1)


    @property
    def life(self):
        return np.where(self._place)

    @life.setter
    def life(self, cordinates):
        #TODO: input check
        self._place[cordinates[0], cordinates[1]] = True


class Gameoflife(Gofengine):

    def __init__(self):
        Gofengine.__init__(self)
        self._root = tk.Tk()
        self._root.title('Game of life')
        self._root.geometry('1200x900')
        self._root.resizable(False, False)

        self._pause = False

        self._world = tk.LabelFrame(self._root, text= 'World', height=880, width=1000)
        self._world.place(relx=0.01, rely=0.01)

        self._game_place = tk.Canvas(self._world, background='lightgray')
        self._game_place.place(relheight=1, relwidth=1)

        # self._vizszint = tk.Scrollbar(self._game_place)
        # self._vizszint.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # t = tk.Text(self._game_place, width=500, height=200, wrap=tk.NONE, yscrollcommand=self._vizszint.set)
        # [t.insert(tk.END, "this is some text\n") for _ in range(20)]
        #
        # t.pack(side=tk.TOP, fill= tk.X)
        #
        # self._vizszint.config(command=t.yview)


        self._status = tk.LabelFrame(self._root, height=80, width=150, text='Status')
        self._status.place(relx=0.86, rely=0.01)
        self._status_text = tk.Label(self._status, font=('Arial', 15), text="Initialization")
        self._status_text.place(relx=0.1, rely=0.2)

        self._control = tk.LabelFrame(self._root, height=300, width=150, text='Control')
        self._control.place(relx=0.86, rely=0.15)

        tk.Button(self._control, width=11, font=('Arial', 15), text='Play', command=self.run_app).place(relx=0.04, rely=0.05)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Pause', command=self.pause).place(relx=0.04, rely=0.3)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Abort').place(relx=0.04, rely=0.55)
        tk.Button(self._control, width=11, font=('Arial', 15), text='Exit', command=self._root.destroy).place(relx=0.04, rely=0.8)

        self._number_of_round = tk.LabelFrame(self._root, height=100, width=150, text='Round')
        self._number_of_round.place(relx=0.86, rely=0.75)
        self._number_of_round_text = tk.Label(self._number_of_round, font=('Arial', 20), text='0')
        self._number_of_round_text.place(relx=0.2, rely=0.25)

        self._number_of_life = tk.LabelFrame(self._root, height=100, width=150, text='Population')
        self._number_of_life.place(relx=0.86, rely=0.875)
        self._number_of_life_text = tk.Label(self._number_of_life, font=('Arial', 20), text='0')
        self._number_of_life_text.place(relx=0.2, rely=0.25)

        self._game_place.bind('<Button>', self.add_cell)

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
        self._pause = False
        self.round = 0
        while True:
            self.round += 1
            if not self._place.sum(): break
            if self._pause:
                self._status_text.config(text='Pause')
                self._status_text.update()
                break
            self.update_app()
            self.update_data()

            self._number_of_round_text.config(text=self.round)
            self._number_of_round_text.update()

            self._number_of_life_text.config(text=self._place.sum())
            self._number_of_life_text.update()

            self._status_text.config(text='Run')
            self._status_text.update()

            if self.is_empty():
                messagebox.showinfo(title="End", message="A teljes populáció kihalt!")
                self._status_text.config(text='Stop')
                self._status_text.update()
                break
            sleep(0.1)


if __name__ == "__main__":
    game = Gameoflife()

    game._root.mainloop()





