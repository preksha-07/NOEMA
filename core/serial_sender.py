import serial
import time

from core.safety import (
    validate_command
)


# =====================================================
# SERIAL EXECUTION
# =====================================================

def send_commands(
    commands,
    port="COM3",
    baudrate=9600
):

    MAX_RETRIES = 3

    try:

        ser = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        time.sleep(2)

        print(
            "\nConnected to ESP32 on",
            port
        )

        # -------------------------------------------------
        # COMMAND LOOP
        # -------------------------------------------------

        for cmd in commands:

            # =============================================
            # SAFETY VALIDATION
            # =============================================

            if not validate_command(cmd):

                print(
                    f"\n❌ Invalid command blocked: {cmd}"
                )

                continue

            retries = 0

            success = False

            # =============================================
            # RETRY LOOP
            # =============================================

            while retries < MAX_RETRIES:

                message = cmd + "\n"

                ser.write(
                    message.encode()
                )

                print(
                    "Sent:",
                    cmd
                )

                start_time = time.time()

                # =========================================
                # WAIT FOR DONE
                # =========================================

                while True:

                    response = ser.readline().decode().strip()

                    if response:

                        print(
                            "ESP32:",
                            response
                        )

                    if response == "DONE":

                        success = True

                        break

                    # -------------------------------------
                    # TIMEOUT
                    # -------------------------------------

                    if time.time() - start_time > 5:

                        print(
                            f"\n⚠️ Timeout on command: {cmd}"
                        )

                        retries += 1

                        print(
                            f"Retry {retries}/{MAX_RETRIES}"
                        )

                        break

                if success:

                    break

            # =============================================
            # FINAL FAILURE
            # =============================================

            if not success:

                print(
                    f"\n❌ Command failed permanently: {cmd}"
                )

                ser.close()

                return

        # -------------------------------------------------
        # FINISH
        # -------------------------------------------------

        ser.close()

        print(
            "\n✅ All commands executed successfully."
        )

    except Exception as e:

        print(
            "\n❌ Serial Error:",
            e
        )