import RPi.GPIO as GPIO
from time import sleep
import time

class DistanceSensor:
    def __init__(self, trig_pin = 14, echo_pin = 15, timeout = 0.1):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.timeout = timeout
        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def getDistance(self):
        GPIO.output(self.trig_pin, GPIO.LOW)
        sleep(0.05)

        GPIO.output(self.trig_pin, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        start_time = time.time()
        max_wait = start_time + self.timeout

        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
            if pulse_start > max_wait:
                return None # Timeout

        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
            if pulse_end > max_wait:
                return None # Timeout

        duration = pulse_end - pulse_start
        distance = duration * 17150

        return (round(distance, 2))

if __name__ == '__main__':
    try:
        sensor = DistanceSensor()
        while True:
            print(sensor.getDistance())
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()