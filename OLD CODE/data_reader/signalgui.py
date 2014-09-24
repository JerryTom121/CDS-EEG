import pygame
import time

# Screen size constants
WIDTH = 1200
HEIGHT = 800
Y_BUFFER = 50
INPUT_MAX = 1023
INPUT_TO_HEIGHT = (HEIGHT-2*Y_BUFFER)/INPUT_MAX

# Color & Size Constants
BG_COLOR = 'black'
LINE_COLOR = 'white'
LINE_WIDTH = 1
LIMIT_COLOR = 'blue'
THRESHOLD_COLOR = 'yellow'
TOGGLE_OFF_COLOR = 'green'
TOGGLE_ON_COLOR = 'red'

# Font Constants
FONT = 'monospace'
FONT_SIZE = 15
FONT_COLOR = 'white'

# Logic Constants
INIT_POINT = [0, HEIGHT - Y_BUFFER] # Where the cursor stars
THRESHOLD_PERCENT = 0.535 # Percentage of max height
THRESHOLD = INPUT_MAX * THRESHOLD_PERCENT

# Song Constants
SONG_1 = "Introduction.mp3"
SONG_2 = "Lisztomania.mp3"

# Makeshift enum class
class RecordingType:
  none = 0
  left = 1
  right = 2
  noise = 3

