import json

# =========================
# SERIAL IMPORT
# =========================

try:

    import serial

    SERIAL_AVAILABLE = True

except ImportError:

    SERIAL_AVAILABLE = False


# =========================
# SETTINGS
# =========================

PORT = "COM3"
BAUD_RATE = 115200


# =========================
# CONNECT TO ESP32
# =========================

esp32 = None

if SERIAL_AVAILABLE:

    try:

        esp32 = serial.Serial(
            PORT,
            BAUD_RATE,
            timeout=1
        )

    except:

        esp32 = None


# =========================
# GET ESP32 DATA
# =========================

def get_esp32_data():

    # pyserial not installed
    if not SERIAL_AVAILABLE:

        return None

    # serial port not opened
    if esp32 is None:

        return None

    try:

        line = (
            esp32.readline()
            .decode("utf-8")
            .strip()
        )

        # no data received
        if not line:

            return None

        data = json.loads(line)

        return {

            "distance": float(
                data["distance"]
            ),

            "turns": int(
                data["turns"]
            ),

            "vibration": float(
                data["vibration"]
            )

        }

    except:

        return None