import serial
import time


# =====================================================
# SEND G-CODE TO ESP32
# =====================================================

def send_gcode(
    gcode,
    port="COM3",
    baudrate=115200
):

    try:

        ser = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        time.sleep(2)

        print(
            f"\nConnected to ESP32 on {port}"
        )

        # -------------------------------------------------
        # SEND LINE BY LINE
        # -------------------------------------------------

        for line in gcode:

            message = line + "\n"

            ser.write(message.encode())

            print("Sent:", line)

            start_time = time.time()

            # ---------------------------------------------
            # WAIT FOR DONE
            # ---------------------------------------------

            while True:

                response = (
                    ser.readline()
                    .decode()
                    .strip()
                )

                if response:

                    print(
                        "ESP32:",
                        response
                    )

                if response == "DONE":

                    break

                # Timeout protection
                if (
                    time.time() - start_time
                    > 5
                ):

                    print(
                        f"❌ Timeout: {line}"
                    )

                    ser.close()

                    return

        ser.close()

        print(
            "\nG-code execution complete."
        )

    except Exception as e:

        print("Error:", e)