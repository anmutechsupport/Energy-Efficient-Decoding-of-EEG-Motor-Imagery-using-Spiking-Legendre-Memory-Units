from pylsl import StreamInlet, resolve_byprop

# resolve markers over LSL
print("looking for a Markers stream...")
marker_streams = resolve_byprop('type', 'Markers', timeout=10)

if marker_streams:
    inlet_marker = StreamInlet(marker_streams[0])
    marker_time_correction = inlet_marker.time_correction() # how do I use this?
else:
    inlet_marker = False
    print("Cant find Markers stream")

while True:
    print(inlet_marker.pull_sample())
