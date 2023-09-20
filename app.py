import pygame
import numpy as np
import pyaudio

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
AMPLITUDE = HEIGHT // 4

# PyAudio setup
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Create a screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("System Audio Wave Visualizer")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get audio data
    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the waveform
    for x in range(min(CHUNK, WIDTH-1)):
        y_start = int(HEIGHT // 2 + numpydata[x] * AMPLITUDE / 32767)
        y_end = int(HEIGHT // 2 + numpydata[x+1] * AMPLITUDE / 32767)
        pygame.draw.line(screen, LINE_COLOR, (x, y_start), (x+1, y_end))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
