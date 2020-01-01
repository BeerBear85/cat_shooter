import turrent_driver as turrent
import time
import logging

logging.basicConfig(filename = 'debug.log',
                    level = logging.DEBUG,
                    format = '%(asctime)s:%(levelname)-8s:%(name)s:%(message)s:%(filename)s:%(lineno)s',
                    filemode = 'w')

my_servo = turrent.Servo()
my_shooter = turrent.Shooter()

my_servo.standby(True)
#time.sleep(1)
#my_servo.set_angle(-90)
#my_shooter.shoot()
#time.sleep(1)
#my_servo.set_angle(0)
#my_shooter.shoot()
#time.sleep(1)
#my_servo.set_angle(90)
#my_shooter.shoot()
#time.sleep(1)
#my_servo.set_angle(-90)
#my_shooter.shoot()
#time.sleep(1)
#my_servo.standby(False)
#my_shooter.turn_off()

my_shooter.shoot()
time.sleep(2)

my_servo.standby(True)
my_servo.toggle_sweep(True)
time.sleep(10)
my_shooter.shoot()
my_servo.toggle_sweep(False)
time.sleep(1)
my_servo.standby(False)