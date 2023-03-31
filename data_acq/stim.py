import random
from psychopy import visual, core, event, gui
from pylsl import StreamInfo, StreamOutlet

# Set up LSL stream
stream_info = StreamInfo(name='my_markers_stream', type='Markers', channel_count=1,
                         nominal_srate=0, channel_format='int32', source_id='uniqueid12345')
marker_stream = StreamOutlet(stream_info)

# Define function to send markers
def send_marker(marker_value):
    marker_stream.push_sample([marker_value])
    print(f"Sent marker {marker_value}")

# Define visual stimuli
win = visual.Window(size=(800, 600), fullscr=False, units='pix')
left_arrow = visual.TextStim(win, text='<', pos=(-200, 0), color='white', height=50)
right_arrow = visual.TextStim(win, text='>', pos=(200, 0), color='white', height=50)
down_arrow = visual.TextStim(win, text='v', pos=(0, -200), color='white', height=50)
fixation_cross = visual.TextStim(win, text='+', pos=(0, 0), color='white', height=50)

# Define trial parameters
cue_duration = 4.0  # duration of the cue presentation in seconds
blank_duration = 2.0  # duration of the blank screen in seconds
fixation_duration = 2.0  # duration of the fixation cross in seconds
trials_per_block = 10  # number of trials per block
block_count = 1  # keep track of block count

# Set up GUI for participant information
participant_info = {'Participant ID': '', 'Session ID': '', 'Gender': ['Male', 'Female', 'Other']}
dialog = gui.DlgFromDict(participant_info, title='Participant Information')

# Start experiment
if dialog.OK:
    for trial in range(trials_per_block):
        # Present left arrow cue
        left_arrow.draw()
        send_marker(1)  # marker for left arrow cue
        win.flip()
        core.wait(cue_duration)

        # Present blank screen
        win.color = 'black'
        win.flip()
        core.wait(blank_duration)

        # Present right arrow cue
        right_arrow.draw()
        send_marker(2)  # marker for right arrow cue
        win.flip()
        core.wait(cue_duration)

        # Present blank screen
        win.color = 'black'
        win.flip()
        core.wait(blank_duration)

        # Present down arrow cue
        down_arrow.draw()
        send_marker(3)  # marker for down arrow cue
        win.flip()
        core.wait(cue_duration)

        # Present fixation cross
        fixation_cross.draw()
        send_marker(4)  # marker for fixation cross
        win.flip()
        core.wait(fixation_duration)

    # End of block
    block_count += 1

# End experiment
win.close()
core.quit()
