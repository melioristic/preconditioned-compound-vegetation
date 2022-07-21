import math
import time

_start_time = time.time()


def tic():
    global _start_time
    _start_time = time.time()


def tac():
    diff = time.time() - _start_time
    t_sec = math.floor(diff)
    t_msec = diff - t_sec
    (t_min, t_sec) = divmod(t_sec, 60)
    (t_hour, t_min) = divmod(t_min, 60)
    print(f'Time passed: {t_hour} hour {t_min} min {t_sec} sec {t_msec*1000:.0f} msec')
