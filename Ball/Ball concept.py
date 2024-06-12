import random
import tkinter

WIDTH, HEIGHT = 1200, 500
x, y = WIDTH // 2, HEIGHT // 2
vx, vy = -10, -10
BALL_RADIUS = 20
TIMEOUT = 50

x1 = WIDTH // 2
PLATFORM_H = 50
PLATFORM_W = 250

BRICKS_PART = 0.3
ROWS, COLS = 4, 16Ы

points = 0
game_mode = True

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

ball = canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS,
                          fill='red', outline='black')
platform = canvas.create_rectangle(x1 - PLATFORM_W // 2, HEIGHT,
                                   x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H,
                                   fill='green', outline='black')
score = canvas.create_text(x1, HEIGHT - PLATFORM_H // 2, text = '0', font=('Courier', 32, 'bold'),
                           fill='white')

brick_w, brick_h = WIDTH / COLS, HEIGHT * BRICKS_PART / ROWS

bricks = []

for row in range(ROWS):
    for col in range(COLS):
        xb, yb = col * brick_w, row * brick_h
        red, green, blue = (random.randint(0, 255) for _ in range(3))
        color = f'#{red:0>2x}{green:0>2x}{blue:0>2x}'
        bricks.append(canvas.create_rectangle(xb, yb, xb + brick_w, yb + brick_h, fill = color))

def game():
    global x, y, vx, vy, points, game_mode
    x, y = x + vx, y + vy
    canvas.coords(ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)
    if y <= BALL_RADIUS:
        vy = abs(vy)
    if x <= BALL_RADIUS or x >= WIDTH - BALL_RADIUS:
        vx = -vx

    if x1 - PLATFORM_W // 2 <= x <= x1 + PLATFORM_W // 2 and \
        y == HEIGHT - (BALL_RADIUS + PLATFORM_H):
        vy = -vy
        score_up()

    brick = get_brick()
    if brick:
        vy = -vy
        canvas.delete(brick)
        bricks.pop(bricks.index(brick))
        score_up()
    root.update()
    if y < (HEIGHT - BALL_RADIUS):
        root.after(TIMEOUT, game)
    else:
        game_mode = False
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text='GAME OVER',
                           fill='red', font=(None, 50))

def keyboard(event):
    global x1
    if event.keycode == 37:
        x1 -= 50
    if event.keycode == 39:
        x1 += 50
    move_platform_and_score()

def  score_up():
    global points
    points += 1
    canvas.itemconfig(score, text=str(points))

def mouse_move(event):
    global x1
    x1 = event.x
    move_platform_and_score()

def move_platform_and_score():
    if game_mode:
        canvas.coords(platform, x1 - PLATFORM_W // 2, HEIGHT,
                      x1 + PLATFORM_W // 2, HEIGHT - PLATFORM_H)
        canvas.coords(score, x1, HEIGHT - PLATFORM_H // 2)

def get_brick():
    for brick in bricks:
        xb1, yb1, xb2, yb2 = canvas.coords(brick)
        if xb1 < x < xb2 and yb1 < y < yb2:
            return brick

game()
root.bind('<Key>', keyboard)
root.mainloop()
