import os
import json
import time
import pygame

# Load config.json
with open("config.json") as f:
    config = json.load(f)

TRANSITION_DURATION = config["transition_duration"]
IMAGE_FOLDER = os.path.join(os.getcwd(), config["image_folder"])

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen_rect = screen.get_rect()

def load_assets():
    assets = []
    for file in os.listdir(IMAGE_FOLDER):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            name, _ = os.path.splitext(file)
            parts = name.split(".")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                order = int(parts[0])
                display_time = int(parts[1])
                assets.append((order, display_time, os.path.join(IMAGE_FOLDER, file)))
    # Sort by order number
    assets.sort(key=lambda x: x[0])
    return assets

assets = load_assets()

def fade_transition(surface):
    overlay = surface.copy()
    for alpha in range(0, 256, 20):
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

def display_image(path, duration):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, screen_rect.size)
        fade_transition(img)
        start = time.time()
        while time.time() - start < duration:
            check_events()
            time.sleep(0.1)
    except Exception as e:
        print(f"Error displaying image {path}: {e}")

def main_loop():
    while True:
        for _, duration, media_path in assets:
            check_events()
            display_image(media_path, duration)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        pygame.quit()
