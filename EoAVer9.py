import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os
import math
import json


# +-----------------------------------------------------------------+
# |                   COLOR MATCH GAME (GAME 1)                     |
# +-----------------------------------------------------------------+
class ColorMatchGame:
    def __init__(self, master, launcher):
        self.master = master
        self.launcher = launcher
        self.master.title("Color Matcher")
        try:
            root_x, root_y = self.master.master.winfo_x(), self.master.master.winfo_y()
            self.master.geometry(f"800x550+{root_x + 50}+{root_y + 50}")
        except:
            self.master.geometry("800x550")
        self.master.resizable(False, False)
        self.master.configure(bg='#333')
        self.master.grab_set()

        self.score, self.rounds_played, self.time_left, self.mix_ratio = 0, 0, 10, 0.5
        self.round_limit, self.timer_id = 10, None

        self.main_frame = tk.Frame(master, bg='#333')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.game_frame = tk.Frame(self.main_frame, bg='#333')

        self.title_label = tk.Label(self.game_frame, text="Color Matcher", font=("Arial", 28, "bold"), fg="white",
                                    bg="#333")
        self.title_label.pack(pady=5)
        info_frame = tk.Frame(self.game_frame, bg='#333');
        info_frame.pack(pady=5)
        self.round_label = tk.Label(info_frame, text="", font=("Arial", 14), fg="white", bg="#333");
        self.round_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(info_frame, text="", font=("Arial", 14, "bold"), fg="#ff5555", bg="#333");
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        self.instructions_label = tk.Label(self.game_frame, text="Use Left/Right Arrows to mix. Press Space to match.",
                                           font=("Arial", 12), fg="white", bg="#333");
        self.instructions_label.pack(pady=5)
        color_frame = tk.Frame(self.game_frame, bg="#333");
        color_frame.pack(pady=10)
        tk.Label(color_frame, text="Target Color", font=("Arial", 14), fg="white", bg="#333").grid(row=0, column=0,
                                                                                                   padx=20)
        self.target_canvas = tk.Canvas(color_frame, width=150, height=150, highlightthickness=2,
                                       highlightbackground="white");
        self.target_canvas.grid(row=1, column=0, padx=20)
        tk.Label(color_frame, text="Your Color", font=("Arial", 14), fg="white", bg="#333").grid(row=0, column=1,
                                                                                                 padx=20)
        self.player_canvas = tk.Canvas(color_frame, width=150, height=150, highlightthickness=2,
                                       highlightbackground="white");
        self.player_canvas.grid(row=1, column=1, padx=20)
        choice_frame = tk.Frame(self.game_frame, bg="#333");
        choice_frame.pack(pady=10)
        tk.Label(choice_frame, text="Choice A", font=("Arial", 12), fg="white", bg="#333").grid(row=0, column=0,
                                                                                                padx=40)
        self.choice_a_canvas = tk.Canvas(choice_frame, width=50, height=50);
        self.choice_a_canvas.grid(row=1, column=0, padx=40)
        tk.Label(choice_frame, text="Choice B", font=("Arial", 12), fg="white", bg="#333").grid(row=0, column=1,
                                                                                                padx=40)
        self.choice_b_canvas = tk.Canvas(choice_frame, width=50, height=50);
        self.choice_b_canvas.grid(row=1, column=1, padx=40)
        self.score_label = tk.Label(self.game_frame, text="Score: 0", font=("Arial", 16), fg="white", bg="#333");
        self.score_label.pack(pady=10)
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 14, "italic"), fg="white", bg="#333");
        self.feedback_label.pack(pady=5)

        self.game_over_frame = tk.Frame(self.main_frame, bg="#333")
        tk.Label(self.game_over_frame, text="Game Over", font=("Arial", 36, "bold"), fg="white", bg="#333").pack(
            pady=20)
        self.final_score_label = tk.Label(self.game_over_frame, text="", font=("Arial", 24), fg="white", bg="#333");
        self.final_score_label.pack(pady=10)
        end_button_frame = tk.Frame(self.game_over_frame, bg="#333")
        end_button_frame.pack(pady=20)
        self.play_again_button = tk.Button(end_button_frame, text="Play Again", font=("Arial", 16),
                                           command=self.restart_game);
        self.play_again_button.pack(side=tk.LEFT, padx=10)
        self.back_button = tk.Button(end_button_frame, text="Back to Main Menu", font=("Arial", 16),
                                     command=self.master.destroy);
        self.back_button.pack(side=tk.RIGHT, padx=10)

        self.master.bind("<Left>", self.move_closer_to_a);
        self.master.bind("<Right>", self.move_closer_to_b)
        self.master.bind("<space>", self.check_match);
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.restart_game()

    def restart_game(self):
        self.game_over_frame.pack_forget();
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.score, self.rounds_played = 0, 0;
        self.score_label.config(text="Score: 0")
        self.next_round()

    def game_over(self):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.game_frame.pack_forget()
        self.launcher.check_high_score("Color Matcher", self.score)
        self.final_score_label.config(text=f"Final Score: {self.score}")
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1; self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up! +0 points", fg="red"); self.master.after(2000, self.next_round)

    def generate_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def mix_colors(self, c1, c2, r):
        return (int(c1[0] * (1 - r) + c2[0] * r), int(c1[1] * (1 - r) + c2[1] * r), int(c1[2] * (1 - r) + c2[2] * r))

    def next_round(self):
        if self.rounds_played >= self.round_limit: self.game_over(); return
        self.rounds_played += 1;
        self.mix_ratio, self.time_left = 0.5, 10
        self.color_a, self.color_b = self.generate_random_color(), self.generate_random_color()
        self.target_color_rgb = self.mix_colors(self.color_a, self.color_b, random.uniform(0.1, 0.9))
        self.update_player_color();
        self.target_canvas.config(bg=self.rgb_to_hex(self.target_color_rgb))
        self.choice_a_canvas.config(bg=self.rgb_to_hex(self.color_a));
        self.choice_b_canvas.config(bg=self.rgb_to_hex(self.color_b))
        self.round_label.config(text=f"Round: {self.rounds_played}/{self.round_limit}");
        self.feedback_label.config(text="")
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.update_timer()

    def update_player_color(self):
        self.player_canvas.config(bg=self.rgb_to_hex(self.mix_colors(self.color_a, self.color_b, self.mix_ratio)))

    def move_closer_to_a(self, e):
        self.mix_ratio = max(0.0, self.mix_ratio - 0.02); self.update_player_color()

    def move_closer_to_b(self, e):
        self.mix_ratio = min(1.0, self.mix_ratio + 0.02); self.update_player_color()

    def check_match(self, e):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        player_rgb = self.mix_colors(self.color_a, self.color_b, self.mix_ratio)
        dist = sum([(a - b) ** 2 for a, b in zip(player_rgb, self.target_color_rgb)]) ** 0.5
        points = int((1 - (dist / 441.67)) ** 2 * 100)
        if points > 95:
            f, c = "Perfect! +{p} pts".format(p=points), "lightgreen"
        elif points > 85:
            f, c = "So close! +{p} pts".format(p=points), "yellow"
        elif points > 70:
            f, c = "Good eye! +{p} pts".format(p=points), "white"
        else:
            f, c = "Not quite. +{p} pts".format(p=points), "orange"
        self.score += points;
        self.score_label.config(text=f"Score: {self.score}");
        self.feedback_label.config(text=f, fg=c)
        self.master.after(2000, self.next_round)


