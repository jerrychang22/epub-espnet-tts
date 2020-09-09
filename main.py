#!/usr/bin/env python3

import signal
import sys
from mpsc import Factory

engine = 0

def signal_handler(sig, frame):
    print("Terminating engine")
    engine.terminate()
    sys.exit(0)

def main():
    f = open("test.txt", 'r')
    data = f.read().split('.')
    print('Preprocessing data')

    n_producers = 1
    print(f'Setting up {n_producers} producers')
    
    global engine 
    engine = Factory(n_producers)

    print('Adding data')
    engine.add_items(data)

    print('Starting TTS')
    engine.start()

    #print('Stopping engine')
    #engine.terminate()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
