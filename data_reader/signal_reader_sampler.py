from collections import deque
#from signalgui import Gui
from arduino import get_arduino
import serial, json
import time

# Screen size constants
WIDTH = 1200
HEIGHT = 800
Y_BUFFER = 50
INPUT_MAX = 1023
INPUT_TO_HEIGHT = (HEIGHT-2*Y_BUFFER)/INPUT_MAX

# Data Saving Constants
RIGHT_JSON_SAVE_FILE = 'data/output_r.json'
LEFT_JSON_SAVE_FILE = 'data/output_l.json'
DATUM_PER_SAMPLE = 1 # how many data points to skip (not average) before saving next datum
SAMPLE_DURATION = 150 # units of data points received from arduino


# Text to send to GUI
RECORDING_TEXT = 'Recording'
LEFT_RECORDED_TEXT = 'Trial data recorded for LEFT glance.'
RIGHT_RECORDED_TEXT = 'Trial data recorded for RIGHT glance.'
NOISE_RECORDED_TEXT = 'Trial data recorded for NOISE.'
SAVED_TEXT = 'All Data Saved'
HEADER_TEXT = "Press 'l' (left) 'r' (right) or 'n' (noise) to record. To save all data press 's'."

def save_goodbad_json(good_data, bad_data, json_save_file):
  output_vectors = good_data + bad_data
  output_labels = [1]*len(good_data) + [-1]*len(bad_data)
  f = open("trial.dat", 'w')
  f.write(json.dumps([output_vectors, output_labels]))
  f.close()

if __name__ == '__main__':
  ard = get_arduino()
#  gui = Gui(WIDTH, HEIGHT, HEADER_TEXT)
  right_data = [] # to save one trial
  right_trial_data = [] # to save many trials
  left_data = []
  left_trial_data = []
  noise_data = []
  noise_trial_data = []

  # Set up default values for loop 
  t = 0 # time displayed on GUI
  done = False
  datum_skip_i = 0
  num_data_received = 0
	
    
  i = 0
  # Main loop
  data=[0]*1001
  while True:
#    done = gui.check_for_input()
#
#    if t > gui.width:
#      t = 0
#      gui.reset_screen()
#      gui.reset_last_point()

    # Process next datum
    
    data[i] = (ard.readline().decode('UTF-8').strip(), time.time())  # Arduino data comes in bytes
    print(data[i])
    if i >= 1000:
        break
    i += 1

  f = open("trial.dat", 'w')
  f.write(json.dumps(data))
  f.close()
#    if len(str(datum)) > 0: # Skip if no datum was read
#      try:
#        val = int(datum)
#      except:
#        val = -1
#        print("Problem in converting datum to int")
#
#      # Save data
#      if gui.should_record():
#        gui.write_bottom(RECORDING_TEXT)
#        if num_data_received <= SAMPLE_DURATION:
#          num_data_received += 1
#          if datum_skip_i >= DATUM_PER_SAMPLE - 1:
#            if gui.is_recording_right():
#              right_trial_data.append(val)
#            elif gui.is_recording_left():
#              left_trial_data.append(val)
#            # Could do 'else', but this is kept for clarity
#            elif gui.is_recording_noise():
#              noise_trial_data.append(val)
#            datum_skip_i = 0
#          else:
#            datum_skip_i += 1
#        else:
#          if gui.is_recording_right():
#            right_data.append(right_trial_data)
#            right_trial_data = []
#            gui.set_recorded(RIGHT_RECORDED_TEXT)
#          elif gui.is_recording_left():
#            left_data.append(left_trial_data)
#            left_trial_data = []
#            gui.set_recorded(LEFT_RECORDED_TEXT)
#          elif gui.is_recording_noise():
#            noise_data.append(noise_trial_data)
#            noise_trial_data = []
#            gui.set_recorded(NOISE_RECORDED_TEXT)
#          num_data_received = 0
#          datum_skip_i = 0
#
#      if gui.should_save:
#        save_goodbad_json(right_data, left_data + noise_data, RIGHT_JSON_SAVE_FILE)
#        save_goodbad_json(left_data, right_data + noise_data, LEFT_JSON_SAVE_FILE)
#        gui.set_saved(SAVED_TEXT)
#        left_data = []
#        right_data = []
#        noise_data = []
#
#      # Display to GUI
#      y = HEIGHT - int(val * INPUT_TO_HEIGHT) - Y_BUFFER # Convert to fit on screen
#      gui.draw_point([t, y])
#      t += 1
#      gui.flip()
#
#  gui.quit()