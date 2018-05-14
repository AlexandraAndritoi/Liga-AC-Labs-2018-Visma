import RPi.GPIO as GPIO

class Motor:

    def __init__(self, forward_pin, backward_pin):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin

        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)

        GPIO.output(forward_pin, GPIO.LOW)
        GPIO.output(backward_pin, GPIO.LOW)


    def move_forward(self):
        GPIO.output(self.forward_pin, GPIO.HIGH)
        GPIO.output(self.backward_pin, GPIO.LOW)

    def move_backward(self):
        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.backward_pin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.backward_pin, GPIO.LOW)