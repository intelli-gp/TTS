import json
import subprocess

class slide:
    def __init__(self, title, points, text):
        self.title = title
        self.points = points
        self.text = text

def request_video_link(slides):
    slides_data = [{"title": slide.title, "points": slide.points, "text": slide.text} for slide in slides]
    payload = {"slides": slides_data}
    payload_json = json.dumps(payload)
    api_url = "http://104.41.151.128:8800/tts"
    command = [
        "curl", "-X", "POST", api_url,
        "-H", "accept: application/json",
        "-H", "Content-Type: application/json",
        "-d", payload_json
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    slides = [
    slide(
        title="Unlocking the Magic of Machine Learning",
        points=[],
        text="Unlocking the Magic of Machine Learning"
    ),
    slide(
        title="Table Of Contents",
        points=[
            "*What is Machine Learning?* (Definition, types, key concepts)",
            "*How Machine Learning Works:* (Algorithms, data usage, training process)",
            "*Applications of Machine Learning:* (Realworld examples in various fields)",
            "*Benefits and Challenges of Machine Learning:* (Efficiency, insights, bias, ethical considerations)",
            "*Future of Machine Learning:* (Emerging trends, potential impact)"
        ],
        text=(
            "*What is Machine Learning?* (Definition, types, key concepts)"
            "*How Machine Learning Works:* (Algorithms, data usage, training process)"
            "*Applications of Machine Learning:* (Realworld examples in various fields)"
            "*Benefits and Challenges of Machine Learning:* (Efficiency, insights, bias, ethical considerations)"
            "*Future of Machine Learning:* (Emerging trends, potential impact)"
        )
    ),
    slide(
        title="Introduction",
        points=[
            "\n\nIntroduction to machine learning",
            "\nFundamental concepts, inner workings, and realworld applications\n",
            "Benefits and challenges",
            "Future of machine learning"
        ],
        text=(
            "\n\nWelcome, everyone! Today, we're diving into the fascinating world of *machine learning. "
            "This presentation will demystify this transformative technology, exploring its **fundamental concepts, "
            "inner workings, and real-world applications.* We'll also examine the *remarkable benefits and inherent "
            "challenges* that come with machine learning, concluding with a glimpse into its *exciting future.* Let's concluding with a glimpse into its *exciting future.* Let's  concluding with a glimpse into its *exciting future.* Let's "
            "begin unlocking the magic!\n\n"
            )   
        )
    ]
    print(request_video_link(slides))