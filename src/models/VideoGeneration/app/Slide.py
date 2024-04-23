from moviepy.editor import ImageClip,AudioFileClip, concatenate_videoclips
from moviepy.audio.AudioClip import AudioArrayClip
import matplotlib.pyplot as plt
import numpy as np

class Slide:
    def __init__(self, title, bullet_points, audio_array,audio_path):
        self.title = title
        self.bullet_points = bullet_points
        # reshape audio array to be size (N x 1) if necessary
        self.audio_array = audio_array if len(audio_array.shape) == 2 else audio_array.reshape(audio_array.shape[0],1)
        self.audio_path = audio_path

    def generate_img(self):
        fig, ax = plt.subplots()
        ax.set_title(self.title)
        for idx, bp in enumerate(self.bullet_points):
            ax.text(0.05, 0.9 - idx * 0.1, f"- {bp}", fontsize=12, transform=ax.transAxes)
        ax.axis('off') 

        # Convert Matplotlib figure to a NumPy array
        fig.canvas.draw()
        img_data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img_data = img_data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        plt.close()
        return img_data

    """def get_slide_duration(self):
        audio = AudioSegment.from_file(self.audio_path)
        return len(audio)"""
    
    @staticmethod
    def generate_video_from_slides(slides,video_name):
        clips = []
        for slide in slides:
            #slide_duration = slide.get_slide_duration()
            slide_img = slide.generate_img()
            #audio_clip = AudioArrayClip(slide.audio_array,fps = 32000)
            audio_clip = AudioFileClip(slide.audio_path)
            slide_clip = ImageClip(slide_img,duration = audio_clip.duration)
            slide_clip = slide_clip.set_audio(audio_clip)
            print(slide_clip.duration)
            clips.append(slide_clip)
        final_clip = concatenate_videoclips(clips)
        # export video
        final_clip.write_videofile(video_name, fps=24)