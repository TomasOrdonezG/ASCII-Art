import cv2
import moviepy.editor as mp

# Define the path of the video file
video_path = "videos/rick.mp4"

# Create a VideoCapture object
cap = cv2.VideoCapture(video_path)

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Set the duration of the video clip to capture (in seconds)
duration = 1.0

# Calculate the number of frames to capture
num_frames_to_capture = int(duration * fps)

# Create an empty list to store the frames
frames = []

# Loop through the frames
for i in range(num_frames_to_capture):
    # Read the frame
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        break

    # Append the frame to the list
    frames.append(frame)

# Release the video capture
cap.release()

# Create a new VideoWriter object
out = cv2.VideoWriter('videos/rick_short.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frames[0].shape[1], frames[0].shape[0]))

# Write the frames to the output video file
for frame in frames:
    out.write(frame)

# Release the VideoWriter object
out.release()

# Load the new video with moviepy
clip = mp.VideoFileClip("videos/rick_short.mp4")

# Save the new video with the cropped audio
clip.write_videofile("videos/rick_short_with_audio.mp4", fps=fps, codec="libx264", audio_codec="aac")
