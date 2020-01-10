import matplotlib.pyplot as plt
import numpy as np
import time
import os


def initialize(n):
    ca = np.zeros((n), dtype=np.int32)
    ca[len(ca)//2] = 1
    return ca

def plot(ca, hold_time=0.05):
    def press(event):
        if event.key == 'q':
            os.sys.exit('Exiting...')

    if plot.data is None:
        # Setup figure
        n = len(ca)
        plot.data = np.zeros((int(n//2), n))
    else:
        if plot.i < int(len(ca)//2):
            plot.data[plot.i,:] = ca.copy()
            plot.i += 1
        else:
            # Shift all data
            plot.data[:-1,:] = plot.data[1:,:]
            plot.data[-1, :] = ca.copy()


    figure = plt.figure(1)
    figure.canvas.mpl_connect('key_press_event', press)
    plt.axis('off')
    plt.imshow(plot.data, cmap='gray', vmin=0, vmax=1)
    plt.pause(hold_time)
plot.data = None
plot.i = 0

def run_rule(a, b, c, rule):
    n = a*(1<<2) + b*(1<<1) + c*(1<<0)
    return (rule >> n) & 1

def update(ca, rule, bc=0):
    n = len(ca)
    new = ca.copy()

    for i in range(1, n-1):
        new[i] = run_rule(ca[i-1], ca[i], ca[i+1], rule)
    new[0] = run_rule(bc, ca[0], ca[0+1], rule)
    new[n-1] = run_rule(ca[n-2], ca[n-1], bc, rule)

    return new

def print_rule(rule):
    x = [0,1]
    for a in x:
        for b in x:
            for c in x:
                res = run_rule(a,b,c, rule=rule)
                print('  [{}, {}, {}] -> {}'.format(a, b, c, res))

def main(iterations=128, sleep_time=0.1, rule=30):
    print('Rule:')
    print_rule(rule)
    print('')

    ca = initialize(iterations)

    plot(ca)
    for _ in range(int(iterations//2)):
        ca = update(ca, rule)
        plot(ca)
        time.sleep(sleep_time)
    plt.show()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='ca',
        description='''Wolfram cellular automaton

Run a Wofram style cellular automaton.
'''
    )
    parser.add_argument('--iterations', '-n', default=128, type=int, help='Number of iterations')
    parser.add_argument('--sleep_time', default=0.1, type=float, help='Time to sleep between iterations')
    parser.add_argument('--rule', default=30, type=int, help='Rule to run, in range 0-255')
    args = parser.parse_args()

    main(**vars(args))

