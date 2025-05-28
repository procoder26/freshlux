import os
import json
import time
import pygame
import cv2
import numpy as np

# Load config.json
with open("config.json") as f:
    config = json.load(f)

IMAGE_DISPLAY_TIME = config["image_display_time"]
TRANSITION_DURATION = config["transition_duration"]
IMAGE_FOLDER = os.path.join(os.getcwd(), config["image_folder"])
VIDEO_EXTENSIONS = tuple(config["video_extensions"])

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen_rect = screen.get_rect()

def load_assets():
    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith(('.jpg', '.jpeg', '.png') + VIDEO_EXTENSIONS)]
    files_full = [os.path.join(IMAGE_FOLDER, f) for f in sorted(files)]
    return files_full

assets = load_assets()

def fade_transition(surface):
    overlay = surface.copy()
    for alpha in range(0, 256, 10):
        overlay.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(overlay, overlay.get_rect(center=screen_rect.center))
        pygame.display.flip()
        time.sleep(TRANSITION_DURATION / 25)

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

def display_image(path):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, screen_rect.size)
        fade_transition(img)
        total_time = IMAGE_DISPLAY_TIME
        elapsed = 0
        interval = 0.1
        while elapsed < total_time:
            check_events()
            time.sleep(interval)
            elapsed += interval
    except Exception as e:
        print(f"Error displaying image {path}: {e}")

def display_video(path):
    try:
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if not fps or fps <= 0:
            fps = 30
        frame_time = 1 / fps

        ret, frame = cap.read()
        if not ret:
            cap.release()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, screen_rect.size)
        surf = pygame.surfarray.make_surface(np.rot90(frame))
        fade_transition(surf)

        while ret:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cap.release()
                        pygame.quit()
                        exit()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, screen_rect.size)
            surf = pygame.surfarray.make_surface(np.rot90(frame))
            screen.blit(surf, (0, 0))
            pygame.display.flip()

            ret, frame = cap.read()
            time.sleep(frame_time)

        cap.release()
    except Exception as e:
        print(f"Error playing video {path}: {e}")

def main_loop():
    while True:
        for media in assets:
            check_events()
            if media.lower().endswith(VIDEO_EXTENSIONS):
                display_video(media)
            else:
                display_image(media)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        pygame.quit()