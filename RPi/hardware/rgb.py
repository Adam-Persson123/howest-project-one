from RPi import GPIO

class RGB:
    def __init__(self, red = 5, green = 6, blue = 13):
        self.red = red
        self.green = green
        self.blue = blue

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)

        self.pwm_red = GPIO.PWM(red, 1000)
        self.pwm_red.start(100)
        self.pwm_green = GPIO.PWM(green, 1000)
        self.pwm_green.start(100)
        self.pwm_blue = GPIO.PWM(blue, 1000)
        self.pwm_blue.start(100)

    def set_color(self, red, green, blue):
        self.pwm_red.ChangeDutyCycle(100 - (red / 255 * 100))
        self.pwm_green.ChangeDutyCycle(100 - (green / 255 * 100))
        self.pwm_blue.ChangeDutyCycle(100 - (blue / 255 * 100))