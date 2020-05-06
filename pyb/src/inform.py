"""
Contains Inform class
"""
import pyb


class Inform:
    """
    This class is used to signalize pyboard status. It is fully static to optimize runtime.
    Should be used every time pyboard changes its state or important event happens.
    @author: Jakub Chodubski
    """
    state: int = 0

    @staticmethod
    def waiting():  # green on
        # Should be used if the board is waiting for new inputs
        state = 0
        pyb.LED(1).on()
        pyb.LED(2).off()
        pyb.LED(3).off()

    @staticmethod
    def running():  # blue on
        # Use this if board is not accepting any inputs at the moment
        # Any data send via USB VCP to board will be queued
        state = 1
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).off()

    @staticmethod
    def error():  # red on
        # Algorithm encountered a problem
        # Board is waiting for debug and reset
        state = 2
        pyb.LED(1).off()
        pyb.LED(2).off()
        pyb.LED(3).on()

    @staticmethod
    def connected():  # quick flash green, blued
        # Signal Virtual Comm Port has been connected
        # After signaling is done previous state will be displayed
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).on()
        Inform.correct_led()

    @staticmethod
    def correct_led():
        # Method used to correct currently displayed LEDs to state saved in Inform.state

        if Inform.state == 0:
            Inform.waiting()

        if Inform.state == 1:
            Inform.running()

        if Inform.state == 2:
            Inform.error()
