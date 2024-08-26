Moisture_level = 0

basic.show_icon(IconNames.HEART)

def on_forever():
    global Moisture_level
    pins.digital_write_pin(DigitalPin.P0, 1)
    Moisture_level = pins.analog_read_pin(AnalogPin.P1)
    pins.digital_write_pin(DigitalPin.P0, 0)
    
    # Send data over serial
    serial.write_string("Moisture Level: " + str(Moisture_level) + "\n")

    basic.pause(5000)

basic.forever(on_forever)
