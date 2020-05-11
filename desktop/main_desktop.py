from desktop.alghoritm_control import GUI
from desktop.usb import USB

if __name__ == '__main__':
    usb = USB()
    gui = GUI(usb)

    # must be at the end of main
    gui.work()
