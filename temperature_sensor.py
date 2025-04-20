import machine
import time
import dht

# === 1. Initialization ===
sensor_pin = machine.Pin(4)  # Use your actual GPIO pin
temperature_sensor = dht.DHT22(sensor_pin)

# === 2. Trigger Measurement ===
def trigger_temp_measurement(sensor):
    try:
        sensor.measure()
    except Exception as e:
        print("Trigger failed:", e)

# === 3. Read Sensor Data ===
def read_temperature(sensor):
    try:
        temp = sensor.temperature()
        return temp
    except Exception as e:
        print("Read failed:", e)
        return None

# === 4. Data Conversion ===
# DHT returns °C already — no need for conversion

# === 5. Data Processing ===
temp_log = []

def process_temperature(raw_temp):
    if raw_temp is None:
        return None
    temp_log.append(raw_temp)
    if len(temp_log) > 3:
        temp_log.pop(0)
    average_temp = sum(temp_log) / len(temp_log)
    return round(average_temp, 2)

# === 6. Data Storage ===
def store_temperature(value):
    print("Processed Temperature: {:.2f} °C".format(value))
    # You can store to memory/EEPROM/file here if needed

# === Main Loop ===
while True:
    trigger_temp_measurement(temperature_sensor)
    temp_raw = read_temperature(temperature_sensor)
    temp_processed = process_temperature(temp_raw)
    if temp_processed is not None:
        store_temperature(temp_processed)
    time.sleep(10)
