import pygame
import sys
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Positive & Negative Space Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
HIGHLIGHT = (100, 180, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Shape types
shapes = ["circle", "square", "triangle", "star", "pentagon", "diamond"]

# Game variables
score = 0
current_index = 0
time_limit = 10
last_time = time.time()
MAX_CHOICES = 5
BASE_CHOICES = 2
feedback_text = ""
feedback_color = BLACK
feedback_timer = 0


def draw_positive_space(shape, x, y):
    if shape == "circle":
        pygame.draw.circle(screen, BLACK, (x, y), 60)
    elif shape == "square":
        pygame.draw.rect(screen, BLACK, (x - 50, y - 50, 100, 100))
    elif shape == "triangle":
        points = [(x, y - 60), (x - 60, y + 60), (x + 60, y + 60)]
        pygame.draw.polygon(screen, BLACK, points)
    elif shape == "star":
        points = [
            (x, y - 60), (x + 14, y - 20), (x + 60, y - 20),
            (x + 22, y + 7), (x + 36, y + 60), (x, y + 25),
            (x - 36, y + 60), (x - 22, y + 7), (x - 60, y - 20),
            (x - 14, y - 20)
        ]
        pygame.draw.polygon(screen, BLACK, points)
    elif shape == "pentagon":
        points = [
            (x, y - 60), (x + 57, y - 19), (x + 35, y + 49),
            (x - 35, y + 49), (x - 57, y - 19)
        ]
        pygame.draw.polygon(screen, BLACK, points)
    elif shape == "diamond":
        points = [(x, y - 70), (x + 60, y), (x, y + 70), (x - 60, y)]
        pygame.draw.polygon(screen, BLACK, points)


def draw_negative_space(shape, x, y):
    pygame.draw.rect(screen, BLACK, (x - 80, y - 80, 160, 160))
    if shape == "circle":
        pygame.draw.circle(screen, WHITE, (x, y), 60)
    elif shape == "square":
        pygame.draw.rect(screen, WHITE, (x - 50, y - 50, 100, 100))
    elif shape == "triangle":
        points = [(x, y - 60), (x - 60, y + 60), (x + 60, y + 60)]
        pygame.draw.polygon(screen, WHITE, points)
    elif shape == "star":
        points = [
            (x, y - 60), (x + 14, y - 20), (x + 60, y - 20),
            (x + 22, y + 7), (x + 36, y + 60), (x, y + 25),
            (x - 36, y + 60), (x - 22, y + 7), (x - 60, y - 20),
            (x - 14, y - 20)
        ]
        pygame.draw.polygon(screen, WHITE, points)
    elif shape == "pentagon":
        points = [
            (x, y - 60), (x + 57, y - 19), (x + 35, y + 49),
            (x - 35, y + 49), (x - 57, y - 19)
        ]
        pygame.draw.polygon(screen, WHITE, points)
    elif shape == "diamond":
        points = [(x, y - 70), (x + 60, y), (x, y + 70), (x - 60, y)]
        pygame.draw.polygon(screen, WHITE, points)


def show_text(text, x, y, color=BLACK, font_obj=font):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


def get_option_positions(num_choices):
    margin = 20
    option_width = 130
    option_height = 130
    total_width = num_choices * option_width + (num_choices - 1) * margin
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - option_height - 40
    return [pygame.Rect(start_x + i * (option_width + margin), y, option_width, option_height) for i in range(num_choices)]


def main():
    global score, current_index, time_limit, last_time
    global feedback_text, feedback_color, feedback_timer

    clock = pygame.time.Clock()
    running = True

    correct_option = None
    options_list = []
    current_mode = None
    wrong_version_added = False

    while running:
        screen.fill(WHITE)

        elapsed = time.time() - last_time
        remaining_time = max(0, int(time_limit - elapsed))

        num_choices = min(MAX_CHOICES, BASE_CHOICES + (score // 3))
        current_shape = shapes[current_index]

        if not options_list:
            current_mode = random.choice(["positive", "negative"])
            correct_option = random.randint(0, num_choices - 1)
            wrong_version_added = False
            options_list = []
            used_shapes = [current_shape]

            for i in range(num_choices):
                if i == correct_option:
                    options_list.append((current_shape, current_mode))
                elif not wrong_version_added:
                    wrong_mode = "negative" if current_mode == "positive" else "positive"
                    options_list.append((current_shape, wrong_mode))
                    wrong_version_added = True
                else:
                    available_shapes = [s for s in shapes if s not in used_shapes]
                    if not available_shapes:
                        other_shape = random.choice(shapes)
                    else:
                        other_shape = random.choice(available_shapes)
                        used_shapes.append(other_shape)
                    rand_space = random.choice(["positive", "negative"])
                    options_list.append((other_shape, rand_space))

        # UI and feedback
        show_text(f"Select the correct shape with {current_mode} space.", 10, 10, BLACK, small_font)
        show_text(f"Score: {score}", 10, 40, BLACK, small_font)
        timer_color = RED if remaining_time <= 3 else BLACK
        show_text(f"Time Left: {remaining_time}s", WIDTH - 170, 10, timer_color, small_font)

        if feedback_text:
            show_text(feedback_text, WIDTH // 2 - 80, HEIGHT // 2 + 20, feedback_color)

        draw_positive_space(current_shape, WIDTH // 2, HEIGHT // 2 - 80)

        option_positions = get_option_positions(num_choices)
        mouse_pos = pygame.mouse.get_pos()

        # ✅ Safe draw loop to avoid crash if mismatch
        for i, rect in enumerate(option_positions):
            if i >= len(options_list):
                break
            color = HIGHLIGHT if rect.collidepoint(mouse_pos) else GRAY
            pygame.draw.rect(screen, color, rect)

            shape, space_type = options_list[i]
            if space_type == "positive":
                draw_positive_space(shape, rect.centerx, rect.centery)
            else:
                draw_negative_space(shape, rect.centerx, rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and feedback_timer == 0:
                for i, rect in enumerate(option_positions):
                    if i >= len(options_list):
                        break
                    if rect.collidepoint(event.pos):
                        if i == correct_option:
                            score += 1
                            feedback_text = "Correct!"
                            feedback_color = GREEN
                        else:
                            feedback_text = "Incorrect"
                            feedback_color = RED
                        feedback_timer = time.time() + 1.0
                        break

        pygame.display.flip()
        clock.tick(30)

        # ✅ After display: cleanup for next round
        if feedback_timer > 0 and time.time() > feedback_timer:
            current_index = (current_index + 1) % len(shapes)
            last_time = time.time()
            correct_option = None
            options_list = []
            feedback_text = ""
            feedback_timer = 0
            wrong_version_added = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
