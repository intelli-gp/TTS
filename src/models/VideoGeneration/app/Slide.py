
from moviepy.editor import ImageClip,AudioFileClip, concatenate_videoclips
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from ImageMatcher import ImageMatcher
import numpy as np

class Slide:
    LINE_LMT = 75
    LINE_VERTICAL_DIST = 0.35
    MIN_CONFIDENCE = 0.25
    Y_POS_MIN = 0.25
    Y_POS_IMG_MIN = 0.4
    def __init__(self, title, bullet_points,audio_path):
        self.title = title
        self.bullet_points = bullet_points
        # reshape audio array to be size (N x 1) if necessary
        #self.audio_array = audio_array if len(audio_array.shape) == 2 else audio_array.reshape(audio_array.shape[0],1)
        self.audio_path = audio_path

    def __chucnk_bp(self,str):
        vertical_off = 0
        if(len(str) > Slide.LINE_LMT):
            new_str = ""
            i = 0
            while(i < len(str)):
                print(f"before {i}")
                vertical_off = vertical_off + Slide.LINE_VERTICAL_DIST
                upper_limit = i+Slide.LINE_LMT if i+Slide.LINE_LMT < len(str) else len(str)
                curr_line = str[i:upper_limit]
                if curr_line[-1] != ' ' and upper_limit != len(str):
                    print(curr_line)
                    # length of last word
                    word_offset = len(curr_line.split(" ")[-1])
                    print(word_offset)
                    upper_limit = upper_limit-word_offset
                    print(f"after {i}")
                new_str = new_str +" \n" + str[i:upper_limit] if(i > 0) else str[i:upper_limit]
                i = upper_limit
            return new_str,vertical_off
        return str,vertical_off
    
    def __find_query(self):
        if len(self.bullet_points) == 0 or len(self.bullet_points[0]) ==0:
            return self.title
        else:
            return self.bullet_points[0]
        
    def __match_slide_img(self):
        image_matcher = ImageMatcher()
        confidence,img = image_matcher.match_best_image(self.__find_query())
        print(f"Confidence is: {confidence}")
        if confidence > Slide.MIN_CONFIDENCE:
            return img
        return None
    
    def generate_img(self):
        fig, ax = plt.subplots()
        title,total_y_off  = self.__chucnk_bp(self.title)
        ax.set_title(title, wrap=True, loc='center',y = 1 - total_y_off*0.1)
        x_pos = -0.1
        y_pos = 0.9
        for idx, bp in enumerate(self.bullet_points):
            if(len(bp)>0):
                text, vertical_off = self.__chucnk_bp(bp)
                total_y_off = total_y_off + vertical_off
                y_pos = 0.9 - (idx+total_y_off) * (0.1)
                if (y_pos < Slide.Y_POS_MIN):
                    print("Passed Limit for Text")
                    break
                print(y_pos)
                ax.text(x_pos, y_pos, f"- {text}", fontsize=10, transform=ax.transAxes)
        #actual_img = self.match_slide_img() 
        # replace later
        
        actual_img = self.__match_slide_img() if y_pos > Slide.Y_POS_IMG_MIN else None
        if actual_img != None:
            resized_img = np.array(actual_img.resize((400, 180)))
                    # Set custom position for the image (normalized coordinates)
            x_position = 0.5  # Adjust x position (0.0 to 1.0)
            y_position = y_pos  # Adjust y position (0.0 to 1.0)
            
            zoom = 1
            # Create an OffsetImage object
            imagebox = OffsetImage(resized_img, zoom=zoom)  # Adjust zoom as needed
            image_height = resized_img.shape[0] * zoom / fig.get_figheight() / fig.dpi
            y_position -= image_height
            # Create an AnnotationBbox object with the image
            ab = AnnotationBbox(imagebox, (x_position, y_position),
                                frameon=False,  # No box around the image
                                xycoords='axes fraction')  # Coordinates are in fraction of axes
            # Add the AnnotationBbox to the plot
            ax.add_artist(ab)

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
    def generate_video_from_slides(slides,video_path):
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
        final_clip.write_videofile(video_path, fps=24)
        """
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

    def get_slide_duration(self):
        audio = AudioSegment.from_file(self.audio_path)
        return len(audio)
    
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
        final_clip.write_videofile(video_name, fps=24)"""