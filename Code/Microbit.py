# import bluetooth
# import serial

def on_bluetooth_connected():
    basic.clear_screen()
    basic.pause(1000)
    basic.show_string("C")
    # basic.pause(1000)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.clear_screen()
    basic.pause(1000)
    basic.show_string("X")
    # basic.pause(1000)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

#start uart bluetooth service
# 12.845312859923238, 77.66315931955364

# reset to default coordinates
def on_button_pressed_a():
    global target_lat, target_lon, bearing_to_target, current_lat,current_lon
    target_lat = 12.845364445067858
    target_lon = 77.66352510162339
    current_lat = 12.844014567079437
    current_lon = 77.66319888503435
    bearing_to_target = calculate_bearing(current_lat, current_lon, target_lat, target_lon)
input.on_button_pressed(Button.A, on_button_pressed_a)

#Recalibrate compass if needed
def on_button_pressed_b():
    input.calibrate_compass()
input.on_button_pressed(Button.B, on_button_pressed_b)

# function to calculate bearing in degrees
def calculate_bearing(lat1 : number, lon1, lat2, lon2):
    lat1_rad = lat1 * 3.14159 / 180
    lon1_rad = lon1 * 3.14159 / 180
    lat2_rad = lat2 * 3.14159 / 180
    lon2_rad = lon2 * 3.14159 / 180
    delta_lon = lon2_rad - lon1_rad
    x = Math.sin(delta_lon) * Math.cos(lat2_rad)
    y = Math.cos(lat1_rad) * Math.sin(lat2_rad) - Math.sin(lat1_rad) * Math.cos(lat2_rad) * Math.cos(delta_lon)
    initial_bearing_rad = Math.atan2(x, y)
    initial_bearing_deg = initial_bearing_rad * 180 / 3.14159
    compass_bearing = (initial_bearing_deg + 360) % 360
    return compass_bearing

def on_uart_data_received():
    global target_lat, target_lon, bearing_to_target, current_lat,current_lon
    data = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    # bluetooth.uart_write_line(data)
    x2 = data.split()
    # bluetooth.uart_write_line("" + str(int(x2[0])))
    # bluetooth.uart_write_line("" + str(int(x2[1])))
    # bluetooth.uart_write_line("" + str(int(x2[2])))
    # bluetooth.uart_write_line("" + str(int(x2[3])))
    pow1 = len(x2[0]) - int(x2[1])
    pow2 = len(x2[2]) - int(x2[3])
    if(int(x2[0]) < 0):
        pow1-=1
    if(int(x2[2]) < 0):
        pow2 -= 1
    bluetooth.uart_write_line("")
    # bluetooth.uart_write_line("Coordinates: ")
    bluetooth.uart_write_line("Latitude: " + str(int(x2[0]) / 10 ** pow1))
    bluetooth.uart_write_line("Longitude: " + str(int(x2[2]) / 10 ** pow2))
    bluetooth.uart_write_string("Type: ")
    if(x2[4].lower()[0] == 's'):
        bluetooth.uart_write_line("Source")
        current_lat = int(x2[0]) / 10 ** pow1
        current_lon = int(x2[2]) / 10 ** pow2
    else:
        bluetooth.uart_write_line("Destination")
        target_lat = int(x2[0]) / 10 ** pow1
        target_lon = int(x2[2]) / 10 ** pow2
    bluetooth.uart_write_line("")
    # bluetooth.uart_write_line(data[0], data[1], data[2],data[3])
    bearing_to_target = calculate_bearing(current_lat, current_lon, target_lat, target_lon)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),on_uart_data_received)

#current location
current_lat = 12.844014567079437
current_lon = 77.66319888503435
#target location
target_lat = 12.845364445067858
target_lon = 77.66352510162339
#get the bearing to the target
bearing_to_target = calculate_bearing(current_lat, current_lon, target_lat, target_lon)
bluetooth.start_uart_service()

#main loop
while True:
    current_heading = input.compass_heading()
    difference = (bearing_to_target - current_heading + 360) % 360
    if difference < 15 or difference > 345:
        basic.show_arrow(ArrowNames.NORTH)
    elif difference < 180:
        basic.show_arrow(ArrowNames.EAST)
    else:
        basic.show_arrow(ArrowNames.WEST)