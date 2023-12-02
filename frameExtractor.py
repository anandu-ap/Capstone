import cv2
import os

class FrameExtractor:
    def __init__(self):
        self.key_frames = None

    # Method to extract key frames from video
    def extract_key_frames(self, video_path, output_directory, num_key_frames):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = [int(i * total_frames / num_key_frames) for i in range(num_key_frames)]

        key_frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            success, frame = cap.read()
            if success:
                key_frames.append(frame)

        cap.release()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for i, frame in enumerate(key_frames):
            frame_filename = f"{output_directory}/frame_{i}.jpg"
            cv2.imwrite(frame_filename, frame)

        self.key_frames = key_frames
