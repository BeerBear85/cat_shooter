import time
import pigpio
import logging
import threading

logger = logging.getLogger(__name__)
pi = pigpio.pi()

if not pi.connected:
    print("No connection the to Raspberry IO ports")
    #exit(-1)

class Shooter:
    def __init__(self):
        self.control_pin = 24
        self.shoot_duration = 0.5 #[s]

        pi.set_mode(self.control_pin, pigpio.OUTPUT)  # Set GPIO pin as output

    def shoot(self):
        pi.write(self.control_pin, 1)
        time.sleep(self.shoot_duration)
        pi.write(self.control_pin, 0)

    def turn_off(self):
        pi.write(self.control_pin, 0)


class Servo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Range paramerets
        self.user_max_negative_angle = -45
        self.user_max_positive_angle = 45
        
        #Servo/Arduino HW config
        self.control_pin = 18
        self.servo_min_angle = -90
        self.servo_max_angle = 90
        self.max_command = 2290
        self.min_command = 700
        self.command_conversion_factor = (self.max_command - self.min_command) / (self.servo_max_angle - self.servo_min_angle)
    
        # Sweep parameters
        self.sweep_speed = 20 # deg/s
        self.sweep_delta_time = 1.0 # [s]
        self.positive_sweep_direction = True #Start direction
        self.sweep_angle_delta = self.sweep_speed * self.sweep_delta_time # Angle sweep step size

        # Parameter check
        if (self.user_max_negative_angle < self.servo_min_angle) or \
            (self.user_max_positive_angle > self.servo_max_angle):
            print("Illegal angle parameters!")
            exit(-1)

        # Member variables
        self.current_angle = 0
        self.sweep_on = False
        self.enable_thread_run = True
        
        # start thread
        self.start()

    def set_angle(self, arg_angle):
        tmp_angle = arg_angle
        
        if tmp_angle > self.user_max_positive_angle:
            tmp_angle = self.user_max_positive_angle
        elif tmp_angle < self.user_max_negative_angle:
            tmp_angle = self.user_max_negative_angle
        
        tmp_servo_midpoint_command = (self.min_command + self.max_command) / 2
        tmp_servo_command = int(tmp_angle * self.command_conversion_factor + tmp_servo_midpoint_command)
        
        print("Setting angle to %d, using command value: %d" %(tmp_angle, tmp_servo_command))
        
        pi.set_servo_pulsewidth(self.control_pin, tmp_servo_command)
        
        self.current_angle = tmp_angle
        
    def standby(self, arg_standby):
        if arg_standby:
            self.enable_thread_run = True
            self.set_angle(0)
        else:
            self.enable_thread_run = False
            self.set_angle(0)
            time.sleep(0.1) # allow time to reset angle
            pi.set_servo_pulsewidth(self.control_pin, 0) # turn off

    def toggle_sweep(self, arg_start_stop):
        if arg_start_stop:
            print("Starting sweep")
            self.sweep_on = True
        else:
            print("Sweep off")
            self.sweep_on = False


    def __iterate_sweep(self):
        tmp_angle = self.current_angle
        if self.positive_sweep_direction:
            tmp_angle += self.sweep_angle_delta
        else:
            tmp_angle -= self.sweep_angle_delta

        if self.current_angle >= self.user_max_positive_angle:
            self.positive_sweep_direction = False
        elif self.current_angle <= self.user_max_negative_angle:
            self.positive_sweep_direction = True

        self.set_angle(tmp_angle)

    # Function run by thread start()
    def run(self):
        while self.enable_thread_run:
            if self.sweep_on:
                self.__iterate_sweep()

            time.sleep(self.sweep_delta_time)