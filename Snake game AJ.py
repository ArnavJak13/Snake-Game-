import tkinter as tk
import random

# =========================
# SETTINGS
# =========================
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
SPEED = 100

# =========================
# GAME WINDOW
# =========================
root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)
canvas.pack()

# =========================
# GAME VARIABLES
# =========================
snake = []
direction = "Right"
next_direction = "Right"

food = []
score = 0
game_over = False


# =========================
# CREATE FOOD
# =========================
def create_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        if [x, y] not in snake:
            return [x, y]


# =========================
# START / RESTART GAME
# =========================
def start_game():
    global snake
    global direction
    global next_direction
    global food
    global score
    global game_over

    snake = [
        [300, 300],
        [280, 300],
        [260, 300]
    ]

    direction = "Right"
    next_direction = "Right"

    score = 0
    game_over = False

    food = create_food()

    draw()

    game_loop()


# =========================
# KEYBOARD CONTROLS
# =========================
def key_pressed(event):
    global next_direction

    key = event.keysym.lower()

    # Restart with ENTER
    if key == "return":
        if game_over:
            start_game()
        return

    # Movement
    if key == "w" and direction != "Down":
        next_direction = "Up"

    elif key == "s" and direction != "Up":
        next_direction = "Down"

    elif key == "a" and direction != "Right":
        next_direction = "Left"

    elif key == "d" and direction != "Left":
        next_direction = "Right"


root.bind("<KeyPress>", key_pressed)


# =========================
# DRAW GAME
# =========================
def draw():
    canvas.delete("all")

    # Draw snake
    for i, segment in enumerate(snake):

        x, y = segment

        if i == 0:
            color = "lime"
        else:
            color = "green"

        canvas.create_rectangle(
            x,
            y,
            x + CELL_SIZE,
            y + CELL_SIZE,
            fill=color,
            outline="black"
        )

    # Draw food
    x, y = food

    canvas.create_oval(
        x,
        y,
        x + CELL_SIZE,
        y + CELL_SIZE,
        fill="red",
        outline="darkred"
    )

    # Score
    canvas.create_text(
        50,
        20,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 16)
    )


# =========================
# GAME LOOP
# =========================
def game_loop():

    global direction
    global food
    global score
    global game_over

    if game_over:
        return

    direction = next_direction

    # Current head position
    head_x, head_y = snake[0]

    # Calculate new head position
    if direction == "Up":
        head_y -= CELL_SIZE

    elif direction == "Down":
        head_y += CELL_SIZE

    elif direction == "Left":
        head_x -= CELL_SIZE

    elif direction == "Right":
        head_x += CELL_SIZE

    new_head = [head_x, head_y]

    # =========================
    # WALL COLLISION
    # =========================
    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
    ):
        end_game()
        return

    # =========================
    # BODY COLLISION
    # =========================
    if new_head in snake:
        end_game()
        return

    # Add new head
    snake.insert(0, new_head)

    # =========================
    # FOOD
    # =========================
    if new_head == food:

        score += 1
        food = create_food()

    else:

        # Remove tail
        snake.pop()

    draw()

    # Continue game
    root.after(SPEED, game_loop)


# =========================
# GAME OVER
# =========================
def end_game():

    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 30,
        text="GAME OVER",
        fill="red",
        font=("Arial", 40, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 20,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 20)
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 60,
        text="Press ENTER to restart",
        fill="yellow",
        font=("Arial", 16)
    )


# =========================
# START
# =========================
start_game()

root.mainloop()
