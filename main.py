import turrent_driver as turrent
import time

turrent.standby(True)
time.sleep(1)
turrent.test(True)
time.sleep(1)
turrent.test(False)
time.sleep(1)
turrent.test(True)
time.sleep(1)
turrent.test(False)
time.sleep(1)
turrent.standby(False)