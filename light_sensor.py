import machine
import time
import bh1750

# === 1. Initialization ===
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
light_sensor = bh1750.BH1750(i2c)

# === 2. Trigger Measurement ===
# BH1750 starts measuring automatically upon reading
def trigger_light_measurement(sensor):
    # No trigger needed for BH1750
    pass

# === 3. Read Sensor Data ===
def read_light_intensity(sensor):
    try:
        lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
        return lux
    except Exception as e:
        print("Light read error:", e)
        return None

# === 4. Data Conversion ===
# BH1750 gives direct lux values — no conversion needed

# === 5. Data Processing ===
lux_log = []

def process_light(lux):
    if lux is None:
        return None
    lux_log.append(lux)
    if len(lux_log) > 5:
        lux_log.pop(0)
    filtered_lux = sum(lux_log) / len(lux_log)
    return round(filtered_lux, 2)

# === 6. Data Storage ===
def store_light(value):
    print("Processed Light Intensity: {:.2f} lx".format(value))
    # You can store or log this value as needed

# === Main Loop ===
while True:
    trigger_light_measurement(light_sensor)
    raw_lux = read_light_intensity(light_sensor)
    processed_lux = process_light(raw_lux)
    if processed_lux is not None:
        store_light(processed_lux)
    time.sleep(10)
