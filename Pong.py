import pygame
import sys
import random
import os
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 8
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
MAX_BALL_SPEED_Y = 10  # Maximum vertical speed for the ball
WHITE = (255, 255, 10)
BLACK = (0, 0, 0)
GRAY = (62, 62, 62)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
FPS = 60

# Win condition
MAX_SCORE = 10

# AI difficulty settings
AI_EASY = 4      # Higher number = slower reactions
AI_MEDIUM = 2    # Default setting
AI_HARD = 1      # Very responsive
AI_IMPOSSIBLE = 0 # Perfect tracking
ai_difficulty = AI_MEDIUM
ai_difficulty_names = {
    AI_EASY: "Easy",
    AI_MEDIUM: "Medium",
    AI_HARD: "Hard",
    AI_IMPOSSIBLE: "Impossible"
}

# Setup background fallback color
default_bg_color = BLACK

# Game states
MENU = 0
GAME = 1
PAUSED = 2
WINNER = 3

# Paddle colors
paddle_colors = [
    ("WHITE", WHITE),
    ("RED", RED),
    ("BLUE", BLUE),
    ("GREEN", GREEN),
    ("YELLOW", YELLOW),
    ("PURPLE", PURPLE),
    ("ORANGE", ORANGE),
    ("CYAN", CYAN)
]

left_paddle_color_idx = 0  # Default to WHITE
right_paddle_color_idx = 0  # Default to WHITE


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("monospace", 100, bold=True)
menu_font = pygame.font.SysFont("monospace", 36)
font = pygame.font.SysFont("monospace", 50)

# Background handling
background_options = [
    "Red&Blue",
    "Black&White",
    "Pink&Purple",
    "OnePiece"
]
current_bg_index = 0
background_image = None

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "images")

# Add code to create the images directory if it doesn't exist
def ensure_images_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    
    if not os.path.exists(images_dir):
        try:
            print(f"Creating images directory at: {images_dir}")
            os.makedirs(images_dir)
            print("Images directory created successfully. Please place your background images there.")
            print("Current game directory: " + script_dir)
            return images_dir
        except Exception as e:
            print(f"Error creating images directory: {e}")
    
    return images_dir

# Create images directory if needed
images_directory = ensure_images_directory()

powerup_images = {
    "speed": pygame.image.load(os.path.join(images_dir, "Speed_Up.jpg")),
    "size": pygame.image.load(os.path.join(images_dir, "Size_UP.png")),
    "slow": pygame.image.load(os.path.join(images_dir, "slow_down.png"))
}

# Load power-up images
def load_powerup_image(type):
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    
    # Check if images exists in different locations
    possible_image_paths = [
        os.path.join(script_dir, "images"),  # Same directory as the script
        "images",                            # Current working directory
        os.path.join(os.getcwd(), "images"), # Explicit current working directory
        os.path.join(script_dir, "..", "images")  # Parent directory
    ]
    
    for image_dir in possible_image_paths:
        if os.path.exists(image_dir) and os.path.isdir(image_dir):
            images_dir = image_dir
            break
    
    # Image filenames based on power-up type
    image_filenames = {
        "speed": "Speed_Up.jpg", 
        "size": "Size_UP.png",
        "slow": "slow_down.png"
    }
    
    try:
        image_path = os.path.join(images_dir, image_filenames[type])
        if os.path.exists(image_path):
            print(f"Loading power-up image: {image_path}")
            return pygame.image.load(image_path)
        else:
            print(f"Power-up image not found: {image_path}")
            return None
    except Exception as e:
        print(f"Error loading power-up image: {e}")
        return None

# Load background images
def load_background(index):
    global background_image
    bg_name = background_options[index]
    print(f"Attempting to load background: {bg_name}")
    
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    
    # Check if images exists in different locations
    possible_image_paths = [
        os.path.join(script_dir, "images"),  # Same directory as the script
        "images",                            # Current working directory
        os.path.join(os.getcwd(), "images"), # Explicit current working directory
        os.path.join(script_dir, "..", "images")  # Parent directory
    ]
    
    for image_dir in possible_image_paths:
        if os.path.exists(image_dir) and os.path.isdir(image_dir):
            print(f"Found images directory at: {image_dir}")
            images_dir = image_dir
            break
    
    try:
        # Debug: Print all files in images directory
        print(f"Looking for files in: {images_dir}")
        try:
            for file in os.listdir(images_dir):
                print(f"  - {file}")
                
                # Check if this file matches our target
                if bg_name.lower() in file.lower():
                    image_path = os.path.join(images_dir, file)
                    print(f"Found matching image: {image_path}")
                    return pygame.image.load(image_path)
        except Exception as e:
            print(f"Error listing directory: {e}")
            return None
        
        # If we get here, no matching file was found
        print(f"No matching file found for {bg_name}")
        return None
    except Exception as e:
        print(f"Error loading background: {e}")
        return None

