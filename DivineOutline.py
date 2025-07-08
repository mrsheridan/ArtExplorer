import tkinter as tk
import math
import random

# Define the main game class
class DivineOutlineGame:
    """
    A game where the user transforms a shape's curviness to match a target type
    (Geometric or Biomorphic) using arrow keys.
    Includes a timer, scoring, rounds, and a splash screen.
    """
    def __init__(self, master):
        """
        Initializes the game window, canvas, and game variables.

        Args:
            master: The Tkinter root window.
        """
        self.master = master
        master.title("Divine Outline")
        # Set window size, slightly increased height for instructions and buttons
        master.geometry("800x750") # Increased height for new UI elements
        master.resizable(False, False) # Prevent resizing for simpler layout management

        # Canvas dimensions and center
        self.canvas_width = 600
        self.canvas_height = 500 # Slightly reduced canvas height to make space for new labels
        self.center_x = self.canvas_width / 2
        self.center_y = self.canvas_height / 2
        self.radius = 200  # Base radius for the shape's points
        self.num_points = 8  # Number of points to define the polygon (e.g., an octagon base)
        self.offset_range = 50  # Max random offset for biomorphic points from geometric points

        # Game state variables
        self.curviness = 50  # Current curviness level (0 = geometric, 100 = biomorphic)
        self.target_type = None  # Stores the target type for the current round ("Geometric" or "Biomorphic")
        self.current_round = 0
        self.total_score = 0
        self.time_left = 0
        self.timer_id = None # To store the ID of the after() call for the timer
        self.game_active = False # Flag to control game input and state

        # --- UI Elements ---
        # Create the main canvas for drawing shapes
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height,
                                bg="#f0f0f0", bd=2, relief="solid")
        # Pack this later, after splash screen

        # Labels for game information
        self.round_label = tk.Label(master, text="Round: 0/10", font=("Inter", 14))
        self.score_label = tk.Label(master, text="Score: 0", font=("Inter", 14))
        self.timer_label = tk.Label(master, text="Time: 10", font=("Inter", 14, "bold"), fg="red")
        self.instructions_label = tk.Label(master, text="Use LEFT/RIGHT arrows to change the shape's curviness. Press SPACE to lock in!",
                                            font=("Inter", 14))
        self.target_label = tk.Label(master, text="", font=("Inter", 16, "bold"), fg="#333333")
        self.feedback_label = tk.Label(master, text="", font=("Inter", 14), fg="blue")

        # New Game button
        self.new_game_button = tk.Button(master, text="New Game", command=self.start_game,
                                         font=("Inter", 12), bg="#4CAF50", fg="white",
                                         activebackground="#45a049", relief="raised", bd=3,
                                         width=15, height=2)

        # Bind arrow keys and spacebar for user input
        master.bind("<Left>", self.decrease_curviness)
        master.bind("<Right>", self.increase_curviness)
        master.bind("<space>", self.lock_shape) # Bind spacebar to lock in the shape

        # Initially show the splash screen
        self.show_splash_screen()

    def show_splash_screen(self):
        """
        Displays the initial splash screen with game rules and a start button.
        Hides all main game UI elements.
        """
        # Hide main game elements
        self.canvas.pack_forget()
        self.round_label.pack_forget()
        self.score_label.pack_forget()
        self.timer_label.pack_forget()
        self.instructions_label.pack_forget()
        self.target_label.pack_forget()
        self.feedback_label.pack_forget()
        self.new_game_button.pack_forget()

        # Create splash screen elements
        self.splash_frame = tk.Frame(self.master, padx=20, pady=20, bg="#e0e0e0", bd=5, relief="ridge")
        self.splash_frame.pack(expand=True, fill="both", padx=50, pady=50)

        splash_title = tk.Label(self.splash_frame, text="Divine Outline", font=("Inter", 28, "bold"), bg="#e0e0e0", fg="#333333")
        splash_title.pack(pady=20)

        rules_text = (
            "Welcome to Divine Outline!\n\n"
            "Your goal is to match the shape's outline to the target type.\n"
            "• Use the LEFT arrow key to make the shape more GEOMETRIC.\n"
            "• Use the RIGHT arrow key to make the shape more BIOMORPHIC (curvy).\n"
            "• You have 10 seconds per round to match the shape.\n"
            "• Press the SPACEBAR to lock in your shape and score points.\n"
            "• Each round is worth up to 100 points, based on accuracy.\n"
            "• There are 10 rounds in total. Good luck!"
        )
        splash_rules = tk.Label(self.splash_frame, text=rules_text, font=("Inter", 14), bg="#e0e0e0", justify="left")
        splash_rules.pack(pady=20)

        start_button = tk.Button(self.splash_frame, text="Start Game", command=self.start_game,
                                 font=("Inter", 16, "bold"), bg="#28a745", fg="white",
                                 activebackground="#218838", relief="raised", bd=5,
                                 width=20, height=3)
        start_button.pack(pady=30)

    def start_game(self):
        """
        Initializes a new game session, hiding the splash screen and showing
        the main game UI. Resets score and round count.
        """
        # Destroy splash screen elements
        if hasattr(self, 'splash_frame'):
            self.splash_frame.destroy()

        # Pack main game UI elements
        self.canvas.pack(pady=5)
        self.round_label.pack(pady=2)
        self.score_label.pack(pady=2)
        self.timer_label.pack(pady=2)
        self.instructions_label.pack(pady=5)
        self.target_label.pack(pady=5)
        self.feedback_label.pack(pady=5)
        self.new_game_button.pack(pady=10)
        self.new_game_button.config(text="New Game") # Reset button text

        self.current_round = 0
        self.total_score = 0
        self.score_label.config(text=f"Score: {self.total_score}")
        self.game_active = True # Enable game input
        self.start_new_round()

    def start_new_round(self):
        """
        Sets up a new round, including incrementing round count, generating
        new shapes, setting a new target, and starting the timer.
        """
        if self.current_round >= 10:
            self.end_game()
            return

        self.current_round += 1
        self.round_label.config(text=f"Round: {self.current_round}/10")
        self.feedback_label.config(text="") # Clear previous feedback

        self.generate_shape_points()  # Generate new unique base shapes for each round

        # Randomly choose the target shape type for this round
        self.target_type = random.choice(["Geometric", "Biomorphic"])
        self.target_label.config(text=f"Target: {self.target_type} Shape")

        # Set initial curviness to challenge the player
        if self.target_type == "Geometric":
            # If target is geometric, start with a more biomorphic shape
            self.curviness = random.randint(60, 90)
        else:  # Target is "Biomorphic"
            # If target is biomorphic, start with a more geometric shape
            self.curviness = random.randint(10, 40)

        self.draw_shape()  # Draw the initial shape
        self.time_left = 10 # Reset timer for the new round
        self.start_timer() # Start the countdown

    def start_timer(self):
        """
        Starts or updates the round timer. When time runs out, it automatically
        locks the shape and ends the round.
        """
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left > 0 and self.game_active:
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.start_timer)
        elif self.game_active: # Time ran out
            self.lock_shape(event=None, timed_out=True) # Automatically lock when time is 0

    def generate_shape_points(self):
        """
        Generates the base geometric points (a regular polygon) and
        corresponding biomorphic points (randomly offset from geometric points).
        These are used for interpolation.
        """
        self.geometric_points = []
        self.biomorphic_points = []

        for i in range(self.num_points):
            # Calculate points for a regular polygon (e.g., octagon)
            angle = 2 * math.pi * i / self.num_points
            gx = self.center_x + self.radius * math.cos(angle)
            gy = self.center_y + self.radius * math.sin(angle)
            self.geometric_points.append((gx, gy))

            # Generate biomorphic points by adding random offsets to geometric points
            # This creates a more organic, less regular shape
            bx = gx + random.uniform(-self.offset_range, self.offset_range)
            by = gy + random.uniform(-self.offset_range, self.offset_range)
            self.biomorphic_points.append((bx, by))

    def get_interpolated_shape(self):
        """
        Calculates the points for the current shape by interpolating between
        the geometric and biomorphic base points based on the 'curviness' level.

        Returns:
            list: A list of (x, y) tuples representing the interpolated shape's vertices.
        """
        interpolated_points = []
        factor = self.curviness / 100.0  # Convert curviness (0-100) to a factor (0.0-1.0)

        for i in range(self.num_points):
            gx, gy = self.geometric_points[i]
            bx, by = self.biomorphic_points[i]

            # Linear interpolation for each coordinate
            ix = gx * (1 - factor) + bx * factor
            iy = gy * (1 - factor) + by * factor
            interpolated_points.append((ix, iy))
        return interpolated_points

    def draw_shape(self):
        """
        Clears the canvas and draws the current interpolated shape.
        """
        self.canvas.delete("all")  # Clear previous drawings on the canvas
        points = self.get_interpolated_shape()
        # Flatten the list of (x,y) tuples into a single list [x1, y1, x2, y2, ...]
        # This format is required by Tkinter's create_polygon
        flat_points = [coord for point in points for coord in point]
        self.canvas.create_polygon(flat_points, outline="black", fill="", width=2)

    def calculate_round_score(self):
        """
        Calculates the score for the current round based on how close the
        current curviness is to the target type's ideal curviness.
        Max score is 100.
        """
        ideal_curviness = 0 # Default for Geometric
        if self.target_type == "Biomorphic":
            ideal_curviness = 100

        # Calculate the absolute difference from the ideal curviness
        difference = abs(self.curviness - ideal_curviness)

        # Score is 100 minus the difference, ensuring it's not negative
        score = max(0, 100 - difference)
        return score

    def lock_shape(self, event=None, timed_out=False):
        """
        Locks in the current shape, calculates the score for the round,
        stops the timer, and prepares for the next round or ends the game.
        """
        if not self.game_active:
            return # Do nothing if game is not active

        # Stop the timer
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        # Calculate score for the round
        round_score = self.calculate_round_score()
        self.total_score += round_score

        # Update UI with round results
        if timed_out:
            self.feedback_label.config(text=f"Time's up! You scored {round_score} points this round.", fg="orange")
        else:
            self.feedback_label.config(text=f"Shape locked! You scored {round_score} points this round.", fg="green")
        self.score_label.config(text=f"Score: {self.total_score}")

        # Disable input temporarily
        self.game_active = False

        # Schedule the next round or end the game after a short delay
        self.master.after(2000, self.start_new_round) # 2-second delay

    def increase_curviness(self, event=None):
        """
        Increases the shape's curviness by a step.
        Clamps the curviness value between 0 and 100.
        Redraws the shape.
        """
        if self.game_active and self.curviness < 100:
            self.curviness += 5 # Increase curviness by 5
            self.draw_shape()

    def decrease_curviness(self, event=None):
        """
        Decreases the shape's curviness by a step.
        Clamps the curviness value between 0 and 100.
        Redraws the shape.
        """
        if self.game_active and self.curviness > 0:
            self.curviness -= 5 # Decrease curviness by 5
            self.draw_shape()

    def end_game(self):
        """
        Ends the game, displays the final score, and resets the game state.
        """
        self.game_active = False # Disable game input
        self.feedback_label.config(text=f"Game Over! Your final score is: {self.total_score} points!", fg="purple")
        self.target_label.config(text="Game Finished!")
        self.timer_label.config(text="Time: --")
        self.instructions_label.config(text="Click 'New Game' to play again!")
        self.new_game_button.config(text="Play Again?") # Change button text

# Main execution block
if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    # Instantiate the game
    game = DivineOutlineGame(root)
    # Start the Tkinter event loop
    root.mainloop()