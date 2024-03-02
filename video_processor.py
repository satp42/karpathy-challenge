import cv2
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import json

def extract_audio_from_video(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)
    audio.close()
    video.close()

def split_audio_fixed_length(audio_path, video_fps, chunk_length_ms=30000):
    audio = AudioSegment.from_file(audio_path)
    segments_metadata = []
    for i in range(0, len(audio), chunk_length_ms):
        start_time_ms = i
        end_time_ms = min(i + chunk_length_ms, len(audio))
        start_frame = int(start_time_ms / 1000 * video_fps)
        end_frame = int(end_time_ms / 1000 * video_fps)

        if end_time_ms > len(audio):
            end_time_ms = len(audio)
            end_frame = int(len(audio) / 1000 * video_fps)
        chunk = audio[start_time_ms:end_time_ms]
        chunk_filename = f"chunk{i//chunk_length_ms}.wav"
        chunk.export(chunk_filename, format="wav")

        segemts_metadata.append({
            "start_time_ms": start_time_ms,
            "end_time_ms": end_time_ms,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "audio_path": chunk_filename
        })

    with open('segments_metadata.json', 'w') as f:
        json.dump(segments_metadata, f, indent=4)

def process_video(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(frame_delay) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def transcription(audio_segment_path):
    # This is just placeholder text for demonstration purposes.
    simulated_transcription_text = "This is the simulated transcription of the audio segment."
    print(f"Simulated transcription for segment: {audio_segment_path}")
    return simulated_transcription_text

transcription_text = transcription('audio_segment_01.wav')
print(transcription_text)

# process_video('your_video.mp4')
# extract_audio_from_video('your_video.mp4', 'your_audio.wav')
split_audio_fixed_length('your_audio.wav', video_fps=30, chunk_length_ms=30000)