class Gui:
  def __init__(self, _width, _height, header_text=None):
    self.SONG_1 = "Introduction.mp3"
    self.SONG_2 = "Lisztomania.mp3"
    pygame.init()
    self.width = _width
    self.height = _height
    self.screen = pygame.display.set_mode((_width, _height))
    self.toggle1 = False
    self.toggle2 = False
    self.should_save = False
    self.record = False
    self.recording_type = RecordingType.none
    self.message = None
    self.message2 = None
    self.bottom_msg = None
    self.header_text = header_text
    self.reset_last_point()
    self.reset_screen()

  ### Control Functions
  def quit(self):
    pygame.mixer.music.stop()
    pygame.quit()

  def check_for_input(self):
    done = False
    for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
        done = True # Flag that we are done so we exit this loop
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          self.record = True
          self.recording_type = RecordingType.right
        if event.key == pygame.K_l:
          self.record = True
          self.recording_type = RecordingType.left
        if event.key == pygame.K_n:
          self.record = True
          self.recording_type = RecordingType.noise
        if event.key == pygame.K_s:
          self.should_save = True
    return done

  ### Display Functions

  def reset_last_point(self):
    self.last_point = INIT_POINT

  # Redraw the background
  def reset_screen(self):
    # self.screen.fill(pygame.Color(BG_COLOR))
    rect = pygame.Rect(0, Y_BUFFER, WIDTH, HEIGHT - Y_BUFFER)
    pygame.draw.rect(self.screen, pygame.Color(BG_COLOR), rect)

    # Top +5 Volts line
    pygame.draw.line(self.screen, pygame.Color(LIMIT_COLOR),
      (0, Y_BUFFER), (WIDTH, Y_BUFFER), LINE_WIDTH)

    # Bottom -5 Volts line
    pygame.draw.line(self.screen, pygame.Color(LIMIT_COLOR),
      (0,HEIGHT - Y_BUFFER), (WIDTH, HEIGHT - Y_BUFFER), LINE_WIDTH)
  
    self.write_header()

    if self.message:
      self.write_message(self.message)
    if self.message2:
      self.write_message2(self.message2)
    if self.bottom_msg:
      self.write_bottom(self.bottom_msg)

  def draw_point(self, p):
    pygame.draw.line(self.screen, pygame.Color(LINE_COLOR), self.last_point, p, LINE_WIDTH)
    self.last_point = p

  def toggle_block1(self):
    rect = pygame.Rect(0, 0, WIDTH/2, Y_BUFFER/2)
    if self.toggle1:
      pygame.draw.rect(self.screen, pygame.Color(TOGGLE_ON_COLOR), rect)
    else:
      pygame.draw.rect(self.screen, pygame.Color(TOGGLE_OFF_COLOR), rect)
    self.toggle1 = not self.toggle1

  def toggle_block2(self):
    rect = pygame.Rect(WIDTH/2, 0, WIDTH, Y_BUFFER/2)
    if self.toggle2:
      pygame.draw.rect(self.screen, pygame.Color(TOGGLE_ON_COLOR), rect)
    else:
      pygame.draw.rect(self.screen, pygame.Color(TOGGLE_OFF_COLOR), rect)
    self.toggle2 = not self.toggle2

  def write_message(self, message):
    # self.clear_message()
    myfont = pygame.font.SysFont(FONT, FONT_SIZE)
    label = myfont.render(message, 1, pygame.Color(FONT_COLOR))
    self.screen.blit(label, (0, Y_BUFFER/2))
    self.message = message

  def clear_message(self):
    rect = pygame.Rect(0, Y_BUFFER/2 + 1, WIDTH/2, Y_BUFFER - 1)
    pygame.draw.rect(self.screen, pygame.Color(BG_COLOR), rect)
    self.message = None

  def write_message2(self, message):
    # self.clear_message2()
    myfont = pygame.font.SysFont(FONT, FONT_SIZE)
    label = myfont.render(message, 1, pygame.Color(FONT_COLOR))
    self.screen.blit(label, (WIDTH/2, Y_BUFFER/2))
    self.message2 = message

  def clear_message2(self):
    rect = pygame.Rect(WIDTH/2, Y_BUFFER/2 + 1, WIDTH, Y_BUFFER - 1)
    pygame.draw.rect(self.screen, pygame.Color(BG_COLOR), rect)
    self.message2 = None

  def write_bottom(self, message):
    self.clear_bottom()
    myfont = pygame.font.SysFont(FONT, FONT_SIZE)
    label = myfont.render(message, 1, pygame.Color(FONT_COLOR))
    self.screen.blit(label, (0, HEIGHT - Y_BUFFER/2 + 1))
    self.bottom_msg = message

  def clear_bottom(self):
    rect = pygame.Rect(0, HEIGHT - Y_BUFFER/2 + 1, WIDTH, HEIGHT)
    pygame.draw.rect(self.screen, pygame.Color(BG_COLOR), rect)
    self.bottom_msg = None

  def write_header(self):
    if not self.message and not self.message2:
      myfont = pygame.font.SysFont(FONT, FONT_SIZE)
      label = myfont.render(self.header_text, 1, pygame.Color(FONT_COLOR))
      self.screen.blit(label, (0, Y_BUFFER/2))

  def flip(self):
    pygame.display.flip()

  ### Music related functions
  # No longer necessary since we use Windows Media keys
  def init_music(self):
    pygame.mixer.music.load(SONG_2)
    pygame.mixer.music.play(0)
    pygame.mixer.music.pause()

  def toggle_song(self):
    self.is_on = not self.is_on
    if self.is_on:
      pygame.mixer.music.unpause()
    else:
      pygame.mixer.music.pause()

  def next_song(self):
    tmp = self.SONG_2
    self.SONG_2 = self.SONG_1
    self.SONG_1 = tmp
    pygame.mixer.music.stop()
    pygame.mixer.music.load(self.SONG_1)
    pygame.mixer.music.play(0)
    if not self.is_on:
      pygame.mixer.music.pause()

  def restart_song(self):
    pygame.mixer.music.rewind()

  ### Recording Functions
  def should_record(self):
    return self.record

  def is_recording_right(self):
    return self.recording_type == RecordingType.right

  def is_recording_left(self):
    return self.recording_type == RecordingType.left

  def is_recording_noise(self):
    return self.recording_type == RecordingType.noise

  def set_recorded(self, recorded_text):
    self.record = False
    self.recording_type = RecordingType.none
    self.clear_bottom()
    self.write_bottom(recorded_text)

  def set_saved(self, saved_text):
    self.should_save = False
    self.clear_bottom()
    self.write_bottom(saved_text)