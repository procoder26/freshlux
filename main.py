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

def load_assets():
    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return [os.path.join(IMAGE_FOLDER, f) for f in sorted(files)]

assets = load_assets()

def fade_in(surface, steps=15):
    for alpha in range(0, 256, max(1, 256 // steps)):
        surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(surface, surface.get_rect(center=screen_rect.center))
        pygame.display.flip()
        time.sleep(TRANSITION_DURATION / steps)
    surface.set_alpha(255)

def fade_out(surface, steps=15):
    for alpha in range(255, -1, -max(1, 256 // steps)):
        surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(surface, surface.get_rect(center=screen_rect.center))
        pygame.display.flip()
        time.sleep(TRANSITION_DURATION / steps)

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

def display_image(path):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, screen_rect.size)
        fade_in(img)
        start = time.time()
        while time.time() - start < IMAGE_DISPLAY_TIME:
            check_events()
            time.sleep(0.1)
        fade_out(img)
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
