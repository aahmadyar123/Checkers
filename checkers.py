"""
Aaron Ahmadyar
"""

import tkinter
import time


class Checkers(object):
    """
    A simple game of Checkers
    Instance Variables:
        self.window: The Tkinter window 
        self.reset: The reset button that restarts the game
        self.field: The Tkinter Canvas
        self.turn: an int the represents whose turn it is.  If number is negative, piece is a king.
        self.pieces: a 2D int array representing the board and the position of pieces. ex: self.pieces[y][x]
        self.click: initial click position of user in canvas
    """
    # Class Variables
    p1_color = 'gray20'
    p1_king_color = 'gray50'
    p2_color = 'DarkOrange2'
    p2_king_color = 'OrangeRed2'
    space_color1 = 'navajo white'
    space_color2 = 'saddle brown'
    # End Class Variables
    def __init__(self):
        """
        Initialize and setup the board
        """

        # Set up GUI
        self.window = tkinter.Tk()
        self.window.title("Checkers")
        self.reset = tkinter.Button(self.window, text = "Reset")
        self.field = tkinter.Canvas(self.window, width = 815, height = 800)

        # Pack Items in GUI
        self.reset.pack()
        self.field.pack()

        # Bind Buttons for GUI
        self.reset.bind("<Button-1>", self.__reset__)
        self.field.bind("<Button-1>", self.__click__)
        self.field.bind("<ButtonRelease-1>", self.__release__)

        # Sets pieces and resets the game.  __reset__() expects an event argument so I used None
        self.__reset__(None)

    def __reset__(self, event):
        """
        Resets the board and gets ready a new game
        :param event: a tkinter event when user clicks the reset button.  Even is never used though.
        :return: None
        """
        # Delete everything on Canvas
        all_items = self.field.find_all()
        for item in all_items:
            self.field.delete(item)

        # Create 8 by 8 2d array with every element set to 0
        self.pieces = [[0 for y in range(8)] for x in range(8)]

        # Color Checker Board
        for y in range(0, 8):
            for x in range(0, 8):
                if (x + y) % 2 == 0:
                    color = Checkers.space_color1
                else:
                    color = Checkers.space_color2
                self.field.create_rectangle(x * 100, y * 100, x * 100 + 99, y * 100 + 99, fill=color)

        # setting up turn indicators
        self.field.create_rectangle(800, 0, 815, 399, fill = 'white' )
        self.field.create_rectangle(800, 400, 815, 799, fill = Checkers.p1_color )

        # Checker board top and left border lines would not show.  I just manually drew lines to fix it
        self.field.create_line(2, 2, 2, 800)
        self.field.create_line(2, 2, 815, 2)

        # setting up checker pieces for player 1
        for y in range(5, 8):
            for x in range(0, 8):
                if (x+y) % 2 == 1:
                    self.field.create_oval((x * 100) + 20, (y * 100) + 20, (x * 100) + 80, (y * 100) + 80, fill=Checkers.p1_color)
                    self.pieces[y][x] = 1

        # setting up checker pieces for player 2
        for y in range(0, 3):
            for x in range(0, 8):
                if (x + y) % 2 == 1:
                    self.field.create_oval((x*100)+20, (y*100)+20, (x*100)+80, (y*100)+80, fill=Checkers.p2_color)
                    self.pieces[y][x] = 2
        self.click = ()
        self.turn = 1

    def __click__(self, event):
        """
        The function that gets executed when a user clicks on the board
        :param event: The event that contains the coordinates of the click
        :return: None
        """
        self.click = (int(event.x / 100), int(event.y / 100))

    def __release__(self, event):
        """
        Release is executed whenever the user lets go of the mouse button.
        This method checks if movement is valid, and if it is it calls piece movement to move the piece
        :param event: Mouse Button 1 Release
        :return:
        """
        # Save start and end coordinates
        x1 = self.click[0]
        y1 = self.click[1]
        x2 = int(event.x / 100)
        y2 = int(event.y / 100)

        # Reset click variable
        self.click = ()

        # Check valid move
        if not self.__is_valid_move__(x1, y1, x2, y2):
            return

        # Move piece
        dub_jump = self.__piece_movement__(x1, y1, x2, y2)

        # Return to avoid changing turns
        if dub_jump:
            return

        # Change turns
        if self.__game_over__():
            self.turn == 0
        elif self.turn == 1:
            self.turn = 2
            self.field.itemconfigure(self.field.find_closest(807,200), fill = Checkers.p2_color)
            self.field.itemconfigure(self.field.find_closest(807,600), fill = 'white')
        elif self.turn == 2:
            self.turn = 1
            self.field.itemconfigure(self.field.find_closest(807,600), fill = Checkers.p1_color)
            self.field.itemconfigure(self.field.find_closest(807,200), fill = 'white')

    def __piece_movement__(self, x1, y1, x2, y2):
        kill = False

        # Visually Move the Piece
        piece = self.field.find_closest(x1 * 100 + 50, y1 * 100 + 50)
        self.field.move(piece, 100*(x2-x1), 100*(y2-y1))

        # Check if piece kills
        if abs(x2-x1) == 2:
            kill = True
            enemy = self.field.find_closest(100*int((x2+x1)/2)+50, 100*int((y2+y1)/2)+50)
            self.field.delete(enemy)
            self.pieces[int((y2+y1)/2)][int((x2+x1)/2)] = 0

        # Update representation of checkers board
        self.pieces[y2][x2] = self.pieces[y1][x1]
        self.pieces[y1][x1] = 0

        # Check for kings
        self.__king_me__()

        # Return True if the player can double jump, otherwise False
        if kill and self.__can_piece_kill__(x2, y2, False if self.pieces[y2][x2] == self.turn else True):
            return True
        return False

    def __king_me__(self):
        for x in range(8):
            if self.pieces[0][x] == 1:
                self.pieces[0][x] = -1
                piece = self.field.find_closest(x*100 + 50, 50)
                self.field.itemconfigure(piece, fill=Checkers.p1_king_color)
        for x in range(8):
            if self.pieces[7][x] == 2:
                self.pieces[7][x] = -2
                piece = self.field.find_closest(x * 100 + 50, 750)
                self.field.itemconfigure(piece, fill=Checkers.p2_king_color)

    def __is_valid_move__(self, x1, y1, x2, y2):
        """
        Checks if user's move is valid or not
        :param x1: coordinate point
        :param y1: coordinate point
        :param x2: coordinate point
        :param y2: coordinate point
        :return: Boolean
        """

        # Basic error checking
        if x1 < 0 or x1 >= 8 or \
           y1 < 0 or x1 >= 8 or \
           x2 < 0 or x2 >= 8 or \
           y2 < 0 or y2 >= 8:
            return False
        # make sure piece belongs to player
        if self.pieces[y1][x1] != self.turn and \
           self.pieces[y1][x1] != self.turn*-1:
            return False

        # make sure landing space is empty
        if self.pieces[y2][x2] != 0:
            return False
        # Set direction piece is moving
        enemy = 10
        move = 0
        if self.turn == 1:
            move = -1
            enemy = 2
        if self.turn == 2:
            move = 1
            enemy = 1
        # Check if Player is trying to kill as either a normal piece or a king
        if x2 == x1+2 or x2 == x1-2:
            # Normal Piece
            if y2 == y1 + 2 * move:
                if abs(self.pieces[int((y2+y1)/2)][int((x2+x1)/2)]) == enemy:
                    return True
            # King Piece
            if self.pieces[y1][x1] == self.turn * -1 and y2 == y1-2*move:
                if abs(self.pieces[int((y2 + y1) / 2)][int((x2 + x1) / 2)]) == enemy:
                    return True
        # The checkers piece must kill if given the chance.
        if self.__can_player_kill__():
            return False
        # Check scenario where piece is trying to move
        if (x2 == x1+1 or x2 == x1-1) and y2 == y1+move:
            return True

        # check scenario where king piece is trying to move
        if self.pieces[y1][x1] == self.turn * -1 and y2 == y1-move and (x2 == x1+1 or x2 == x1-1):
            return True
        # move was not valid return False
        return False

    def __can_player_kill__(self):
        """
        This function will loop over every piece and check to see if it is capable of taking an enemy chip
        :return: Boolean
        """
        for x in range(8):
            for y in range(8):
                if self.pieces[y][x] == self.turn:
                    if self.__can_piece_kill__(x, y, False):
                        return True
                if self.pieces[y][x] == -1 * self.turn:
                    if self.__can_piece_kill__(x, y, True):
                        return True
        return False

    def __can_piece_kill__(self, x, y, king):
        """
        This function will check if an individual checker's piece can bring himself to kill an enemy
        :param x: the x-coorinate of the piece
        :param y: the y-coordinate of the piece
        :param king: boolean value whether the piece is a king or not
        :return: Boolean
        """
        enemy = 10
        move = 0
        if self.turn == 1:
            enemy = 2
            move = -1
        if self.turn == 2:
            enemy = 1
            move = 1

        if x + 2 < 8 and 0 <= y + 2*move < 8:
            if abs(self.pieces[y+move][x+1] == enemy) and (self.pieces[y + 2*move][x+2] == 0):
                return True

        if x - 2 >= 0 and 0 <= y + 2*move < 8:
            if abs(self.pieces[y+move][x-1]) == enemy and self.pieces[y + 2 * move][x - 2] == 0:
                return True

        # movement for king pieces

        if king:
            if x + 2 < 8 and 0 <= y - 2 * move < 8:
                if abs(self.pieces[y - move][x + 1]) == enemy and self.pieces[y - 2 * move][x + 2] == 0:
                    return True
            if x - 2 >= 0 and 0 <= y - 2 * move < 8:
                if abs(self.pieces[y - move][x - 1]) == enemy and self.pieces[y - 2 * move][x - 2] == 0:
                    return True
        return False

    def __game_over__(self):
        """
        Is the game over?
        :return: Boolean
        """
        p1_exists = False
        p2_exists = False

        # Check if players have pieces on board
        for y in range(0, 8):
            for x in range(0, 8):
                if abs(self.pieces[y][x]) == 1:
                    p1_exists = True
                if abs(self.pieces[y][x]) == 2:
                    p2_exists = True

        if (p1_exists or p2_exists) and not (p1_exists and p2_exists):
            if p1_exists and not p2_exists:
                winner_color = Checkers.p1_color
            elif p2_exists and not p1_exists:
                winner_color = Checkers.p2_color

            # Set turn indicator to winner
            self.field.itemconfigure(self.field.find_closest(807,200), fill=winner_color)
            self.field.itemconfigure(self.field.find_closest(807,600), fill=winner_color)


            
            spaces = set()
            for y in range(0,8):
                for x in range(0,8):
                    if self.pieces[y][x] == 0:
                        spaces.add((y,x))
                        
            for num in range(len(spaces)):
                location = spaces.pop()
                y = location[0]
                x = location[1]
           
                self.field.create_oval((x * 100) + 20, (y * 100) + 20, (x * 100) + 80, (y * 100) + 80, fill=winner_color)
                time.sleep(.125)
                self.field.update_idletasks()
            return True
        return False


def main():
    game = Checkers()
    game.window.mainloop()


if __name__ == "__main__":
    main()