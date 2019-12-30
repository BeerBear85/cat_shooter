import time
import pigpio

pi = pigpio.pi()

if not pi.connected:
    print("No connection the to Raspberry IO ports")
    exit()
    
LED_pin = 24



class servo():
    def __init__(self):
        self.control_pin = 18
        
        #Servo/Arduino HW config
        self.mServoMinAngle = -90;
        self.mServoMaxAngle = 90;
        self.mMaxCommand = 2290;
        self.mMinCommand = 700;
        self.mCommandConversionFactor = (self.mMaxCommand - self.mMinCommand)/(self.mServoMaxAngle - self.mServoMinAngle);
        
        print(self.mCommandConversionFactor)
        
        self.m_current_angle = 0
    
        # Sweep parameters
        self.mSweepSpeed = 50; #deg/s
        self.mSweepDeltaTime = 0.2; #[ss]
        self.mPositiveSweepDirection = True; #Start direction
        self.mSweepAngleDelta = self.mSweepSpeed * self.mSweepDeltaTime; # Angle sweep step size

    def setAngle(self, arg_angle):
        tmp_angle = arg_angle;
        
        if(tmp_angle > self.mServoMaxAngle):
            tmp_angle = self.mServoMaxAngle
        elif (tmp_angle < self.mServoMinAngle):
            tmp_angle = self.mServoMinAngle
        
        tmp_servo_midpoint_command = (self.mMinCommand + self.mMaxCommand)/2
        tmp_servo_command = int(tmp_angle*self.mCommandConversionFactor + tmp_servo_midpoint_command)
        
        print("Setting angle to %d, using command value: %d" %(tmp_angle, tmp_servo_command))
        
        pi.set_servo_pulsewidth(self.control_pin, tmp_servo_command)
        
        self.m_current_angle = tmp_angle
        
    def standby(self, arg_standby):
        if arg_standby:
            self.setAngle(0)
        else:
            self.setAngle(0)
            time.sleep(0.1) # allow time to reset angle
            pi.set_servo_pulsewidth(self.control_pin, 0) # turn off
    


pi.set_mode(LED_pin, pigpio.OUTPUT) # Set GPIO pin as output

def test(arg_on):
    my_servo = servo()
    if arg_on:
        pi.write(LED_pin, 1)
        my_servo.setAngle(-90)
    else:
        pi.write(LED_pin, 0)
        my_servo.setAngle(90)

def standby(arg_standby):
    my_servo = servo()
    my_servo.standby(arg_standby)
    if arg_standby:
        pi.write(LED_pin, 1)
    else:
        pi.write(LED_pin, 0)
    