# +-----------------------------------------------------------------+
# |                     LINE QUIZ GAME (GAME 2)                     |
# +-----------------------------------------------------------------+
class LineQuizGame:
    def __init__(self, master, launcher):
        self.master = master
        self.launcher = launcher
        self.master.title("Let's Learn: Lines")
        try:
            root_x, root_y = self.master.master.winfo_x(), self.master.master.winfo_y()
            self.master.geometry(f"750x600+{root_x + 50}+{root_y + 50}")
        except:
            self.master.geometry("750x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#333')
        self.master.grab_set()

        self.question_pool = [
            ("Which line is smooth and flowing?", "curved"), ("Which line moves sharply in angles?", "zigzag"),
            ("Which line goes straight with no bends?", "straight"),
            ("Which line moves up and down like waves?", "wavy"),
            ("Which line swirls like curly ribbon?", "looping"), ("Which line is calm and peaceful?", "wavy"),
            ("Which line bends without corners?", "curved"), ("Which line is sharp and sudden?", "zigzag"),
            ("Which line keeps the same direction?", "straight"), ("Which line curls or spirals?", "looping")
        ]
        self.all_answers = ["curved", "zigzag", "straight", "wavy", "looping"]

        self.main_frame = tk.Frame(master, bg='#333', padx=15, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.timer_id = None
        self.show_lesson_ui()

    def show_lesson_ui(self):
        self.clear_frame()
        center_frame = tk.Frame(self.main_frame, bg="#333")
        center_frame.pack(expand=True)

        tk.Label(center_frame, text="Line Quiz Challenge", font=("Arial", 22, "bold"), fg="white", bg="#333").pack(
            pady=(0, 15))
        lesson_text = (
            "You will have up to ten seconds on each question to answer correctly from three options.\n"
            "Only one of the three options is correct.\n"
            "The most points you can get is 1000 for the ten questions.\n\n"
            "Good luck!"
        )
        tk.Label(center_frame, text=lesson_text, font=("Arial", 14), justify=tk.CENTER, wraplength=700, fg="white",
                 bg="#333").pack(pady=10)
        tk.Button(center_frame, text="Start Quiz", font=("Arial", 14), command=self.start_quiz).pack(pady=20)

    def generate_questions(self):
        self.questions = []
        pool = self.question_pool[:]
        random.shuffle(pool)
        for prompt, correct_answer in pool[:10]:
            options = {correct_answer}
            while len(options) < 3: options.add(random.choice(self.all_answers))
            shuffled_options = list(options);
            random.shuffle(shuffled_options)
            correct_letter = chr(ord('A') + shuffled_options.index(correct_answer))
            self.questions.append((prompt, shuffled_options, correct_letter))

    def start_quiz(self):
        self.generate_questions()
        self.score = 0
        self.current_question_index = 0
        self.show_quiz_ui()

    def show_quiz_ui(self):
        self.clear_frame()
        self.time_left = 10
        center_frame = tk.Frame(self.main_frame, bg="#333");
        center_frame.pack(expand=True)
        top_frame = tk.Frame(center_frame, bg="#333");
        top_frame.pack(pady=10)
        self.score_label = tk.Label(top_frame, text=f"Score: {self.score}", font=("Arial", 14), fg="white", bg="#333");
        self.score_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(top_frame, text=f"Time: {self.time_left}", font=("Arial", 14, "bold"), fg="#ff5555",
                                    bg="#333");
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        prompt, options, _ = self.questions[self.current_question_index]
        self.prompt_label = tk.Label(center_frame, text=prompt, font=("Arial", 16, "italic"), wraplength=700,
                                     fg="white", bg="#333");
        self.prompt_label.pack(pady=20)
        self.answer_buttons = []
        for i, option_text in enumerate(options):
            letter = chr(ord('A') + i)
            button = tk.Button(center_frame, text=f"{letter}. {option_text}", font=("Arial", 14),
                               command=lambda l=letter: self.check_answer(l), width=20)
            button.pack(pady=5);
            self.answer_buttons.append(button)
        self.feedback_label = tk.Label(center_frame, text="", font=("Arial", 14), fg="white", bg="#333");
        self.feedback_label.pack(pady=10)
        self.update_quiz_timer()

    def update_quiz_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1;
            self.timer_id = self.master.after(1000, self.update_quiz_timer)
        else:
            self.feedback_label.config(text="Time's up! +0 points", fg="red")
            for btn in self.answer_buttons: btn.config(state='disabled')
            self.master.after(2000, self.next_question)

    def check_answer(self, chosen_letter):
        if self.timer_id: self.master.after_cancel(self.timer_id); self.timer_id = None
        _, _, correct_letter = self.questions[self.current_question_index]
        if chosen_letter == correct_letter:
            points_earned = self.time_left * 10 + 10;
            self.score += points_earned
            self.feedback_label.config(text=f"Correct! +{points_earned} points", fg="lightgreen")
        else:
            self.feedback_label.config(text=f"Incorrect. The answer was {correct_letter}", fg="orange")
        self.score_label.config(text=f"Score: {self.score}")
        for btn in self.answer_buttons: btn.config(state='disabled')
        self.master.after(2000, self.next_question)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_quiz_ui()
        else:
            self.show_final_score_ui()

    def show_final_score_ui(self):
        self.clear_frame()
        center_frame = tk.Frame(self.main_frame, bg="#333");
        center_frame.pack(expand=True)
        tk.Label(center_frame, text="Quiz Complete!", font=("Arial", 22, "bold"), fg="white", bg="#333").pack(pady=10)
        self.launcher.check_high_score("Line Quiz", self.score)
        tk.Label(center_frame, text=f"Your final score is: {self.score}", font=("Arial", 18), fg="white",
                 bg="#333").pack(pady=10)
        button_frame = tk.Frame(center_frame, bg="#333");
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Play Again", font=("Arial", 14), command=self.start_quiz).pack(side=tk.LEFT,
                                                                                                     padx=10)
        tk.Button(button_frame, text="Back to Main Menu", font=("Arial", 14), command=self.master.destroy).pack(
            side=tk.RIGHT, padx=10)

    def clear_frame(self):
        if self.timer_id: self.master.after_cancel(self.timer_id); self.timer_id = None
        for widget in self.main_frame.winfo_children(): widget.destroy()


# +-----------------------------------------------------------------+
# |                   SHAPE PICKER GAME (GAME 3)                    |
# +-----------------------------------------------------------------+
class ShapeGame:
    def __init__(self, master, launcher):
        self.master = master
        self.launcher = launcher
        self.master.title("Shape Picker Game")
        try:
            root_x, root_y = self.master.master.winfo_x(), self.master.master.winfo_y()
            self.master.geometry(f"600x550+{root_x + 50}+{root_y + 50}")
        except:
            self.master.geometry("600x550")
        self.master.resizable(False, False)
        self.master.configure(bg='#333')
        self.master.grab_set()

        self.score, self.rounds_played, self.time_left = 0, 0, 10
        self.round_limit, self.timer_id = 10, None
        self.correct_shape = ""

        self.main_frame = tk.Frame(master, bg='#333')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.game_frame = tk.Frame(self.main_frame, bg='#333')

        self.title_label = tk.Label(self.game_frame, text="Shape Picker", font=("Arial", 28, "bold"), fg="white",
                                    bg="#333");
        self.title_label.pack(pady=5)
        self.instructions_label = tk.Label(self.game_frame, text="", font=("Arial", 16), fg="white", bg="#333");
        self.instructions_label.pack()
        info_frame = tk.Frame(self.game_frame, bg='#333');
        info_frame.pack(pady=5)
        self.round_label = tk.Label(info_frame, text="", font=("Arial", 14), fg="white", bg="#333");
        self.round_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(info_frame, text="", font=("Arial", 14, "bold"), fg="#ff5555", bg="#333");
        self.timer_label.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(self.game_frame, width=500, height=350, bg="#444", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.check_answer)

        self.score_label = tk.Label(self.game_frame, text="Score: 0", font=("Arial", 16), fg="white", bg="#333");
        self.score_label.pack(pady=5)
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 14, "italic"), fg="white", bg="#333");
        self.feedback_label.pack()

        self.game_over_frame = tk.Frame(self.main_frame, bg="#333")
        tk.Label(self.game_over_frame, text="Game Over", font=("Arial", 36, "bold"), fg="white", bg="#333").pack(
            pady=20)
        self.final_score_label = tk.Label(self.game_over_frame, text="", font=("Arial", 24), fg="white", bg="#333");
        self.final_score_label.pack(pady=10)
        end_button_frame = tk.Frame(self.game_over_frame, bg="#333");
        end_button_frame.pack(pady=20)
        tk.Button(end_button_frame, text="Play Again", font=("Arial", 16), command=self.restart_game).pack(side=tk.LEFT,
                                                                                                           padx=10)
        tk.Button(end_button_frame, text="Back to Main Menu", font=("Arial", 16), command=self.master.destroy).pack(
            side=tk.RIGHT, padx=10)

        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.restart_game()

    def draw_shape(self, shape, x, y):
        size = 50;
        tags = shape;
        color = self.shape_colors[shape]
        if shape == "Circle":
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, tags=tags)
        elif shape == "Square":
            self.canvas.create_rectangle(x, y, x + size, y + size, fill=color, tags=tags)
        elif shape == "Triangle":
            self.canvas.create_polygon(x + size / 2, y, x, y + size, x + size, y + size, fill=color, tags=tags)
        elif shape == "Rectangle":
            self.canvas.create_rectangle(x, y, x + size + 20, y + size - 10, fill=color, tags=tags)
        elif shape == "Oval":
            self.canvas.create_oval(x, y, x + size + 20, y + size - 10, fill=color, tags=tags)
        elif shape == "Pentagon":
            self.canvas.create_polygon(x + 25, y, x, y + 20, x + 10, y + 50, x + 40, y + 50, x + 50, y + 20, fill=color,
                                       tags=tags)
        elif shape == "Hexagon":
            self.canvas.create_polygon(x + 25, y, x + 5, y + 15, x + 5, y + 35, x + 25, y + 50, x + 45, y + 35, x + 45,
                                       y + 15, fill=color, tags=tags)
        elif shape == "Star":
            self.canvas.create_polygon(x + 25, y, x + 30, y + 18, x + 50, y + 20, x + 35, y + 32, x + 40, y + 50,
                                       x + 25, y + 40, x + 10, y + 50, x + 15, y + 32, x, y + 20, x + 20, y + 18,
                                       fill=color, tags=tags)
        elif shape == "Diamond":
            self.canvas.create_polygon(x + 25, y, x + 50, y + 25, x + 25, y + 50, x, y + 25, fill=color, tags=tags)
        elif shape == "Parallelogram":
            self.canvas.create_polygon(x + 15, y, x + 60, y, x + 45, y + 50, x, y + 50, fill=color, tags=tags)

    def next_round(self):
        if self.rounds_played >= self.round_limit: self.game_over(); return
        self.canvas.delete("all")
        self.rounds_played += 1
        self.time_left = 10

        num_shapes = min(3 + self.rounds_played, 10)
        self.shape_list = list(self.shape_colors.keys())[:num_shapes]
        self.correct_shape = random.choice(self.shape_list)

        self.instructions_label.config(text=f"Click the {self.correct_shape}")
        self.feedback_label.config(text="")
        self.round_label.config(text=f"Round: {self.rounds_played}/{self.round_limit}")

        positions = self.get_positions(len(self.shape_list))
        random.shuffle(self.shape_list)
        for shape, (x, y) in zip(self.shape_list, positions):
            self.draw_shape(shape, x, y)

        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.update_timer()

    def get_positions(self, count):
        positions = [];
        spacing_x = 100;
        spacing_y = 100;
        cols = 4;
        start_x = (500 - (cols * 80)) / 2
        for i in range(count):
            x = start_x + (i % cols) * spacing_x
            y = 30 + (i // cols) * spacing_y
            positions.append((x, y))
        return positions

    def check_answer(self, event):
        if self.timer_id:
            self.master.after_cancel(self.timer_id); self.timer_id = None
        else:
            return

        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if clicked_items and self.canvas.gettags(clicked_items[0])[0] == self.correct_shape:
            points = 50 + self.time_left * 10
            self.score += points
            self.feedback_label.config(text=f"Correct! +{points}", fg="lightgreen")
        else:
            self.feedback_label.config(text=f"Wrong! The answer was {self.correct_shape}", fg="orange")
        self.score_label.config(text=f"Score: {self.score}")
        self.master.after(1500, self.next_round)

    @property
    def shape_colors(self):
        return {
            "Circle": "red", "Square": "blue", "Triangle": "green", "Rectangle": "orange",
            "Oval": "purple", "Pentagon": "pink", "Hexagon": "cyan", "Star": "yellow",
            "Diamond": "teal", "Parallelogram": "brown"
        }

    def restart_game(self):
        self.game_over_frame.pack_forget();
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.score, self.rounds_played = 0, 0;
        self.score_label.config(text="Score: 0")
        self.next_round()

    def game_over(self):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.launcher.check_high_score("Shape Picker", self.score)
        self.game_frame.pack_forget();
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)
        self.final_score_label.config(text=f"Final Score: {self.score}")

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1;
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up!", fg="red")
            self.timer_id = None
            self.master.after(1500, self.next_round)


