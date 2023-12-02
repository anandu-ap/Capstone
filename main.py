import cv2
import numpy as np
from collage import Collage
from frameExtractor import FrameExtractor


if __name__ == "__main__":
    
    video_path = input("Video file path : ") # Input video
    output_directory = "output" # output directory
    num_frames = int(input("Number of frames : "))  # Total number of key frames to extract

    # extracting the key frames from video
    fe = FrameExtractor()
    print("Extracting the key frames.........")
    fe.extract_key_frames(video_path, output_directory, num_frames)
    print("Key frames extracted.")

    i_frames = fe.key_frames

    h, w, ch = i_frames[0].shape
    alpha = w/h # aspect ratio of frames


    # Contructing the collage
    collageObj = Collage(1, alpha, num_frames)

    print("Creating collage.........")
    collageObj.constructCollage(i_frames, False)
    print("Collage created.")
    collage = collageObj.getCollage()

    # Saving the collage to device
    frame_filename = f"{output_directory}/collage.jpg"
    print("Saving the collage to device....")
    cv2.imwrite(frame_filename, collage)
    print("Collage saved to device.")

    # Showing the final collage
    cv2.imshow('Image', collage)

    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

