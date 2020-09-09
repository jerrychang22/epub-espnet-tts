#!/usr/bin/env python3

#Multiple producer, single consumer

from multiprocessing import Process, Queue
from tts import TTS_Worker
import simpleaudio as sa
import os
import time

class Factory:

    def __init__(self, n_producers, audio_dest='audio/', audio_format='.wav'):
        print('Initializing factory')
        self.n_workers = n_producers
        self.input_q = Queue()
        self.output_q = Queue()
        self.producers = []
        
        for i in range(self.n_workers):
            print(f'Setting up worker {i+1}')
            self.producers.append(Process(target=self.producer, args=(i, self.input_q, self.output_q)))

        self.consumer_p = Process(target=self.consumer, args=(self.output_q,))

        self.audio_d = audio_dest
        self.audio_f = audio_format

        self.max_i = 1

    def producer(self, i, input_q, output_q):
        worker = TTS_Worker(i+1)
        while True:
            item = input_q.get()
            if item is None:
                return

            name = str(item[0])
            worker.process_text(item[1], name)
            output_q.put(name)

    def consumer(self, output_q):
        wav_list = []
        consumer_i = 1
        while True:
            item = output_q.get()
            if (item == None): 
                return

            wav_list.append(item)
            if str(consumer_i) in wav_list:
                wav = self.audio_d + item + self.audio_f
                wave_obj = sa.WaveObject.from_wave_file(wav)
                play_obj = wave_obj.play()
                play_obj.wait_done()

                os.remove(wav)
                wav_list.remove(str(consumer_i))
                consumer_i = consumer_i + 1


    def start(self):
        for p in self.producers:
            p.start()
        self.consumer_p.start()

    def add_items(self, data):
        for i in range(len(data)):
            item = (i + self.max_i, data[i])
            self.input_q.put(item)

        self.max_i += len(data)

    def terminate(self):
        for _ in range(self.n_workers):
            self.input_q.put(None)

        for p in self.producers:
            p.join()

        self.output_q.put(None)
        self.consumer.join()

if __name__ == '__main__':
    wave_obj = sa.WaveObject.from_wave_file('audio/test.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()
    print('Audio played')
   
