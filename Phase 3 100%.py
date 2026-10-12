import os
import sys
import qrcode
import cv2
from colorama import Fore, Style, init

init(autoreset=True)

# ==============================
#      QR CODE SYSTEM
# ==============================

APP_NAME = "QR CODE STUDIO"

def line():
    print(Fore.CYAN + "=" * 55)

def header():
    os.system("cls" if os.name == "nt" else "clear")
    line()
    print(Fore.MAGENTA + Style.BRIGHT +
          "             QR CODE STUDIO")
    print(Fore.YELLOW + "          Universal QR Toolkit")
    line()

def pause():
    input(Fore.YELLOW + "\nPress Enter to continue...")


# ==============================
#      QR CODE GENERATOR
# ==============================

def generate_qr():
    header()
    print(Fore.GREEN + Style.BRIGHT + "        [ QR CODE GENERATOR ]")
    line()

    data = input(Fore.CYAN + "Enter text or URL: ").strip()

    if not data:
        print(Fore.RED + "Error: Input cannot be empty!")
        pause()
        return

    filename = input(
        Fore.YELLOW + "Enter output filename (default: my_qr): "
    ).strip()

    if not filename:
        filename = "my_qr"

    if not filename.lower().endswith(".png"):
        filename += ".png"

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="#4527A0",
            back_color="#FFFFFF"
        )

        image.save(filename)

        print(Fore.GREEN + "\n✓ QR code generated successfully!")
        print(Fore.CYAN + f"File: {os.path.abspath(filename)}")

    except Exception as error:
        print(Fore.RED + f"Generation failed: {error}")

    pause()


# ==============================
#      QR IMAGE DECODER
# ==============================

def decode_qr():
    header()
    print(Fore.GREEN + Style.BRIGHT + "         [ QR IMAGE DECODER ]")
    line()

    filename = input(
        Fore.CYAN + "Enter QR image path: "
    ).strip().strip('"')

    if not os.path.isfile(filename):
        print(Fore.RED + "Error: Image file not found!")
        pause()
        return

    image = cv2.imread(filename)

    if image is None:
        print(Fore.RED + "Error: Unable to read image!")
        pause()
        return

    try:
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(image)

        if data:
            print(Fore.GREEN + "\n✓ QR Code Detected!")
            line()
            print(Fore.YELLOW + "Decoded Information:")
            print(Fore.WHITE + Style.BRIGHT + data)
            line()
        else:
            print(Fore.RED + "No readable QR code detected.")

    except Exception as error:
        print(Fore.RED + f"Decoding error: {error}")

    pause()


# ==============================
#      LIVE WEBCAM SCANNER
# ==============================

def scan_webcam():
    header()
    print(Fore.GREEN + Style.BRIGHT + "          [ LIVE QR SCANNER ]")
    line()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print(Fore.RED + "Error: Webcam not available!")
        pause()
        return

    detector = cv2.QRCodeDetector()
    last_data = None

    print(Fore.YELLOW + "Show a QR code to the camera.")
    print(Fore.CYAN + "Press Q to stop scanning.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print(Fore.RED + "Unable to capture camera frame.")
                break

            data, points, _ = detector.detectAndDecode(frame)

            if points is not None:
                points = points.astype(int)

                for i in range(len(points[0])):
                    start = tuple(points[0][i])
                    end = tuple(points[0][(i + 1) % len(points[0])])

                    cv2.line(
                        frame, start, end,
                        (0, 255, 100), 3
                    )

            if data and data != last_data:
                last_data = data
                print(Fore.GREEN + f"\n✓ QR Data: {data}")

            cv2.imshow("QR Code Studio - Live Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as error:
        print(Fore.RED + f"Scanner error: {error}")

    finally:
        camera.release()
        cv2.destroyAllWindows()

    pause()


# ==============================
#      SYSTEM DIAGNOSTICS
# ==============================

def diagnostics():
    header()
    print(Fore.GREEN + Style.BRIGHT + "        [ SYSTEM DIAGNOSTICS ]")
    line()

    print(Fore.CYAN + f"Application : {APP_NAME}")
    print(Fore.WHITE + f"Python      : {sys.version.split()[0]}")
    print(Fore.WHITE + f"Directory   : {os.getcwd()}")

    print(Fore.YELLOW + "\n--- MODULE STATUS ---")

    modules = {
        "QR Generator": "qrcode",
        "OpenCV Scanner": "cv2",
        "Color Interface": "colorama"
    }

    for name, module in modules.items():
        try:
            __import__(module)
            print(Fore.GREEN + f"[ACTIVE]   {name}")
        except ImportError:
            print(Fore.RED + f"[MISSING]  {name}")

    print(Fore.YELLOW + "\n--- CAMERA STATUS ---")

    camera = cv2.VideoCapture(0)

    if camera.isOpened():
        print(Fore.GREEN + "Webcam: Available")
    else:
        print(Fore.RED + "Webcam: Unavailable")

    camera.release()

    line()
    pause()


# ==============================
#          MAIN MENU
# ==============================

def main_menu():
    while True:
        header()

        print(Fore.GREEN + "  [1] " + Fore.WHITE + "Generate QR Code")
        print(Fore.GREEN + "  [2] " + Fore.WHITE + "Decode QR from Image")
        print(Fore.GREEN + "  [3] " + Fore.WHITE + "Scan QR using Webcam")
        print(Fore.GREEN + "  [4] " + Fore.WHITE + "System Diagnostics")
        print(Fore.RED + "  [5] " + Fore.WHITE + "Exit Application")

        line()

        choice = input(
            Fore.YELLOW + "\nSelect an option (1-5): "
        ).strip()

        if choice == "1":
            generate_qr()

        elif choice == "2":
            decode_qr()

        elif choice == "3":
            scan_webcam()

        elif choice == "4":
            diagnostics()

        elif choice == "5":
            print(Fore.GREEN + "\nShutting down QR Code Studio...")
            print(Fore.MAGENTA + "Thank you for using our application!")
            break

        else:
            print(Fore.RED + "\nInvalid choice! Please select 1-5.")
            pause()


# ==============================
#       PROGRAM EXECUTION
# ==============================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nApplication stopped safely.")
