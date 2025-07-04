#!/usr/bin/env python3

import os
import json
import time
import pygame

# Get absolute path to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load config.json from script directory
config_path = os.path.join(script_dir, "config.json")
with open(config_path) as f:
    config = json.load(f)

IMAGE_DISPLAY_TIME = config["image_display_time"]
TRANSITION_DURATION = config["transition_duration"]
IMAGE_FOLDER = os.path.join(script_dir, config["image_folder"])

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen_rect = screen.get_rect()

def natural_sort_key(filename):
    # Extract leading number from filename like "12.png" or "3.jpg"
    name, _ = os.path.splitext(filename)
    try:
        return int(name)
    except ValueError:
        return float('inf')  # push non-numeric filenames to the end

def load_assets():
    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    files.sort(key=natural_sort_key)
    return [os.path.join(IMAGE_FOLDER, f) for f in files]

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
        screen.blit(img, screen_rect)
        pygame.display.flip()
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
