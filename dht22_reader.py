import machine
import time
import dht

# === a. Initialization ===
# Define the GPIO pin used for the DHT22
sensor_pin = machine.Pin(4)  # Change this to the correct pin for your setup
dht_sensor = dht.DHT22(sensor_pin)

# Buffers to hold recent readings for filtering
humidity_log = []
temperature_log = []

def initialize_sensor():
    print("Initializing DHT22 sensor...")
    return dht_sensor

# === b. Trigger Measurement ===
def trigger_measurement(sensor):
    try:
        sensor.measure()
    except Exception as e:
        print("Measurement trigger failed:", e)

# === c. Read Sensor Data ===
def read_humidity(sensor):
    try:
        return sensor.humidity()
    except Exception as e:
        print("Failed to read humidity:", e)
        return None

def read_temperature(sensor):
    try:
        return sensor.temperature()
    except Exception as e:
        print("Failed to read temperature:", e)
        return None

# === d. Process Data (Moving Average Filter) ===
def process_value(raw_value, buffer):
    if raw_value is None:
        return None
    buffer.append(raw_value)
    if len(buffer) > 3:
        buffer.pop(0)
    return round(sum(buffer) / len(buffer), 2)

# === e. Store or Output Data ===
def store_data(humidity, temperature):
    print("Processed Humidity: {:.2f}%".format(humidity))
    print("Processed Temperature: {:.2f}°C".format(temperature))
    # Extend here to log to ThingSpeak, SD card, etc.

# === Main Loop ===
sensor = initialize_sensor()

while True:
    trigger_measurement(sensor)

    # Read raw sensor values
    raw_humidity = read_humidity(sensor)
    raw_temperature = read_temperature(sensor)

    # Filter/Process values
    processed_humidity = process_value(raw_humidity, humidity_log)
    processed_temperature = process_value(raw_temperature, temperature_log)

    # Display or send values
    if processed_humidity is not None and processed_temperature is not None:
        store_data(processed_humidity, processed_temperature)

    # Wait for 10 seconds before the next reading
    time.sleep(10)
