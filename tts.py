#!/usr/bin/env python3

#ESPnet2-TTS realtime demonstration
#https://colab.research.google.com/github/espnet/notebook/blob/master/espnet2_tts_realtime_demo.ipynb

import time
import torch
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.tts_inference import Text2Speech
from parallel_wavegan.utils import download_pretrained_model
from parallel_wavegan.utils import load_model
from soundfile import write as sfwrite

class TTS_Worker:
    def __init__(self, worker_id=1, audio_dest='audio/', audio_format='.wav'):
        self.id = worker_id
        #Model selection
        self.fs = 22050
        self.lang = "English"
        self.tag = "kan-bayashi/ljspeech_tacotron2"
        self.vocoder_tag = "ljspeech_parallel_wavegan.v1"

        #Model setup
        self.d = ModelDownloader()
        self.text2speech = Text2Speech(
            **self.d.download_and_unpack(self.tag),
            device="cpu",
            # Only for Tacotron 2
            threshold=0.5,
            minlenratio=0.0,
            maxlenratio=10.0,
            use_att_constraint=False,
            backward_window=1,
            forward_window=3,
        )
        self.vocoder = load_model(download_pretrained_model(self.vocoder_tag)).to("cpu").eval()
        
        self.text2speech.spc2wav = None
        self.vocoder.remove_weight_norm()

        self.audio_d = audio_dest
        self.audio_f = audio_format

    def process_text(self, text, dest):
        print(f'Worker {self.id} attempting : {text}')
        with torch.no_grad():
            #start = time.time()
            wav, c, *_ = self.text2speech(text)
            wav = self.vocoder.inference(c)
        #rtf = (time.time() - start) / (len(wav) / self.fs)
        #print(f"RTF = {rtf:5f}")

        #Output generation
        wav = wav.view(-1).cpu().numpy()
        sfwrite(self.audio_d + dest + self.audio_f, wav, self.fs)
        print(f'Worker {self.id} finished : {text}')


if __name__ == '__main__':
    #Test user input
    worker = TTS_Worker(1, 'audio/', '.wav')
    print(f"Input your favorite sentence.")
    x = input()
    start = time.time()
    worker.process_text(x, 'test')
    rtf = (time.time() - start)
    print(f"RTF = {rtf:5f}")

