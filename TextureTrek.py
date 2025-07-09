import pygame
import sys
import os
import random
import time

USERNAME = "wrigh"
SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 800
TEXTURE_SIZE = (300, 300)
FONT_SIZE = 36
TIMER_LIMIT = 10
SCORES_FILE = "scores.txt"
FEEDBACK_DISPLAY_TIME = 1.5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Texture Trek: Final Challenge")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

texture_labels = [
    "Soft", "Gritty", "Slimy", "Bumpy", "Slippery",
    "Fuzzy", "Crumbly", "Smooth", "Scratchy"
]

textures = {}
for label_name in texture_labels:
    filename = f"texture_{label_name.lower()}.jpg"
    path = os.path.join("C:/Users", USERNAME, "Downloads", filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, TEXTURE_SIZE)
            textures[label_name] = img
        except pygame.error:
            print(f"Failed to load image: {filename}")
            textures[label_name] = None
    else:
        print(f"File not found: {filename}")
        textures[label_name] = None

score = 0
correct = 0
incorrect = 0
timed_out = 0
start_time = 0
remaining_textures = random.sample(texture_labels, len(texture_labels))
current_texture = ""
choices = []
correct_index = 0
feedback_message = ""
feedback_color = (0, 0, 0)
feedback_time = 0
game_over = False
awaiting_initials = False
player_initials = ""

def generate_round():
    global current_texture, choices, correct_index, start_time, feedback_message, feedback_time
    if remaining_textures:
        current_texture = remaining_textures.pop(0)
        choices = random.sample(texture_labels, 3)
        if current_texture not in choices:
            choices[random.randint(0, 2)] = current_texture
        correct_index = choices.index(current_texture) + 1
        start_time = time.time()
        feedback_message = ""
        feedback_time = 0
    else:
        end_game()

def render_round():
    screen.fill((240, 240, 250))
    texture_img = textures.get(current_texture, None)
    x = (SCREEN_WIDTH - TEXTURE_SIZE[0]) // 2
    y = 150

    if isinstance(texture_img, pygame.Surface):
        screen.blit(texture_img, (x, y))
    else:
        missing = font.render("Image Missing", True, (200, 0, 0))
        screen.blit(missing, (x + 50, y + 100))

    for i, option in enumerate(choices):
        option_text = font.render(f"{i+1}: {option}", True, (0, 0, 0))
        screen.blit(option_text, (SCREEN_WIDTH // 2 - 100, y + TEXTURE_SIZE[1] + 40 + i * 40))

    if feedback_message and time.time() - feedback_time < FEEDBACK_DISPLAY_TIME:
        feedback = font.render(feedback_message, True, feedback_color)
        screen.blit(feedback, (SCREEN_WIDTH // 2 - feedback.get_width() // 2, y + TEXTURE_SIZE[1] + 180))

    timer_left = max(0, TIMER_LIMIT - int(time.time() - start_time))
    timer_txt = font.render(f"Time Left: {timer_left}s", True, (0, 0, 150))
    score_txt = font.render(f"Score: {score}", True, (0, 150, 0))
    screen.blit(timer_txt, (SCREEN_WIDTH // 2 - timer_txt.get_width() // 2, 20))
    screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, 60))
    pygame.display.flip()

def save_score(initials, points):
    try:
        with open(SCORES_FILE, "a") as file:
            file.write(f"{initials}:{points}\n")
    except IOError:
        pass

def load_scores():
    try:
        entries = []
        with open(SCORES_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[1].isdigit():
                    entries.append((parts[0], int(parts[1])))
        return sorted(entries, key=lambda x: x[1], reverse=True)[:5]
    except (IOError, ValueError):
        return []

def end_game():
    global game_over, awaiting_initials
    game_over = True
    top_scores = load_scores()
    if len(top_scores) < 5 or score > top_scores[-1][1]:
        awaiting_initials = True

def render_end_screen():
    screen.fill((30, 30, 30))
    summary = [
        f"Final Score: {score}",
        f"Correct Answers: {correct}",
        f"Incorrect Answers: {incorrect}",
        f"Timed Out: {timed_out}"
    ]
    for i, line in enumerate(summary):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160 + i * 40))

    if awaiting_initials:
        prompt = font.render(f"Enter initials (3 letters): {player_initials}", True, (255, 215, 0))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 380))
    else:
        heading = font.render("Leaderboard (Top 5):", True, (180, 220, 255))
        screen.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, 420))
        top_scores = load_scores()
        for i, (name, pts) in enumerate(top_scores):
            entry = font.render(f"{i+1}. {name} – {pts} pts", True, (200, 200, 255))
            screen.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2, 470 + i * 40))
    pygame.display.flip()

generate_round()
running = True

while running:
    if not game_over:
        render_round()
        elapsed = time.time() - start_time
        if elapsed > TIMER_LIMIT and not feedback_message:
            score -= 50
            timed_out += 1
            feedback_message = "Too slow! –50"
            feedback_color = (200, 0, 0)
            feedback_time = time.time()

        if feedback_message and time.time() - feedback_time >= FEEDBACK_DISPLAY_TIME:
            generate_round()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            elif event.type == pygame.KEYDOWN and not feedback_message:
                guess = None
                if event.key == pygame.K_1:
                    guess = 1
                elif event.key == pygame.K_2:
                    guess = 2
                elif event.key == pygame.K_3:
                    guess = 3

                if guess is not None:
                    if guess == correct_index:
                        score += 100
                        correct += 1
                        feedback_message = "Correct! +100"
                        feedback_color = (0, 160, 0)
                    else:
                        score -= 50
                        incorrect += 1
                        feedback_message = "Incorrect! –50"
                        feedback_color = (200, 0, 0)
                    feedback_time = time.time()
    else:
        render_end_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif awaiting_initials and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_initials) == 3:
                    save_score(player_initials.upper(), score)
                    awaiting_initials = False
                elif pygame.K_a <= event.key <= pygame.K_z and len(player_initials) < 3:
                    player_initials += chr(event.key)
                elif event.key == pygame.K_BACKSPACE and player_initials:
                    player_initials = player_initials[:-1]

    clock.tick(30)

pygame.quit()
sys.exit()