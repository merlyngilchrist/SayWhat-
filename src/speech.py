import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from transformers import AutoTokenizer

class SpeechRecognition:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15", sample_rate=16000):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate
        self.audio_queue = queue.Queue()
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    def audio_callback(self, indata, frames, time, status):
        """ Callback function to capture audio data in real-time """
        if status:
            print(f"Audio Error: {status}")
        self.audio_queue.put(bytes(indata))

    def detect_language(self, text):
        """ Use NLLB-200 tokenizer to detect language """
        tokens = self.tokenizer(text, return_tensors="pt")
        detected_lang = tokens.get("lang", ["unknown"])[0]
        return detected_lang

    def recognize_speech(self):
        """ Continuously proccesses audio and returns recognized text """
        with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000, dtype='int16', channels=1, callback=self.audio_callback):
            print("Listening... (Press Ctrl+C to stop)")

            while True:
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    recognized_text = result.get("text", "")
                    if recognized_text.strip():
                        lang = self.detect_language(recognized_text)
                        print(f"Recongnized: {recognized_text} | Language: {lang}")
                        yield recognized_text, lang
            
if __name__ == "__main__":
    speech_recognizer = SpeechRecognition()
    try:
        for text in speech_recognizer.recognize_speech():
            pass #
    except KeyboardInterrupt:
        print("\n Stopping...")