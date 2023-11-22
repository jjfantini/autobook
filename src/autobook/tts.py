from autobook.core.env import Env
from openai import OpenAI


class SpeechGenerator:
    def __init__(self, api_key: str, model: str = "tts-1-hd", voice="nova"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.voice = voice

    def generate_speech(self, text, file_path):
        response = self.client.audio.speech.create(
            model=self.model, voice=self.voice, input=text
        )
        response.stream_to_file(file_path)


def main():
    api_key = Env().OPENAI_API
    speech_generator = SpeechGenerator(api_key)

    text = """He escorts five fifth graders from the elementary school to the public library through curtains of falling snow. He is an octogenarian in a canvas coat; his boots are fastened with Velcro; cartoon penguins skate across his necktie. All day, joy has steadily inflated inside his chest, and now, this afternoon, at 4:30 p.m. on a Thursday in February, watching the children"""
    speech_file_path = "test2.mp3"

    speech_generator.generate_speech(text, speech_file_path)
    print("----Success----")


if __name__ == "__main__":
    main()
