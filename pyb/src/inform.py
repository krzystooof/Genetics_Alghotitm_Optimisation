import pyb


class Inform:
    state: int = 0

    @staticmethod
    def waiting():  # green on
        state = 0
        pyb.LED(1).on()
        pyb.LED(2).off()
        pyb.LED(3).off()

    @staticmethod
    def running():  # blue on
        state = 1
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).off()

    @staticmethod
    def error():  # red on
        state = 2
        pyb.LED(1).off()
        pyb.LED(2).off()
        pyb.LED(3).on()

    @staticmethod
    def connected():  # quick flash green, blued
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).on()
        Inform.correct_led()

    @staticmethod
    def correct_led():
        if Inform.state == 0:
            Inform.waiting()

        if Inform.state == 1:
            Inform.running()

        if Inform.state == 2:
            Inform.error()