# Change the background
def change_background():
    global current_bg_index, background_image
    current_bg_index = (current_bg_index + 1) % len(background_options)
    background_image = load_background(current_bg_index)
    # Display current background name
    print(f"Changed to {background_options[current_bg_index]}")

# Try to load the initial background
background_image = load_background(current_bg_index)

# Power-up class
class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type  # "speed", "size", "slow"
        self.active = True
        self.image = powerup_images.get(type)

        self.duration = 10 * FPS  # 10 seconds
        self.effect_active = False
        self.effect_time = 0
    
    def draw(self):
        if self.active and self.image:
            screen.blit(self.image, self.rect.topleft)
    
    def apply(self, paddle, ball):
        if self.type == "speed":
            paddle.speed += 3
            self.effect_active = True
            self.effect_time = self.duration
            self.paddle_ref = paddle
            print(f"Speed boost activated! New speed: {paddle.speed}")
        elif self.type == "size":
            paddle.rect.height += 30
            paddle.rect.y -= 15  # Keep centered
            self.effect_active = True
            self.effect_time = self.duration
            self.paddle_ref = paddle
            print(f"Size increase activated! New height: {paddle.rect.height}")
        elif self.type == "slow":
            ball.speed_x *= 0.7
            ball.speed_y *= 0.7
            self.effect_active = True
            self.effect_time = self.duration
            self.ball_ref = ball
            print(f"Ball slowed! New speed: {ball.speed_x}, {ball.speed_y}")
        self.active = False
    
    def update(self):
        if self.effect_active:
            self.effect_time -= 1
            if self.effect_time <= 0:
                self.remove_effect()
    
    def remove_effect(self):
        if self.type == "speed":
            self.paddle_ref.speed -= 3
            print(f"Speed boost expired. Speed returned to {self.paddle_ref.speed}")
        elif self.type == "size":
            self.paddle_ref.rect.height -= 30
            self.paddle_ref.rect.y += 15  # Keep centered
            print(f"Size increase expired. Height returned to {self.paddle_ref.rect.height}")
        elif self.type == "slow":
            self.ball_ref.speed_x /= 0.7
            self.ball_ref.speed_y /= 0.7
            print(f"Ball speed returned to normal: {self.ball_ref.speed_x}, {self.ball_ref.speed_y}")
        self.effect_active = False

