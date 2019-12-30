
import pigpio


pi = pigio.pi()

if not pi.connected:
    print("No connection the to Raspberry IO ports")
    exit()

pi.set_mode(18, pigpio.OUTPUT) # Set GPIO pin as output
pi.set_mode(24, pigpio.OUTPUT) # Set GPIO pin as output

def test(arg_on):
    if arg_on:
        pi.write(18, 1)
        pi.write(24, 1)
    else:
        pi.write(18, 0)
        pi.write(24, 0)
