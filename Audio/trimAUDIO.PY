import wave

# Open the input file
with wave.open("output.wav", "rb") as infile:
    # Parameters
    framerate = infile.getframerate()
    nframes = infile.getnframes()
    duration = nframes / float(framerate)
    
    # Define the end time (10 seconds)
    end_time = 9
    
    # If the audio is longer than 10 seconds, slice it
    if duration > end_time:
        # Calculate number of frames for the first 10 seconds
        frames_to_read = int(framerate * end_time)
        
        # Read the first 10 seconds of audio
        infile.setpos(0)  # Start from the beginning
        frames = infile.readframes(frames_to_read)
        
        # Write the output file
        with wave.open("trimmed_output.wav", "wb") as outfile:
            outfile.setnchannels(infile.getnchannels())
            outfile.setsampwidth(infile.getsampwidth())
            outfile.setframerate(infile.getframerate())
            outfile.writeframes(frames)

        print("File has been trimmed to 10 seconds.")
    else:
        print("The audio is already less than 10 seconds long.")
