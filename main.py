import os
import json
import time
import pygame

# Load config.json
with open("config.json") as f:
    config = json.load(f)

IMAGE_DISPLAY_TIME = config["image_display_time"]
TRANSITION_DURATION = config["transition_duration"]
IMAGE_FOLDER = os.path.join(os.getcwd(), config["image_folder"])

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen_rect = screen.get_rect()

def load_assets():
    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return [os.path.join(IMAGE_FOLDER, f) for f in sorted(files)]

assets = load_assets()

def fade_transition(surface):
    overlay = surface.copy()
    for alpha in range(0, 256, 20):  # Faster fade for performance
        overlay.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(overlay, overlay.get_rect(center=screen_rect.center))
        pygame.display.flip()
        time.sleep(TRANSITION_DURATION / 13)

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

def display_image(path):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, screen_rect.size)
        fade_transition(img)
        start = time.time()
        while time.time() - start < IMAGE_DISPLAY_TIME:
            check_events()
            time.sleep(0.1)
    except Exception as e:
        print(f"Error displaying image {path}: {e}")

def main_loop():
    while True:
        for media in assets:
            check_events()
            display_image(media)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        pygame.quit()