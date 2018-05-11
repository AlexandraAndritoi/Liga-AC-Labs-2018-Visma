from Motor import Motor
from DistSensor import DistSensor
from multiprocessing.pool import ThreadPool
import RPi.GPIO as GPIO


class Car:
    def __init__(self,m1_forward,m1_backward,
                 m2_forward,m2_backward,
                 m3_forward,m3_backward,
                 m4_forward,m4_backward,
                 front_trig,front_echo,
                 side_trig,side_echo,
                 back_trig,back_echo):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) #BCM=Name Raspberry PORT

        self.motor1=Motor(m1_forward,m1_backward)
        self.motor2=Motor(m2_forward,m2_backward)
        self.motor3=Motor(m3_forward,m3_backward)
        self.motor4=Motor(m4_forward,m4_backward)

        self.front_sensor=DistSensor(front_trig,front_echo)
        self.side_sensor=DistSensor(side_trig,side_echo)
        self.back_sensor=DistSensor(back_trig,back_echo)

        #Pool size=number of distance sensors
        dist_sensor_count=3
        self.pool=ThreadPool(dist_sensor_count)

    def move_forward(self):
        self.motor1.move_forward()
        self.motor2.move_forward()
        self.motor3.move_forward()
        self.motor4.move_forward()

    def move_backward(self):
        self.motor1.move_backward()
        self.motor2.move_backward()
        self.motor3.move_backward()
        self.motor4.move_backward()

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def  dist(self,sensor):
        return sensor.read_distance()

    def read_distances(self):
        #s1=self.front_sensor.read_distance()
        #s2=self.back_sensor.read_distance()
        #s3=self.side_sensor.read_distance()

        async_front=self.pool.apply_async(self.dist,(self.front_sensor,))
        async_side=self.pool.apply_async(self.dist,(self.side_sensor,))
        async_back=self.pool.apply_async(self.dist,(self.back_sensor,))

        return async_front.get(),async_side.get(),async_back.get()

    def cleanup(self):
        GPIO.cleanup()