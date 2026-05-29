import smbus2
from time import sleep
from RPi import GPIO

class LCD:
    def __init__(self, name, bus=1):
        self.name = name
        self.lcd_init()
        self.bus = bus

    I2C_ADDR = 0x27
    LCD_WIDTH = 16
    LCD_CHR = True
    LCD_CMD = False
    LCD_LINE_1 = 0x80 | 0
    LCD_LINE_2 = 0x80 | 0x40
    LCD_BACKLIGHT = 0x08
    LCD_RW = 0b00
    ENABLE = 0x04

    E_PULSE = 0.0002
    E_DELAY = 0.0002

    bus = 1
    i2c = smbus2.SMBus(bus)

    def set_data_bits(self, value, mode):
        MSNibble = value & 0xF0
        LSNibble = (value & 0x0F) << 4
        self.send_byte_with_e_toggle(MSNibble | self.LCD_BACKLIGHT | mode)
        self.send_byte_with_e_toggle(LSNibble | self.LCD_BACKLIGHT | mode)


    def send_byte_with_e_toggle(self, bits):
        sleep(self.E_DELAY)
        # write data to i2c with E bit HIGH
        self.i2c.write_byte(self.I2C_ADDR, bits | self.ENABLE)
        sleep(self.E_PULSE)
        # write data to i2c with E bit LOW
        self.i2c.write_byte(self.I2C_ADDR, bits & (~self.ENABLE & 0xFF))
        sleep(self.E_DELAY)

    def send_instruction(self, data):
        self.set_data_bits(data, self.LCD_CMD)


    def send_character(self, data):
        self.set_data_bits(data, self.LCD_CHR)


    def send_string(self, text, line=1):
        if line == 1:
            line = self.LCD_LINE_1
        elif line == 2:
            line = self.LCD_LINE_2
        self.send_instruction(line)
        spaces = " " * (self.LCD_WIDTH - len(text))
        text = text + spaces
        for char in text:
            self.send_character(ord(char))

        # If text on first line is longer than LCD_WIDTH, move to second line
        if len(text) > self.LCD_WIDTH and line == self.LCD_LINE_1:
            self.send_instruction(self.LCD_LINE_2)
            text = text[self.LCD_WIDTH:]
            spaces = " " * (self.LCD_WIDTH - len(text))
            text = text + spaces
            for char in text:
                self.send_character(ord(char))

    def lcd_init(self):
        self.send_byte_with_e_toggle(0x30)
        self.send_byte_with_e_toggle(0x30)
        self.send_byte_with_e_toggle(0x20)

        self.send_instruction(0x0F)
        self.send_instruction(0x28)