# +-----------------------------------------------------------------+
# |                  SPACE ARRANGER GAME (GAME 4)                   |
# +-----------------------------------------------------------------+
class SpaceArrangerGame:
    def __init__(self, master, launcher):
        self.master = master
        self.launcher = launcher
        self.master.title("Space Arranger")
        try:
            root_x, root_y = self.master.master.winfo_x(), self.master.master.winfo_y()
            self.master.geometry(f"700x600+{root_x + 50}+{root_y + 50}")
        except:
            self.master.geometry("700x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#333')
        self.master.grab_set()

        self.score, self.rounds_played, self.time_left = 0, 0, 10
        self.round_limit, self.timer_id = 10, None

        self.object_pool = {
            "Tree": self.draw_tree, "House": self.draw_house, "Car": self.draw_car,
            "Cloud": self.draw_cloud, "Flower": self.draw_flower, "Bug": self.draw_bug
        }

        self.main_frame = tk.Frame(master, bg='#333')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.splash_frame = tk.Frame(self.main_frame, bg="#333")
        self.game_frame = tk.Frame(self.main_frame, bg='#333')
        self.game_over_frame = tk.Frame(self.main_frame, bg="#333")

        self.setup_splash_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()

        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def setup_splash_screen(self):
        tk.Label(self.splash_frame, text="Space Arranger", font=("Arial", 28, "bold"), fg="white", bg="#333").pack(
            pady=20)
        instructions = (
            "In the Space Arranger game, your goal is to arrange the object that you are given "
            "in either the foreground, midground, or background as quickly as possible. "
            "A higher score will be given for accuracy and quickness."
        )
        tk.Label(self.splash_frame, text=instructions, font=("Arial", 14), fg="white", bg="#333", wraplength=650,
                 justify=tk.CENTER).pack(pady=20, padx=20)
        tk.Button(self.splash_frame, text="Start Game", font=("Arial", 16), command=self.restart_game).pack(pady=20)
        self.splash_frame.pack(fill=tk.BOTH, expand=True)

    def setup_game_screen(self):
        self.title_label = tk.Label(self.game_frame, text="Space Arranger", font=("Arial", 28, "bold"), fg="white",
                                    bg="#333");
        self.title_label.pack(pady=5)
        self.instructions_label = tk.Label(self.game_frame, text="", font=("Arial", 16), fg="white", bg="#333",
                                           wraplength=650);
        self.instructions_label.pack()
        info_frame = tk.Frame(self.game_frame, bg='#333');
        info_frame.pack(pady=5)
        self.round_label = tk.Label(info_frame, text="", font=("Arial", 14), fg="white", bg="#333");
        self.round_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(info_frame, text="", font=("Arial", 14, "bold"), fg="#ff5555", bg="#333");
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        self.canvas = tk.Canvas(self.game_frame, width=600, height=400, bg="#87CEEB", highlightthickness=0);
        self.canvas.pack(pady=10)
        self.score_label = tk.Label(self.game_frame, text="Score: 0", font=("Arial", 16), fg="white", bg="#333");
        self.score_label.pack(pady=5)
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 14, "italic"), fg="white", bg="#333");
        self.feedback_label.pack()

    def setup_game_over_screen(self):
        tk.Label(self.game_over_frame, text="Game Over", font=("Arial", 36, "bold"), fg="white", bg="#333").pack(
            pady=20)
        self.final_score_label = tk.Label(self.game_over_frame, text="", font=("Arial", 24), fg="white", bg="#333");
        self.final_score_label.pack(pady=10)
        end_button_frame = tk.Frame(self.game_over_frame, bg="#333");
        end_button_frame.pack(pady=20)
        tk.Button(end_button_frame, text="Play Again", font=("Arial", 16), command=self.restart_game).pack(side=tk.LEFT,
                                                                                                           padx=10)
        tk.Button(end_button_frame, text="Back to Main Menu", font=("Arial", 16), command=self.master.destroy).pack(
            side=tk.RIGHT, padx=10)

    def restart_game(self):
        self.splash_frame.pack_forget()
        self.game_over_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.score, self.rounds_played = 0, 0
        self.score_label.config(text="Score: 0")
        self.next_round()

    def game_over(self):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.launcher.check_high_score("Space Arranger", self.score)
        self.game_frame.pack_forget()
        self.final_score_label.config(text=f"Final Score: {self.score}")
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1;
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up! +0 points", fg="red")
            self.canvas.unbind("<Motion>");
            self.canvas.unbind("<Button-1>")
            self.master.after(2000, self.next_round)

    def draw_background(self):
        self.canvas.create_rectangle(0, 0, 600, 400, fill="#a8e6cf", outline=""); self.canvas.create_rectangle(0, 250,
                                                                                                               600, 400,
                                                                                                               fill="#dcedc1",
                                                                                                               outline=""); self.canvas.create_line(
            0, 250, 600, 250, fill="#77dd77", width=3)

    def draw_tree(self, x, y, s):
        self.canvas.create_rectangle(x - 5 * s, y, x + 5 * s, y + 40 * s, f="saddlebrown",
                                     tags="object"); self.canvas.create_oval(x - 20 * s, y - 30 * s, x + 20 * s, y,
                                                                             f="forestgreen", tags="object")

    def draw_house(self, x, y, s):
        self.canvas.create_rectangle(x - 25 * s, y, x + 25 * s, y + 40 * s, f="lightyellow",
                                     tags="object"); self.canvas.create_polygon(x - 30 * s, y, x + 30 * s, y, x,
                                                                                y - 20 * s, f="firebrick",
                                                                                tags="object")

    def draw_car(self, x, y, s):
        self.canvas.create_rectangle(x - 30 * s, y + 10 * s, x + 30 * s, y + 30 * s, f="royalblue",
                                     tags="object"); self.canvas.create_rectangle(x - 15 * s, y, x + 15 * s, y + 15 * s,
                                                                                  f="lightblue",
                                                                                  tags="object"); self.canvas.create_oval(
            x - 25 * s, y + 25 * s, x - 10 * s, y + 40 * s, f="black", tags="object"); self.canvas.create_oval(
            x + 10 * s, y + 25 * s, x + 25 * s, y + 40 * s, f="black", tags="object")

    def draw_cloud(self, x, y, s):
        self.canvas.create_oval(x - 25 * s, y, x + 25 * s, y + 20 * s, f="white", o="",
                                tags="object"); self.canvas.create_oval(x - 40 * s, y + 10 * s, x, y + 30 * s,
                                                                        f="white", o="",
                                                                        tags="object"); self.canvas.create_oval(x,
                                                                                                                y + 10 * s,
                                                                                                                x + 40 * s,
                                                                                                                y + 30 * s,
                                                                                                                f="white",
                                                                                                                o="",
                                                                                                                tags="object")

    def draw_flower(self, x, y, s):
        self.canvas.create_oval(x - 5 * s, y - 5 * s, x + 5 * s, y + 5 * s, f="yellow", o=""); [
            self.canvas.create_oval(x - 15 * s * math.cos(a), y - 15 * s * math.sin(a), x + 15 * s * math.cos(a),
                                    y + 15 * s * math.sin(a), f="pink", o="") for a in
            [i / 4 * math.pi for i in range(8)]]

    def draw_bug(self, x, y, s):
        self.canvas.create_oval(x - 10 * s, y, x + 10 * s, y + 15 * s, f="red", tags="object"); self.canvas.create_oval(
            x - 5 * s, y - 10 * s, x + 5 * s, y + 5 * s, f="black", tags="object")

    def mouse_move(self, event):
        self.canvas.delete("object")
        if self.current_object_name == "Cloud":
            y = max(20, min(event.y, 230))
            scale = 0.2 + ((y - 20) / 210) * 0.8
        else:
            y = max(250, min(event.y, 400 - 20))
            scale = 0.2 + ((y - 250) / 150) * 1.3
        self.current_object_func(event.x, y, scale)

    def check_placement(self, event):
        if self.timer_id:
            self.master.after_cancel(self.timer_id); self.timer_id = None
        else:
            return
        self.canvas.unbind("<Motion>");
        self.canvas.unbind("<Button-1>")

        y = event.y
        sky_limit = 250

        if self.current_object_name == "Cloud":
            zone_map = {"BACKGROUND": (0, sky_limit / 2), "MIDGROUND": (sky_limit / 2, sky_limit * 0.8),
                        "FOREGROUND": (sky_limit * 0.8, sky_limit)}
        else:
            ground_height = 400 - sky_limit
            zone_map = {"BACKGROUND": (sky_limit, sky_limit + ground_height / 3),
                        "MIDGROUND": (sky_limit + ground_height / 3, sky_limit + 2 * ground_height / 3),
                        "FOREGROUND": (sky_limit + 2 * ground_height / 3, 400)}

        placed_zone = ""
        for zone, (start, end) in zone_map.items():
            if start <= y < end: placed_zone = zone; break

        if placed_zone == self.target_zone:
            points = 50 + self.time_left * 10
            self.score += points
            self.feedback_label.config(text=f"Correct! +{points}", fg="lightgreen")
        else:
            self.feedback_label.config(text=f"Wrong! That's the {placed_zone}.", fg="orange")
        self.score_label.config(text=f"Score: {self.score}")
        self.master.after(2000, self.next_round)

    def next_round(self):
        if self.rounds_played >= self.round_limit: self.game_over(); return
        self.canvas.delete("all");
        self.draw_background()

        self.rounds_played += 1;
        self.time_left = 10

        self.current_object_name, self.current_object_func = random.choice(list(self.object_pool.items()))

        if self.current_object_name == "Cloud":
            self.target_zone = random.choice(["FOREGROUND", "MIDGROUND", "BACKGROUND"])
        else:
            self.target_zone = random.choice(["FOREGROUND", "MIDGROUND", "BACKGROUND"])

        self.instructions_label.config(text=f"Place the {self.current_object_name} in the {self.target_zone}")
        self.feedback_label.config(text="")
        self.round_label.config(text=f"Round: {self.rounds_played}/{self.round_limit}")

        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.bind("<Button-1>", self.check_placement)
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.update_timer()


