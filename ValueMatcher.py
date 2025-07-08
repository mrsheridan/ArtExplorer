import turtle
import random
import time

# --- Game Setup ---
screen = turtle.Screen()
screen.title("Value Matcher")
screen.bgcolor("white")
screen.setup(width=600, height=400)
screen.tracer(0)

# --- Game Variables ---
score = 0
time_left = 10
game_over = False

# --- Value Scale ---
def draw_value_scale():
    """Draws the 10-part value scale on the summary screen."""
    x = -225
    y = -150
    for i in range(11):
        shade = 1.0 - (i * 0.1)
        square = turtle.Turtle()
        square.shape("square")
        square.shapesize(stretch_wid=2, stretch_len=2)
        square.color(shade, shade, shade)
        square.penup()
        square.goto(x + (i * 45), y)

# --- Sample Value ---
sample_value_turtle = turtle.Turtle()
sample_value_turtle.shape("square")
sample_value_turtle.shapesize(stretch_wid=3, stretch_len=3)
sample_value_turtle.penup()
sample_value_turtle.goto(-150, 50)

# --- Player Value ---
player_value_turtle = turtle.Turtle()
player_value_turtle.shape("square")
player_value_turtle.shapesize(stretch_wid=3, stretch_len=3)
player_value_turtle.penup()
player_value_turtle.goto(150, 50)
player_value = 0.5  # Initial player value (50% gray)
player_value_turtle.color(player_value, player_value, player_value)

# --- UI Elements ---
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.goto(0, 160)
score_pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

timer_pen = turtle.Turtle()
timer_pen.hideturtle()
timer_pen.penup()
timer_pen.goto(0, 130)
timer_pen.write(f"Time: {time_left}", align="center", font=("Courier", 24, "normal"))

# --- Functions ---
def new_round():
    """Starts a new round with a new random sample value."""
    global sample_value
    sample_value = round(random.uniform(0.0, 1.0), 1)
    sample_value_turtle.color(sample_value, sample_value, sample_value)
    global time_left
    time_left = 10
    update_timer()

def increase_value():
    """Increases the player's value."""
    global player_value
    if not game_over:
        player_value = min(1.0, round(player_value + 0.1, 1))
        player_value_turtle.color(player_value, player_value, player_value)
        check_match()

def decrease_value():
    """Decreases the player's value."""
    global player_value
    if not game_over:
        player_value = max(0.0, round(player_value - 0.1, 1))
        player_value_turtle.color(player_value, player_value, player_value)
        check_match()

def check_match():
    """Checks if the player's value matches the sample value and starts a new round."""
    global score
    closeness = 1.0 - abs(player_value - sample_value)
    points = int(closeness * 100)
    score += points
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
    new_round()

def update_timer():
    """Updates the game timer."""
    global time_left, game_over
    if game_over:
        return

    timer_pen.clear()
    timer_pen.write(f"Time: {time_left}", align="center", font=("Courier", 24, "normal"))
    if time_left > 0:
        time_left -= 1
        screen.ontimer(update_timer, 1000)
    else:
        game_over = True
        show_summary()

def show_summary():
    """Displays the summary screen."""
    screen.clear()
    screen.bgcolor("white")
    score_pen.goto(0, 50)
    score_pen.write(f"Final Score: {score}", align="center", font=("Courier", 30, "bold"))
    draw_value_scale()
    screen.update()

# --- Key Bindings ---
screen.listen()
screen.onkey(increase_value, "Up")
screen.onkey(decrease_value, "Down")

# --- Main Game Loop ---
new_round()
while not game_over:
    screen.update()

turtle.done()