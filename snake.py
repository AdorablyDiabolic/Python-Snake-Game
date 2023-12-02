# Import necessary modules 
from tkinter import *
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 80
SPACE_SIZE = 25
BODY_PARTS = 7
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


# Function to start the game
def start_game():
    global start_screen
    start_screen.destroy()  # Destroy the start screen
    snake = Snake()
    food = Food()
    next_turn(snake, food)  # Start the game loop

# Create a function to display the start screen
def display_start_screen():
    global start_screen
    start_screen = Tk()
    start_screen.title("Snake Game")
    start_screen.resizable(False, False)
    
    # Calculate the window's position to center it on the screen
    screen_width = start_screen.winfo_screenwidth()
    screen_height = start_screen.winfo_screenheight()
    window_width = 400
    window_height = 300
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    start_screen.geometry(f"{window_width}x{window_height}+{x}+{y}")

    start_label = Label(start_screen, text="Welcome to Snake Game!", font=('Arial', 20))
    start_label.pack(pady=30)

    instructions_label = Label(start_screen, text="Use arrow keys to control the snake.\nEat the red food to grow.", font=('Arial', 12))
    instructions_label.pack(pady=10)

    start_button = Button(start_screen, text="Start Game", font=('Arial', 14), command=start_game)
    start_button.pack(pady=20)

    start_screen.mainloop()

# Call the function to display the start screen when the script starts
display_start_screen()

class Snake: # Create Snake and Food objects

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self): # Store the reference to the food square
        self.food_list = []  # List to hold multiple food coordinates

        for _ in range(3):  # Create three initial food items
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.food_list.append([x, y])

            self.coordinates = [x, y]

            #Create the food square on the canvas
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    global score
    global BODY_PARTS
    #global SPEED 

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
        if y < 0:
            y = GAME_HEIGHT - SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
        if y >= GAME_HEIGHT:
            y = 0
    elif direction == "left":
        x -= SPACE_SIZE
        if x < 0:
            x = GAME_WIDTH - SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        if x >= GAME_WIDTH:
            x = 0
            
    # collral the snake, make sure it dosent go off screesn 
    #if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        #game_over()
        #return

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        BODY_PARTS += 1 # add 1 to body part when food is eaten

        label.config(text="Score: {}".format(score))

        canvas.delete("food")

        food = Food()

        #window.after(SPEED, next_turn, snake, food)


    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

    # Check for collision with each food item
    for f in food.food_list:
        if x == f[0] and y == f[1]:
            score += 1
            label.config(text="Score: {}".format(score))
            canvas.delete("food")
            food.food_list.remove(f)  # Remove the eaten food
            food.food_list.append([random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE,
                                   random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE])
            for new_food in food.food_list:
                canvas.create_oval(new_food[0], new_food[1], new_food[0] + SPACE_SIZE, new_food[1] + SPACE_SIZE,
                                   fill=FOOD_COLOR, tag="food")
            break  # Exit loop after finding collision with one food item


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('Arial',70), text="GAME OVER", fill="red", tag="gameover")
    
    # Create a restart button
    restart_button = Button(window, text="Restart", font=('Arial', 14), command=restart_game)
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100, window=restart_button, tags="restart_button")

def restart_game():
    global score, direction, BODY_PARTS, snake, food
    score = 0
    direction = 'down'
    BODY_PARTS = 7
    label.config(text="Score: {}".format(score))
    canvas.delete("gameover")
    canvas.delete("food")
    canvas.delete("restart_button")  # Remove the restart button
    if snake:
        canvas.delete("snake")
    if food:
        canvas.delete("food")
    snake = Snake()
    food = Food()
    next_turn(snake, food)



# Create the game window
# Set up the game screen, score, and other UI elements
window = Tk()
window.title("Snake game")
window.resizable(False, False) # stopes the window from being resiezed

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set up event listeners for keyboard input (arrow keys) to control the snake's movement
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
