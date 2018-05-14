from motor import Motor
from dist_sensor import DistSensor
from multiprocessing.pool import ThreadPool
import RPi.GPIO as GPIO


class Car:
    min_stop_sensor_dist = 25
    """Distance given in centimeters"""

    def __init__(self, m1_forward, m1_backward,
                 m2_forward, m2_backward,
                 m3_forward, m3_backward,
                 m4_forward, m4_backward,
                 front_trig, front_echo,
                 side_trig, side_echo,
                 back_trig, back_echo):
        GPIO.setmode(GPIO.BCM)

        self.motor1 = Motor(m1_forward, m1_backward)
        self.motor2 = Motor(m2_forward, m2_backward)
        self.motor3 = Motor(m3_forward, m3_backward)
        self.motor4 = Motor(m4_forward, m4_backward)

        self.front_sensor = DistSensor(front_trig, front_echo)
        self.side_sensor = DistSensor(side_trig, side_echo)
        self.back_sensor = DistSensor(back_trig, back_echo)

        self.running = False

        # Pool size = number of distance sensors
        dist_sensor_count = 3
        self.pool = ThreadPool(dist_sensor_count)


    def move_forward(self):
        print('Moving the car forward ...')
        self.motor1.move_forward()
        self.motor2.move_forward()
        self.motor3.move_forward()
        self.motor4.move_forward()

    def move_backward(self):
        print('Moving the car backward ...')
        self.motor1.move_backward()
        self.motor2.move_backward()
        self.motor3.move_backward()
        self.motor4.move_backward()

    def stop(self):
        print('Stopping the car ...')
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def read_distance(self, sensor):
        return sensor.read_distance()

    def read_distances(self):
        # s1 = self.front_sensor.read_distance()
        # s2 = self.side_sensor.read_distance()
        # s3 = self.back_sensor.read_distance()

        async_front = self.pool.apply_async(self.read_distance, (self.front_sensor, ))
        async_side = self.pool.apply_async(self.read_distance, (self.side_sensor, ))
        async_back = self.pool.apply_async(self.read_distance, (self.back_sensor, ))

        front_dist = async_front.get()
        side_dist = async_side.get()
        back_dist = async_back.get()

        emergency_stop_front = front_dist < Car.min_stop_sensor_dist
        emergency_stop_side = side_dist < Car.min_stop_sensor_dist
        emergency_stop_back = back_dist < Car.min_stop_sensor_dist

        print("Front = %.2f cm, side = %.2f cm, back %.2f cm" \
              % (front_dist, side_dist, back_dist))

        return front_dist, side_dist, back_dist, emergency_stop_front, emergency_stop_side, emergency_stop_back

    def cleanup(self):
        GPIO.cleanup()
