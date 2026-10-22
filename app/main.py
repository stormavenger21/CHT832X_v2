import time

from app.sensor import CHT832x

sensor = CHT832x(bus_number=1)

while True:
    try:
        measurement = sensor.read()

        print(
            f"Temperature: "
            f"{measurement['temperature_c']:.2f} °C | "
            f"Humidity: "
            f"{measurement['humidity_rh']:.2f} %RH"
        )

    except Exception as error:
        print(f"Sensor error: {error}")

    time.sleep(1)