# Game classes
class Paddle:
    def __init__(self, x, y, color_idx=0):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0
        self.color_idx = color_idx
        self.prev_y = y  # For paddle spin effect
        self.movement = 0  # Current movement direction/speed
    
    def move(self, up=True):
        prev_pos = self.rect.y
        
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
        # Calculate movement for spin effect
        self.movement = self.rect.y - prev_pos
    
    def update(self):
        # Track movement for spin effect
        self.prev_y = self.rect.y
    
    def draw(self):
        pygame.draw.rect(screen, paddle_colors[self.color_idx][1], self.rect)
    
    def reset(self):
        self.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.score = 0

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, 
                               HEIGHT // 2 - BALL_SIZE // 2, 
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        self.active = False
        self.start_countdown = 3 * FPS  # 3 seconds countdown
        
        # New attributes for rally speed increase
        self.hits_since_last_score = 0
        self.max_speed_increase = 3  # Maximum multiplier for speed
        self.speed_multiplier = 1.0
        self.base_speed_x = BALL_SPEED_X
        self.base_speed_y = BALL_SPEED_Y
    
    def update(self, paddle_left, paddle_right, powerups):
        if not self.active:
            self.start_countdown -= 1
            if self.start_countdown <= 0:
                self.active = True
            return False
        
        # Store previous position for collision detection
        prev_x = self.rect.x
        prev_y = self.rect.y
        
        # Move the ball with current speed multiplier
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            play_sound(wall_sound)
        
        # Score points if ball goes off screen
        if self.rect.left <= 0:
            play_sound(score_sound)
            paddle_right.score += 1
            # Reset speed multiplier when a point is scored
            self.reset_speed_multiplier()
            return True
        if self.rect.right >= WIDTH:
            play_sound(score_sound)
            paddle_left.score += 1
            # Reset speed multiplier when a point is scored
            self.reset_speed_multiplier()
            return True
        
        # Enhanced paddle collision physics
        if self.rect.colliderect(paddle_left.rect):
            # Calculate where on the paddle the ball hit
            relative_intersect_y = (paddle_left.rect.centery - self.rect.centery) / (paddle_left.rect.height / 2)
            # Change angle based on where it hit
            self.speed_x = abs(self.speed_x)  # Make sure it's going right
            self.speed_y = -relative_intersect_y * MAX_BALL_SPEED_Y
            # Add spin based on paddle movement
            self.speed_y += paddle_left.movement * 0.3
            # Limit vertical speed
            self.speed_y = max(min(self.speed_y, MAX_BALL_SPEED_Y), -MAX_BALL_SPEED_Y)
            play_sound(paddle_sound)
            
            # Increase speed multiplier on paddle hit
            self.increase_speed()
            
        elif self.rect.colliderect(paddle_right.rect):
            # Calculate where on the paddle the ball hit
            relative_intersect_y = (paddle_right.rect.centery - self.rect.centery) / (paddle_right.rect.height / 2)
            # Change angle based on where it hit
            self.speed_x = -abs(self.speed_x)  # Make sure it's going left
            self.speed_y = -relative_intersect_y * MAX_BALL_SPEED_Y
            # Add spin based on paddle movement
            self.speed_y += paddle_right.movement * 0.3
            # Limit vertical speed
            self.speed_y = max(min(self.speed_y, MAX_BALL_SPEED_Y), -MAX_BALL_SPEED_Y)
            play_sound(paddle_sound)
            
            # Increase speed multiplier on paddle hit
            self.increase_speed()
        
        # Check for powerup collisions
        for powerup in powerups:
            if powerup.active and self.rect.colliderect(powerup.rect):
                # Determine which paddle to apply the powerup to
                if self.speed_x > 0:  # Ball moving right, left paddle hit it last
                    powerup.apply(paddle_left, self)
                else:  # Ball moving left, right paddle hit it last
                    powerup.apply(paddle_right, self)
                play_sound(powerup_sound)
        
        return False
    
    def increase_speed(self):
        # Increment hits and increase speed gradually
        self.hits_since_last_score += 1
        
        # Calculate speed multiplier based on hits
        # Increase speed up to max_speed_increase
        self.speed_multiplier = min(1 + (self.hits_since_last_score * 0.05), self.max_speed_increase)
        
        # Update actual speeds based on multiplier
        self.speed_x = math.copysign(self.base_speed_x * self.speed_multiplier, self.speed_x)
        self.speed_y = math.copysign(self.base_speed_y * self.speed_multiplier, self.speed_y)
    
    def reset_speed_multiplier(self):
        # Reset hits and speed multiplier when a point is scored
        self.hits_since_last_score = 0
        self.speed_multiplier = 1.0
        self.speed_x = math.copysign(self.base_speed_x, self.speed_x)
        self.speed_y = math.copysign(self.base_speed_y, self.speed_y)
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        
        # Reset speed-related attributes
        self.base_speed_x = BALL_SPEED_X
        self.base_speed_y = BALL_SPEED_Y
        self.hits_since_last_score = 0
        self.speed_multiplier = 1.0
        
        self.active = False
        self.start_countdown = 3 * FPS  # 3 seconds countdown
    
    def draw(self):
        # Optional: Change ball color or size based on speed multiplier
        ball_color = WHITE
        # Gradually change ball color as it gets faster
        intensity = int(255 * (self.speed_multiplier - 1) / (self.max_speed_increase - 1))
        ball_color = (min(255, 255 * self.speed_multiplier), 
                      max(0, 255 - intensity), 
                      max(0, 255 - intensity))
        
        pygame.draw.rect(screen, ball_color, self.rect)

        
        # Store previous position for collision detection
        prev_x = self.rect.x
        prev_y = self.rect.y
        
        # Move the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            play_sound(wall_sound)
        
        # Score points if ball goes off screen
        if self.rect.left <= 0:
            play_sound(score_sound)
            paddle_right.score += 1
            return True
        if self.rect.right >= WIDTH:
            play_sound(score_sound)
            paddle_left.score += 1
            return True
        
        # Enhanced paddle collision physics
        if self.rect.colliderect(paddle_left.rect):
            # Calculate where on the paddle the ball hit
            relative_intersect_y = (paddle_left.rect.centery - self.rect.centery) / (paddle_left.rect.height / 2)
            # Change angle based on where it hit
            self.speed_x = abs(self.speed_x)  # Make sure it's going right
            self.speed_y = -relative_intersect_y * MAX_BALL_SPEED_Y
            # Add spin based on paddle movement
            self.speed_y += paddle_left.movement * 0.3
            # Limit vertical speed
            self.speed_y = max(min(self.speed_y, MAX_BALL_SPEED_Y), -MAX_BALL_SPEED_Y)
            play_sound(paddle_sound)
            
        elif self.rect.colliderect(paddle_right.rect):
            # Calculate where on the paddle the ball hit
            relative_intersect_y = (paddle_right.rect.centery - self.rect.centery) / (paddle_right.rect.height / 2)
            # Change angle based on where it hit
            self.speed_x = -abs(self.speed_x)  # Make sure it's going left
            self.speed_y = -relative_intersect_y * MAX_BALL_SPEED_Y
            # Add spin based on paddle movement
            self.speed_y += paddle_right.movement * 0.3
            # Limit vertical speed
            self.speed_y = max(min(self.speed_y, MAX_BALL_SPEED_Y), -MAX_BALL_SPEED_Y)
            play_sound(paddle_sound)
        
        # Check for powerup collisions
        for powerup in powerups:
            if powerup.active and self.rect.colliderect(powerup.rect):
                # Determine which paddle to apply the powerup to
                if self.speed_x > 0:  # Ball moving right, left paddle hit it last
                    powerup.apply(paddle_left, self)
                else:  # Ball moving left, right paddle hit it last
                    powerup.apply(paddle_right, self)
                play_sound(powerup_sound)
        
        return False
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        self.active = False
        self.start_countdown = 3 * FPS  # 3 seconds countdown
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Button:
    def __init__(self, y, text, color_type=None):
        self.text = text
        self.y = y
        self.is_hovered = False
        self.color_type = color_type  # "bg", "p1", "p2" or None
        
        # Calculate text size and position
        self.text_surface = menu_font.render(text, True, WHITE)
        
        if color_type is None:
            # Center normal buttons
            self.text_rect = self.text_surface.get_rect(center=(WIDTH//2, y))
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = self.text_surface.get_width() + 40
            self.rect.height = self.text_surface.get_height() + 20
            self.rect.center = (WIDTH//2, y)
        else:
            # Left align color buttons at 30% of screen width
            self.text_rect = self.text_surface.get_rect(x=WIDTH*0.1, centery=y)
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = WIDTH  # Full screen width for clickable area
            self.rect.height = self.text_surface.get_height() + 20
            self.rect.midleft = (0, y)
    
    def draw(self):
        # Draw main text
        color = GRAY if self.is_hovered else WHITE
        text_surface = menu_font.render(self.text, True, color)
        screen.blit(text_surface, self.text_rect)
        
        # Draw current color name instead of "Color Options"
        if self.color_type:
            current_color_name = ""
            if self.color_type == "bg":
                bg_name = background_options[current_bg_index]
                if bg_name.lower() == "onepiece":
                    current_color_name = "ONE PIECE"
                elif bg_name.lower() == "red&blue":
                    current_color_name = "RED & BLUE"
                elif bg_name.lower() == "black&white":
                    current_color_name = "BLACK & WHITE"
                elif bg_name.lower() == "pink&purple":
                    current_color_name = "PINK & PURPLE"
            elif self.color_type == "p1":
                current_color_name = paddle_colors[left_paddle_color_idx][0]
            elif self.color_type == "p2":
                current_color_name = paddle_colors[right_paddle_color_idx][0]
            elif self.color_type == "ai":
                current_color_name = ai_difficulty_names[ai_difficulty]
                
            options_text = menu_font.render(f"({current_color_name})", True, WHITE)
            # Position the color option right-aligned but with a margin to prevent going off-screen
            options_rect = options_text.get_rect(right=WIDTH - 50, centery=self.y)
            screen.blit(options_text, options_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

# Create game objects
paddle_left = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, left_paddle_color_idx)
paddle_right = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, right_paddle_color_idx)
ball = Ball()
powerups = []  # List to hold active powerups

# Create menu buttons to match the screenshot layout
single_player_btn = Button(HEIGHT*0.25, "Singleplayer (vs AI)")
two_player_btn = Button(HEIGHT*0.35, "Multiplayer (Locally)")
change_bg_btn = Button(HEIGHT*0.45, "Change Background Color", "bg")
left_paddle_color_btn = Button(HEIGHT*0.55, "Change Player 1 Color", "p1")
right_paddle_color_btn = Button(HEIGHT*0.65, "Change Player 2 Color", "p2")
ai_difficulty_btn = Button(HEIGHT*0.75, "AI Difficulty", "ai")
quit_btn = Button(HEIGHT*0.85, "Quit")

# Create sound function
def play_sound(sound):
    if sound is not None:
        sound.play()

# Sound objects
paddle_sound = None
wall_sound = None
score_sound = None
powerup_sound = None

# Try to load sound files, but continue if they don't exist
try:
    pygame.mixer.init()
    paddle_sound = pygame.mixer.Sound("paddle.wav")
    wall_sound = pygame.mixer.Sound("wall.wav")
    score_sound = pygame.mixer.Sound("score.wav")
    
    # Create a simple sound for powerups
    powerup_sound = pygame.mixer.Sound("paddle.wav")
    # If you have an actual powerup sound file, use that instead
except:
    print("Sound files not found. Game will run without sound.")

# Change paddle colors
def change_left_paddle_color():
    global left_paddle_color_idx
    left_paddle_color_idx = (left_paddle_color_idx + 1) % len(paddle_colors)
    paddle_left.color_idx = left_paddle_color_idx
    print(f"Left paddle color changed to: {paddle_colors[left_paddle_color_idx][0]}")

def change_right_paddle_color():
    global right_paddle_color_idx
    right_paddle_color_idx = (right_paddle_color_idx + 1) % len(paddle_colors)
    paddle_right.color_idx = right_paddle_color_idx
    print(f"Right paddle color changed to: {paddle_colors[right_paddle_color_idx][0]}")

# Change AI difficulty
def change_ai_difficulty():
    global ai_difficulty
    if ai_difficulty == AI_EASY:
        ai_difficulty = AI_MEDIUM
    elif ai_difficulty == AI_MEDIUM:
        ai_difficulty = AI_HARD
    elif ai_difficulty == AI_HARD:
        ai_difficulty = AI_IMPOSSIBLE
    else:
        ai_difficulty = AI_EASY
    print(f"AI difficulty changed to: {ai_difficulty_names[ai_difficulty]}")

# Simple AI for right paddle
def ai_move(ball, paddle):
    # AI difficulty affects response time and prediction
    if ball.speed_x > 0:  # Only move when ball is coming towards paddle
        # Calculate where the ball will be when it reaches the paddle
        try:
            # Calculate time to reach paddle
            time_to_reach = (paddle.rect.x - ball.rect.x) / ball.speed_x
            # Calculate y-position at that time
            future_y = ball.rect.centery + (ball.speed_y * time_to_reach)
            
            # Add randomness based on difficulty
            if ai_difficulty > 0:  # Not impossible mode
                future_y += random.randint(-ai_difficulty*15, ai_difficulty*15)
            
            # Ensure prediction stays on screen
            future_y = max(min(future_y, HEIGHT - paddle.rect.height//2), paddle.rect.height//2)
            
            # Move towards predicted position
            if future_y < paddle.rect.centery - ai_difficulty:
                paddle.move(up=True)
            elif future_y > paddle.rect.centery + ai_difficulty:
                paddle.move(up=False)
        except:
            # In case of division by zero or other errors
            # Simple fallback AI
            if ball.rect.centery < paddle.rect.centery - ai_difficulty:
                paddle.move(up=True)
            elif ball.rect.centery > paddle.rect.centery + ai_difficulty:
                paddle.move(up=False)

# Function to spawn powerups randomly
def spawn_powerup():
    if random.random() < 0.005 and len([p for p in powerups if p.active]) < 3:  # 0.5% chance per frame, max 3 active
        x = random.randint(WIDTH//4, 3*WIDTH//4)
        y = random.randint(HEIGHT//4, 3*HEIGHT//4)
        type = random.choice(["speed", "size", "slow"])
        powerups.append(PowerUp(x, y, type))

# Function to reset the game
def reset_game():
    global powerups
    paddle_left.reset()
    paddle_right.reset()
    ball.reset()
    powerups = []  # Clear all powerups

# Show winner screen
def show_winner_screen(winner_text):
    # Draw a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Draw winner text
    winner_display = title_font.render(f"{winner_text} WINS!", True, WHITE)
    winner_rect = winner_display.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(winner_display, winner_rect)
    
    # Draw instructions
    instructions = menu_font.render("Press SPACE to play again or ESC for menu", True, WHITE)
    instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(instructions, instructions_rect)

# Draw menu function
def draw_menu():
    # Fill screen with background
    if background_image:
        # Scale the background to fit the screen
        scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    else:
        screen.fill(default_bg_color)
    
    # Draw title - positioned to match screenshot
    title_text = title_font.render("PONG", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT*0.12))
    screen.blit(title_text, title_rect)
    
    # Draw buttons
    single_player_btn.draw()
    two_player_btn.draw()
    change_bg_btn.draw()
    left_paddle_color_btn.draw()
    right_paddle_color_btn.draw()
    ai_difficulty_btn.draw()
    quit_btn.draw()

# Draw game function
def draw_game(two_player_mode):
    # Fill screen with background
    if background_image:
        # Scale the background to fit the screen
        scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    else:
        screen.fill(default_bg_color)
    
    # Draw center line
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    
    # Draw all active powerups
    for p in powerups:
        p.draw()
    
    # Draw paddles and ball
    paddle_left.draw()
    paddle_right.draw()
    ball.draw()
    
    # Display scores
    score_left_text = font.render(str(paddle_left.score), True, WHITE)
    score_right_text = font.render(str(paddle_right.score), True, WHITE)
    screen.blit(score_left_text, (WIDTH // 4, 20))
    screen.blit(score_right_text, (3 * WIDTH // 4, 20))
    
    # "Back to Menu" button at the bottom left with arrow
    back_text = menu_font.render("< Back to Menu", True, WHITE)
    back_rect = back_text.get_rect(bottomleft=(20, HEIGHT - 20))
    screen.blit(back_text, back_rect)
    
    # Display pause instruction
    pause_text = menu_font.render("P: Pause", True, WHITE)
    pause_rect = pause_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 50))
    screen.blit(pause_text, pause_rect)
    
    # Display countdown if ball is not active
    if not ball.active:
        countdown = (ball.start_countdown // FPS) + 1
        countdown_text = font.render(str(countdown), True, WHITE)
        screen.blit(countdown_text, 
                   (WIDTH // 2 - countdown_text.get_width() // 2, 
                    HEIGHT // 2 - countdown_text.get_height() // 2))
    
    # Display active power-up effects
    active_effects = []
    for p in powerups:
        if p.effect_active:
            if p.type == "speed":
                active_effects.append(f"Speed Boost: {p.effect_time//FPS+1}s")
            elif p.type == "size":
                active_effects.append(f"Size Boost: {p.effect_time//FPS+1}s")
            elif p.type == "slow":
                active_effects.append(f"Ball Slowed: {p.effect_time//FPS+1}s")
    
    for i, effect in enumerate(active_effects):
        effect_text = menu_font.render(effect, True, WHITE)
        screen.blit(effect_text, (20, 20 + i * 30))

# Main game loop
running = True
game_state = MENU
two_player_mode = False
cheat_key_pressed = False  # Track cheat key state
pause_key_pressed = False  # Track pause key state
winner = ""

# Print instructions for finding images
print("Looking for background images in the following possible locations:")
script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, "images"),
    "images",
    os.path.join(os.getcwd(), "images"),
    os.path.join(script_dir, "..", "images")
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"✓ Found directory: {path}")
        try:
            files = os.listdir(path)
            if files:
                print(f"  Files found: {', '.join(files)}")
            else:
                print("  Directory is empty")
        except Exception as e:
            print(f"  Error reading directory: {e}")
    else:
        print(f"✗ Not found: {path}")

print("\nExpected background files:")
for bg in background_options:
    print(f"  - {bg}.png or {bg}.jpg")

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_clicked = True
    
    # Get key presses
    keys = pygame.key.get_pressed()
    
    # Menu state
    if game_state == MENU:
        # Check button hover
        single_player_btn.check_hover(mouse_pos)
        two_player_btn.check_hover(mouse_pos)
        change_bg_btn.check_hover(mouse_pos)
        left_paddle_color_btn.check_hover(mouse_pos)
        right_paddle_color_btn.check_hover(mouse_pos)
        ai_difficulty_btn.check_hover(mouse_pos)
        quit_btn.check_hover(mouse_pos)
        
        # Check button clicks
        if single_player_btn.is_clicked(mouse_pos, mouse_clicked):
            game_state = GAME
            two_player_mode = False
            reset_game()
            
        elif two_player_btn.is_clicked(mouse_pos, mouse_clicked):
            game_state = GAME
            two_player_mode = True
            reset_game()
        
        elif change_bg_btn.is_clicked(mouse_pos, mouse_clicked):
            change_background()
            
        elif left_paddle_color_btn.is_clicked(mouse_pos, mouse_clicked):
            change_left_paddle_color()
            
        elif right_paddle_color_btn.is_clicked(mouse_pos, mouse_clicked):
            change_right_paddle_color()
            
        elif ai_difficulty_btn.is_clicked(mouse_pos, mouse_clicked):
            change_ai_difficulty()
            
        elif quit_btn.is_clicked(mouse_pos, mouse_clicked):
            running = False
        
        # Draw menu
        draw_menu()
    
    # Game state
    elif game_state == GAME:
        # Check for pause key
        if keys[pygame.K_p] and not pause_key_pressed:
            game_state = PAUSED
            pause_key_pressed = True
        else:
            pause_key_pressed = keys[pygame.K_p]  # Update key state
            
        # Check back button (now at bottom left)
        back_button_rect = pygame.Rect(20, HEIGHT - 50, 200, 40)
        if back_button_rect.collidepoint(mouse_pos) and mouse_clicked:
            game_state = MENU
        
        # Player 1 controls (left paddle)
        if keys[pygame.K_w]:
            paddle_left.move(up=True)
        if keys[pygame.K_s]:
            paddle_left.move(up=False)
            
        # Cheat button for player 1 (Z key)
        if keys[pygame.K_z]:
            # Only trigger once per key press
            if not cheat_key_pressed:
                paddle_left.score += 1
                print("Player 1 used cheat code!")
                cheat_key_pressed = True
        else:
            cheat_key_pressed = False
        
        # Player 2 controls (right paddle) or AI
        if two_player_mode:
            if keys[pygame.K_UP]:
                paddle_right.move(up=True)
            if keys[pygame.K_DOWN]:
                paddle_right.move(up=False)
        else:
            # Use AI for second paddle
            ai_move(ball, paddle_right)
        
        # Spawn powerups randomly
        spawn_powerup()
        
        # Update powerups
        for p in powerups[:]:  # Create a copy to safely remove items
            p.update()
        
        # Update paddle movement trackers for spin effect
        paddle_left.update()
        paddle_right.update()
        
        # Update ball position and check for scoring
        reset_ball = ball.update(paddle_left, paddle_right, powerups)
        
        if reset_ball:
            ball.reset()
        
        # Check for win condition
        if paddle_left.score >= MAX_SCORE:
            winner = "Player 1"
            game_state = WINNER
        elif paddle_right.score >= MAX_SCORE:
            winner = "Player 2" if two_player_mode else "AI"
            game_state = WINNER
        
        # Draw game
        draw_game(two_player_mode)
    
    # Paused state
    elif game_state == PAUSED:
        # Check for resume key
        if keys[pygame.K_p] and not pause_key_pressed:
            game_state = GAME
            pause_key_pressed = True
        else:
            pause_key_pressed = keys[pygame.K_p]  # Update key state
            
        # Draw the paused game in the background
        draw_game(two_player_mode)
        
        # Draw pause overlay
        pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(pause_overlay, (0, 0))
        
        # Draw pause text
        pause_text = title_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(pause_text, pause_rect)
        
        continue_text = menu_font.render("Press P to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(continue_text, continue_rect)
        
        menu_text = menu_font.render("Press ESC for menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(menu_text, menu_rect)
        
        # Check for ESC key to return to menu
        if keys[pygame.K_ESCAPE]:
            game_state = MENU
    
    # Winner state
    elif game_state == WINNER:
        # Draw the game in the background
        draw_game(two_player_mode)
        
        # Draw winner information
        show_winner_screen(winner)
        
        # Check for keys to continue
        if keys[pygame.K_SPACE]:
            reset_game()
            game_state = GAME
        elif keys[pygame.K_ESCAPE]:
            game_state = MENU
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()