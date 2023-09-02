import tkinter as tk
from tkinter import ttk
from tkinter import *
import random
class Food:
    def __init__(self,master ,  x, y,  space_size=20, color = "red") -> None:
        self.coordinates =[x, y]
        master.create_rectangle(x,y,x+space_size, y+space_size, fill = color, tag ="food")
class Snake:
    def __init__(self,master, eat_funk = None,page= None,  body_size =3, space_size=20, color ="white" , speed =300) -> None:
        self.body_size =body_size
        self.coordinates = []
        self.squares = []
        self.space_size = space_size
        self.direction = 'down'
        self.master = master
        self.color = color
        self.speed = speed
        self.eat_funk = eat_funk
        self.page = page
        self.play= True

        for _ in range(self.body_size):
            self.coordinates.append((0,0))
            temp_square = self.master.create_rectangle(0,0, 0+self.space_size, 0+self.space_size, fill = self.color, tag = str((0,0)))
            self.squares.append(temp_square)
    
    def change_direction(self, new_direction):
        if new_direction == 'left':
            if self.direction != 'right':
                self.direction = new_direction
        elif new_direction == 'right':
            if self.direction != 'left':
                self.direction = new_direction
        elif new_direction == 'up':
            if self.direction != 'down':
                self.direction = new_direction
        elif new_direction == 'down':
            if self.direction != 'up':
                self.direction = new_direction
    
    def check_collision(self):
        x, y = self.coordinates[0]

        if x<0 or x>= self.master.winfo_reqwidth():
            return True
        elif y<0 or y>=self.master.winfo_reqheight():
            return True
        
        for body in self.coordinates[1:]: # coordinate itteration i start the itteration from the indices 1 the indices 0 is already in x and y
            if x== body[0] and y== body[1]:
                return True
        return False
    def move(self, F, eat_funk):
        if self.play:
            x, y = self.coordinates[0]

            if self.direction =='up':
                y -= self.space_size
            elif self.direction =='down':
                y += self.space_size

            elif self.direction == 'left':
                x-= self.space_size
            elif self.direction =='right':
                x += self.space_size
            else:
                raise ValueError(" dierection {} can't be decripted ".format(self.direction))
            self.coordinates.insert(0, (x, y))
            temp_square = self.master.create_rectangle(x,y,x+self.space_size, y+self.space_size, fill =self.color, tag = str((x, y)) )
            self.squares.append(temp_square)

            if x== F.coordinates[0] and y == F.coordinates[1]:
                # take 
                d = lambda : None
                if callable(eat_funk):
                    self.master.delete("food")
                    F = self.create_and_place_food()
                    eat_funk() # del f and create a new
                else:
                    pass
            else:
                id = self.coordinates[-1]
                del self.coordinates[-1]
                s =self.squares[0]
                self.master.delete(s)
                del self.squares[0]
                pass
            if self.check_collision():
                print('collis')
            else:
                self.page.after(self.speed, self.move,  F, self.eat_funk)
    
    def create_and_place_food(self):
        s_coordinates = str(self.coordinates)
        x = random.randint(0, int((self.master.winfo_reqwidth() / self.space_size)-1)) * self.space_size
        y = random.randint(0, int((self.master.winfo_reqheight() / self.space_size) - 1)) * self.space_size
        while True:
            if str([x,y]) in str(s_coordinates):
                x = random.randint(0, (self.master.winfo_reqwidth() / self.space_size)-1) * self.space_size
                y = random.randint(0, (self.master.winfo_reqheight() / self.space_size) - 1) * self.space_size
            else:
                break
        F = Food(self.master, x,y)
        return F
    def destroy(self):
        self.play = False
        self.master.delete('all')
        


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Snake Game")
        self.geometry("600x500")
        self.resizable(0,0)
        self.config(bg="black")
        self.update()
        self.bind('<Left>', lambda event: self.snake.change_direction('left'))
        self.bind('<Right>', lambda event: self.snake.change_direction('right'))
        self.bind('<Up>', lambda event: self.snake.change_direction('up'))
        self.bind('<Down>', lambda event: self.snake.change_direction('down'))

        self.bind('<a>', lambda event: self.snake.change_direction('left'))
        self.bind('<d>', lambda event: self.snake.change_direction('right'))
        self.bind('<w>', lambda event: self.snake.change_direction('up'))
        self.bind('<s>', lambda event: self.snake.change_direction('down'))
        self.start()
    def restart(self):
        try:
            self.snake.destroy()
            self.snake = Snake(self.canvas, page=self, eat_funk= lambda : self.update_score())
            self.food = self.snake.create_and_place_food()
            self.snake.move(self.food, lambda : self.update_score())
            self.score = 0
            self.level = 0
            self.score_label.config(text = f'Score : 000')
            self.level_label.config(text = f'Level : 0')
        except EXCEPTION as e:
            print(e)
            pass
    

    def start(self):

        try:
            for widget in self.winfo_children():
                widget.destroy()
        except:
            pass
        f= Frame(self, bg='black')
        f.pack(side = RIGHT, expand= False, padx=0, pady=0)

        self.score_label = Label(f, text = 'Score : 000', bg='black',fg='white', font= 'Lucida_Calligraphy, 20')
        self.score_label.pack( padx=0, pady=0)

        self.level_label = Label(f, text = 'Level : 0', bg='black',fg='white', font= 'Lucida_Calligraphy, 20')
        self.level_label.pack( padx=0, pady=0)

        Button(f, text= 'Restart', bg='black', fg='white', font= 'Lucida_Calligraphy, 20', border=0, command= self.restart).pack(fill=X)

        self.score =0
        self.level =0        
        self.canvas = Canvas(self, bg="black", height=450, width=400)
        self.canvas.pack(padx=0, pady=0, side = LEFT, expand = False)


        self.snake = Snake(self.canvas, page=self, eat_funk= lambda : self.update_score())
        self.food = self.snake.create_and_place_food()
        self.snake.move(self.food, lambda : self.update_score())

    def update_score(self):
        self.score +=1
        to_write = '000'
        to_write = to_write[len(str(self.score)):len(to_write)] +str(self.score)
        self.score_label.config(text = f'Score : {to_write}')
        if self.score % 5 == 0 and self.level !=5:
            self.snake.speed -=50
            self.level +=1
            self.level_label.config(text = f'Level : {self.level}')




if __name__ == '__main__':
    Gui().mainloop()