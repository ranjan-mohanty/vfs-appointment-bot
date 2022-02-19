import time

def countdown(t):
    while t > -1:
        timer = 'Retry after {:02d} seconds'.format(t)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1