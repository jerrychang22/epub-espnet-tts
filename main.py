#!/usr/bin/env python3

from mpsc import Factory

def main():

    f = open("test.txt", 'r')
    data = f.read().split('.')
    print('Preprocessing data')

    n_producers = 1
    print(f'Setting up {n_producers} producers\n')
    
    engine = Factory(n_producers)
    
    print('Adding data')
    engine.add_items(data)

    print('Starting TTS')
    engine.start()

    print('Stopping engine')
    engine.terminate()

if __name__ == '__main__':
    main()