# +-----------------------------------------------------------------+
# |                   ANGLE MATCH GAME (GAME 5)                     |
# +-----------------------------------------------------------------+
class AngleMatchGame:
    def __init__(self, master, launcher):
        self.master = master
        self.launcher = launcher
        self.master.title("Angle Matcher")
        try:
            root_x, root_y = self.master.master.winfo_x(), self.master.master.winfo_y()
            self.master.geometry(f"600x600+{root_x + 50}+{root_y + 50}")
        except:
            self.master.geometry("600x600")
        self.master.resizable(False, False)
        self.master.configure(bg='#333')
        self.master.grab_set()

        self.score, self.rounds_played, self.time_left = 0, 0, 10
        self.round_limit, self.timer_id = 10, None
        self.player_angle = 0

        self.main_frame = tk.Frame(master, bg='#333')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.game_frame = tk.Frame(self.main_frame, bg='#333')

        self.title_label = tk.Label(self.game_frame, text="Angle Matcher", font=("Arial", 28, "bold"), fg="white",
                                    bg="#333");
        self.title_label.pack(pady=5)
        self.instructions_label = tk.Label(self.game_frame,
                                           text="Adjust angle with arrow keys. Press Spacebar to submit before time runs out!",
                                           font=("Arial", 12), fg="white", bg="#333", wraplength=500);
        self.instructions_label.pack(pady=(0, 5))
        info_frame = tk.Frame(self.game_frame, bg='#333');
        info_frame.pack(pady=5)
        self.round_label = tk.Label(info_frame, text="", font=("Arial", 14), fg="white", bg="#333");
        self.round_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(info_frame, text="", font=("Arial", 14, "bold"), fg="#ff5555", bg="#333");
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        self.canvas = tk.Canvas(self.game_frame, width=400, height=400, bg='black', highlightthickness=0);
        self.canvas.pack(pady=10)
        self.score_label = tk.Label(self.game_frame, text="Score: 0", font=("Arial", 16), fg="white", bg="#333");
        self.score_label.pack(pady=10)
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 14, "italic"), fg="white", bg="#333");
        self.feedback_label.pack(pady=5)

        self.game_over_frame = tk.Frame(self.main_frame, bg="#333")
        tk.Label(self.game_over_frame, text="Game Over", font=("Arial", 36, "bold"), fg="white", bg="#333").pack(
            pady=20)
        self.final_score_label = tk.Label(self.game_over_frame, text="", font=("Arial", 24), fg="white", bg="#333");
        self.final_score_label.pack(pady=10)
        end_button_frame = tk.Frame(self.game_over_frame, bg="#333");
        end_button_frame.pack(pady=20)
        tk.Button(end_button_frame, text="Play Again", font=("Arial", 16), command=self.restart_game).pack(side=tk.LEFT,
                                                                                                           padx=10)
        tk.Button(end_button_frame, text="Back to Main Menu", font=("Arial", 16), command=self.master.destroy).pack(
            side=tk.RIGHT, padx=10)

        self.master.bind("<Left>", self.rotate_left);
        self.master.bind("<Right>", self.rotate_right)
        self.master.bind("<space>", self.check_match);
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.restart_game()

    def restart_game(self):
        self.game_over_frame.pack_forget();
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.score, self.rounds_played = 0, 0;
        self.score_label.config(text="Score: 0")
        self.next_round()

    def game_over(self):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.launcher.check_high_score("Angle Matcher", self.score)
        self.game_frame.pack_forget();
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)
        self.final_score_label.config(text=f"Final Score: {self.score}")

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1; self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up! +0 points", fg="red"); self.master.after(1500, self.next_round)

    def draw_lines(self):
        self.canvas.delete("all");
        cx, cy, length = 200, 200, 150
        tx2 = cx + length * math.cos(math.radians(self.target_angle));
        ty2 = cy + length * math.sin(math.radians(self.target_angle))
        self.canvas.create_line(cx, cy, tx2, ty2, fill='grey', width=2, dash=(4, 4))
        px2 = cx + length * math.cos(math.radians(self.player_angle));
        py2 = cy + length * math.sin(math.radians(self.player_angle))
        self.canvas.create_line(cx, cy, px2, py2, fill='cyan', width=3)

    def next_round(self):
        if self.rounds_played >= self.round_limit: self.game_over(); return
        self.rounds_played += 1;
        self.player_angle = 0;
        self.time_left = 10
        self.target_angle = random.randint(0, 359)
        self.round_label.config(text=f"Round: {self.rounds_played}/{self.round_limit}");
        self.feedback_label.config(text="")
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.update_timer();
        self.draw_lines()

    def rotate_left(self, e):
        self.player_angle = (self.player_angle - 2) % 360; self.draw_lines()

    def rotate_right(self, e):
        self.player_angle = (self.player_angle + 2) % 360; self.draw_lines()

    def check_match(self, e):
        if self.timer_id: self.master.after_cancel(self.timer_id)
        diff = abs(self.player_angle - self.target_angle);
        angle_diff = min(diff, 360 - diff)
        points = max(0, int((1 - (angle_diff / 180)) ** 2 * 100))
        if angle_diff < 2:
            f, c = f"Perfect! +{points} pts", "lightgreen"
        elif angle_diff < 10:
            f, c = f"Excellent! +{points} pts", "yellow"
        elif angle_diff < 25:
            f, c = f"Good! +{points} pts", "white"
        else:
            f, c = f"Missed. +{points} pts", "orange"
        self.score += points;
        self.score_label.config(text=f"Score: {self.score}");
        self.feedback_label.config(text=f, fg=c)
        self.master.after(2000, self.next_round)


