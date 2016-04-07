import time
from gpiocrust import Header, OutputPin, PWMOutputPin

with Header() as header:
    pin11 = OutputPin(11)
    pin15 = PWMOutputPin(15, frequency=100, value=0)

    try:
        while 1:
            # Going up
            pin11.value = True

            for i in range(100):
                pin15.value = i / 100.0
                time.sleep(0.01)

            time.sleep(0.5)

            # Going down
            pin11.value = False

            for i in range(100):
                pin15.value = (100 - i) / 100.0
                print pin15.value
                time.sleep(0.01)

            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
