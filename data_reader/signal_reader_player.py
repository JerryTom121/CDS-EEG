from collections import deque
from signalgui import Gui
from dataprocessor import DataProcessor
from learner.perceptron import Perceptron
from signal_reader_sampler import DATUM_PER_SAMPLE, SAMPLE_DURATION, \
  RIGHT_JSON_SAVE_FILE as RIGHT_TRAINING_JSON_FILE, LEFT_JSON_SAVE_FILE as LEFT_TRAINING_JSON_FILE
from arduino import get_arduino
import music.player as m_player
import json, time

# Screen size constants
WIDTH = 1200
HEIGHT = 800
Y_BUFFER = 50
INPUT_MAX = 1023
INPUT_TO_HEIGHT = (HEIGHT-2*Y_BUFFER)/INPUT_MAX

# File Namesx   
LEARNED_R_FILE = 'data/learned_r.json'
LEARNED_L_FILE = 'data/learned_l.json'
# to override
# RIGHT_TRAINING_JSON_FILE = 'data/output_r_works30avg.json'
# LEFT_TRAINING_JSON_FILE = 'data/output_l_works30avg.json'
LEARNED_R_FILE = 'saved_data/learned_r_1.json'
LEARNED_L_FILE = 'saved_data/learned_l_1.json'

USING_SAVED = 1

# Perceptron Parameters
TOLERANCE = 0.00
MAX_ITERATIONS = 1000

# Music Player Parameters
# How long to wait before checking again for a left/right eye movement
CHECK_DELAY = 1 # units of data points received
# How long to wait before sending a second signal after sending one
MIN_SIGNAL_DELAY = SAMPLE_DURATION # units of data points received

# Get data to learn from
def get_json(input_file):
  f = open(input_file, 'r')
  data = f.read()
  f.close()
  return json.loads(data)

# Save a list of int
def save_json(data, file_name):
  f = open(file_name, 'w')
  f.write(json.dumps(data))
  f.close()

if __name__ == '__main__':
  if USING_SAVED:
    # Use already learned vector
    left_v_array = get_json(LEARNED_L_FILE)
    left_perc = Perceptron(v_array = left_v_array)
    right_v_array = get_json(LEARNED_R_FILE)
    right_perc = Perceptron(v_array = right_v_array)
    data_size = len(right_v_array) - 1 # -1 for the added +1 term in the perceptron algo
  else:
    # Get data and learn
    left_raw_data = get_json(LEFT_TRAINING_JSON_FILE)
    left_training_data = left_raw_data[0]
    left_labels = left_raw_data[1]
    left_perc = Perceptron(left_training_data, left_labels, TOLERANCE, MAX_ITERATIONS)
    save_json(left_perc.get_vector().to_array(), LEARNED_L_FILE)
    data_size = len(left_training_data[0])

    right_raw_data = get_json(RIGHT_TRAINING_JSON_FILE)
    right_training_data = right_raw_data[0]
    right_labels = right_raw_data[1]
    right_perc = Perceptron(right_training_data, right_labels, TOLERANCE, MAX_ITERATIONS)
    save_json(right_perc.get_vector().to_array(), LEARNED_R_FILE)
    # print(left_perc.get_vector())
    # print(right_perc.get_vector())

  # print(left_perc.get_vector())
  # print(right_perc.get_vector())

  ard = get_arduino()
  gui = Gui(WIDTH, HEIGHT)

  # Set up memory
  mem_size = data_size
  memory = [0]*mem_size

  # Set up default values for loop 
  t = 0 # time
  done = False
  datum_skip_i = 0
  mem_i = 0
  check_i = 0
  signal_i = 0

  # Set up music
  # gui.init_music()
  # gui.toggle_song()
  # gui.set_on_display()
  gui.write_message("Pause/Unpause Song (Left Glance)")
  gui.write_message2("Pause/Unpause Song (Right Glance)")

  # Main loop
  while not done:
    done = gui.check_for_input()

    if t > gui.width:
      t = 0
      gui.reset_screen()
      gui.reset_last_point()

    # Process next datum
    datum = ard.readline().decode('UTF-8').strip()  # Arduino data comes in bytes
    if len(str(datum)) > 0: # Skip if no datum was read
      try:
        val = int(datum)
      except:
        val = -1
        print("Problem in converting datum to int")

      if datum_skip_i >= DATUM_PER_SAMPLE - 1:
        # Save data to memory
        if mem_i >= mem_size:
          # shift memory over
          memory = memory[1:]
          memory.append(val)
        else:
          # to start, just fill out the memory
          memory[mem_i] = val
          mem_i += 1
        datum_skip_i = 0
      else:
        datum_skip_i += 1

      # Display to GUI
      y = HEIGHT - int(val * INPUT_TO_HEIGHT) - Y_BUFFER # Convert to fit on screen
      gui.draw_point([t, y])
      gui.flip()
      t += 1
      check_i += 1
      signal_i += 1

      # Check if we should brother to check for a signal
      if signal_i >= MIN_SIGNAL_DELAY:
        # Check if we should if we've waiting long enough since last check
        if check_i >= CHECK_DELAY:
          toggle = left_perc.label(memory) == 1
          next_song = right_perc.label(memory) == 1
          if next_song:
            # gui.restart_song() # using restart for testing
            # m_player.next_track()
            m_player.pause_play()
            gui.toggle_block2()
            signal_i = 0 
          if toggle:
            # gui.toggle_song()
            # gui.set_on_display()
            m_player.pause_play()
            gui.toggle_block1()
            signal_i = 0
          check_i = 0
  gui.quit()