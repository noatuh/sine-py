import pygame
import numpy as np
import pyaudio

# Initialize pygame
pygame.init()

# Constants
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
AMPLITUDE = HEIGHT // 0.02

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
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False

    # Get audio data
    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    
    # Interpolate the numpydata to match screen width
    x_original = np.linspace(0, CHUNK-1, CHUNK)
    x_interpolated = np.linspace(0, CHUNK-1, WIDTH)
    numpydata_interpolated = np.interp(x_interpolated, x_original, numpydata)

    # Draw the waveform
    for x in range(WIDTH-1):
        y_start = int(HEIGHT // 2 + numpydata_interpolated[x] * AMPLITUDE / 32767)
        y_end = int(HEIGHT // 2 + numpydata_interpolated[x+1] * AMPLITUDE / 32767)
        pygame.draw.line(screen, LINE_COLOR, (x, y_start), (x+1, y_end))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
