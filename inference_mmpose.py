import gradio as gr

import os
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *

import sys

sys.path.append("FollowYourPose")


def get_frames(video_in):
    frames = []
    # resize the video
    clip = VideoFileClip(video_in)
    start_frame = 0  # 起始帧数
    end_frame = 50  # 结束帧数

    if not os.path.exists("./raw_frames"):
        os.makedirs("./raw_frames")

    if not os.path.exists("./mmpose_frames"):
        os.makedirs("./mmpose_frames")

    # check fps
    if clip.fps > 30:
        print("vide rate is over 30, resetting to 30")
        clip_resized = clip.resize(height=512)
        clip_resized = clip_resized.subclip(
            start_frame / clip_resized.fps, end_frame / clip_resized.fps
        )  # subclip 2 seconds
        clip_resized.write_videofile("./video_resized.mp4", fps=30)
    else:
        print("video rate is OK")
        clip_resized = clip.resize(height=512)
        clip_resized = clip_resized.subclip(
            start_frame / clip.fps, end_frame / clip.fps
        )  # subclip 5 seconds
        clip_resized.write_videofile("./video_resized.mp4", fps=clip.fps)

    print("video resized to 512 height")

    # Opens the Video file with CV2
    cap = cv2.VideoCapture("./video_resized.mp4")

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("video fps: " + str(fps))
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite("./raw_frames/kang" + str(i) + ".jpg", frame)
        frames.append("./raw_frames/kang" + str(i) + ".jpg")
        i += 1

    cap.release()
    cv2.destroyAllWindows()
    print("broke the video into frames")

    return frames, fps


def create_video(frames, fps, type):
    print("building video result")
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(type + "_result.mp4", fps=fps)

    return type + "_result.mp4"
