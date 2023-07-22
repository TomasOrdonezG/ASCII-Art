import cv2, os
from filter import filter
from moviepy.editor import VideoFileClip, AudioFileClip
from create_ascii_images import PIXEL_H, PIXEL_W

# ! CHANGEABLE:
videoname = 'eva'
AUDIO = True
FULL_VIDEO = False
random = False
colour = False
log_each_row = True
if not FULL_VIDEO:
   duration = 90

output_folder = 'ascii_videos'
frames_folder = 'videos/frames'

# Enter the path to the video file
video_path = f'videos/{videoname}/video.mp4'
audio_path = f'videos/{videoname}/audio.mp3'

# Create a VideoCapture object from the video file
original_video = cv2.VideoCapture(video_path)

# Get data from the video
fps = original_video.get(cv2.CAP_PROP_FPS)
width = int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
if FULL_VIDEO:
   framecount = int(original_video.get(cv2.CAP_PROP_FRAME_COUNT))
   duration = framecount / fps
else:
   framecount = duration * fps

# Make width and height factors of pixel's dimensions
while width % PIXEL_W != 0:
   width -= 1
while height % PIXEL_H != 0:
   height -= 1

# Define the output video filenames
if AUDIO:
   output_video_filename = os.path.join(output_folder, f'{videoname}.mp4')
   output_video_filename_muted = f'videos/{videoname}/TEMP_muted.mp4'
else:
   output_video_filename_muted = os.path.join(output_folder, f'{videoname}_muted.mp4')

# Initialize the video writer object
fourcc = cv2.VideoWriter_fourcc(*'H264')
video_writer = cv2.VideoWriter(output_video_filename_muted, fourcc, fps, (width, height))

# * Create muted video
i = 0
print('Rendering %i frames' % (framecount))
while i < framecount:
   # * Get frame
   i += 1
   ret, frame = original_video.read()
   if not ret:  # End loop when done reading frames
      break
   
   # * Filter frame
   new_frame = filter(frame, colour=colour, random=random, log=log_each_row)
   
   # * Add frame to new video
   video_writer.write(new_frame)

   # * Log
   print('Rendered Frames: %i/%i' % (i, framecount))

# Release video writer
original_video.release()
video_writer.release()
print('Video fully rendered\n')

if AUDIO:
   # * Add audio
   print('Adding audio...')

   # Load the video and audio files
   video_clip = VideoFileClip(output_video_filename_muted)
   audio_clip = AudioFileClip(audio_path)

   # Set the duration of the audio clip to match the duration of the video clip
   audio_clip = audio_clip.set_duration(duration)

   # Add the audio to the video clip
   video_clip = video_clip.set_audio(audio_clip)

   # Write the merged clip to a new file
   video_clip.write_videofile(output_video_filename, codec='libx264', audio_codec='aac')

   # Delete muted video
   os.remove(output_video_filename_muted)

   print('Process finished')
   print('Video saved in ' + output_video_filename)
else:
   print('Video saved in ' + output_video_filename_muted)

# Release the VideoCapture object and close all windows
cv2.destroyAllWindows()