# +-----------------------------------------------------------------+
# |              INITIALS ENTRY DIALOG (CUSTOM)                     |
# +-----------------------------------------------------------------+
class InitialsDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("New High Score!")
        tk.Label(master, text="Congratulations! You made the top 3!").pack()
        tk.Label(master, text="Please enter your initials (3 characters):").pack()
        self.entry = tk.Entry(master, width=5, justify='center', font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.focus_set()
        return self.entry

    def validate(self):
        result = self.entry.get().upper()
        if len(result) == 3 and result.isalpha():
            return 1
        else:
            messagebox.showwarning("Validation Error", "Please enter exactly 3 letters.", parent=self)
            return 0

    def apply(self):
        self.result = self.entry.get().upper()


# +-----------------------------------------------------------------+
# |                       GAME LAUNCHER UI                          |
# +-----------------------------------------------------------------+
class GameLauncher:
    def __init__(self, master):
        self.master = master
        self.master.title("Art Element Game Hub")
        self.master.geometry("750x700")
        self.master.configure(bg="#2d2d2d")

        self.score_file = "best_of_the_best.txt"
        self.high_scores = []  # List of tuples: (score, initials, game_name)

        tk.Label(master, text="Art Element Game Hub", font=("Arial", 28, "bold"), fg="white", bg="#2d2d2d").pack(
            pady=10)

        button_frame = tk.Frame(master, bg="#2d2d2d");
        button_frame.pack(pady=5, padx=20, fill="x")
        game_options = [
            ("Color Matcher", self.launch_color_matcher),
            ("Line Quiz", self.launch_line_quiz),
            ("Shape Picker", self.launch_shape_picker),
            ("Shape Racer", self.launch_shape_racer),
            ("Form Flipper", self.launch_form_flipper),
            ("Angle Matcher", self.launch_angle_matcher)
        ]
        for i, (text, command) in enumerate(game_options):
            row, col = divmod(i, 2)
            button = tk.Button(button_frame, text=text, font=("Arial", 14), command=command, width=15, height=3)
            button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            button_frame.grid_rowconfigure(row, weight=1);
            button_frame.grid_columnconfigure(col, weight=1)

        self.highscore_frame = tk.Frame(master, bg="#444", padx=10, pady=10)
        self.highscore_frame.pack(pady=10, padx=20, fill='x')
        tk.Label(self.highscore_frame, text="Best of the Best", font=("Arial", 18, "bold"), fg="white",
                 bg="#444").pack()
        self.high_score_labels = []
        for i in range(3):
            label = tk.Label(self.highscore_frame, text="", font=("Arial", 14), fg="white", bg="#444")
            label.pack(anchor='center')
            self.high_score_labels.append(label)

        # --- NEW: Reset Button ---
        tk.Button(self.highscore_frame, text="Reset Scores", font=("Arial", 10), command=self.reset_high_scores).pack(
            pady=5)

        self.load_high_scores()
        self.update_high_score_display()

    # --- NEW: Reset Function ---
    def reset_high_scores(self):
        """Deletes the score file and clears the high score display."""
        if messagebox.askyesno("Confirm Reset",
                               "Are you sure you want to reset all high scores? This cannot be undone."):
            if os.path.exists(self.score_file):
                try:
                    os.remove(self.score_file)
                except OSError as e:
                    messagebox.showerror("Error", f"Could not delete scores file: {e}")

            # Clear the in-memory list and update the display
            self.high_scores = []
            self.update_high_score_display()
            messagebox.showinfo("Success", "High scores have been reset.")

    def load_high_scores(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    self.high_scores = json.load(f)
            except (IOError, json.JSONDecodeError):
                self.high_scores = []
        self.high_scores.sort(key=lambda item: item[0], reverse=True)

    def save_high_scores(self):
        try:
            with open(self.score_file, 'w') as f:
                json.dump(self.high_scores, f)
        except IOError:
            messagebox.showerror("Error", "Could not save high scores.")

    def update_high_score_display(self):
        for i, label in enumerate(self.high_score_labels):
            if i < len(self.high_scores):
                score, initials, game_name = self.high_scores[i]
                label.config(text=f"{i + 1}. {initials} - {score} ({game_name})")
            else:
                label.config(text=f"{i + 1}. ---")

    def check_high_score(self, game_name, score):
        is_high_score = len(self.high_scores) < 3 or score > self.high_scores[-1][0]
        if is_high_score and score > 0:
            dialog = InitialsDialog(self.master)
            if dialog.result:
                initials = dialog.result
                self.high_scores.append((score, initials, game_name))
                self.high_scores.sort(key=lambda item: item[0], reverse=True)
                self.high_scores = self.high_scores[:3]
                self.save_high_scores()
                self.update_high_score_display()

    def launch_color_matcher(self):
        ColorMatchGame(tk.Toplevel(self.master), self)

    def launch_line_quiz(self):
        LineQuizGame(tk.Toplevel(self.master), self)

    def launch_shape_picker(self):
        ShapeGame(tk.Toplevel(self.master), self)

    def launch_shape_racer(self):
        ShapeRacerGame(tk.Toplevel(self.master), self)

    def launch_form_flipper(self):
        FormFlipperGame(tk.Toplevel(self.master), self)

    def launch_angle_matcher(self):
        AngleMatchGame(tk.Toplevel(self.master), self)

    def launch_placeholder(self):
        messagebox.showinfo("Coming Soon", "This game is not yet available!")
if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
