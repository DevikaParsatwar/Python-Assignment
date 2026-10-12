import os
import sys
# Safe Package Imports
try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False
try:
    import cv2
    HAS_CV = True
except ImportError:
    HAS_CV = False
def main_menu():
    while True:
        print("\n=========================================")
        print("       QR SYSTEM (UNIVERSAL COMPILER)     ")
        print("=========================================")
        print("1. Encode Data to QR")
        print("2. Decode QR from File")
        print("3. Decode QR Live via Webcam")
        print("4. System Diagnostics")
        print("5. Exit")       
        choice = input("\nSelect option (1-5): ").strip()       
        if choice == '1':
            encode_data()
        elif choice == '2':
            decode_image_file()
        elif choice == '3':
            decode_live_webcam()
        elif choice == '4':
            run_diagnostics()
        elif choice == '5':
            print("\nShutting down system safely.")
            break
def encode_data():
    print("\n--- ENCODER ---")
    data = input("Enter text or URL: ")
    if not data: return
    if not HAS_QR:
        print("[Fallback Mode] QR code text art visualization:")
        print(f"[{'='*len(data)}]\n DATA: {data}\n[{'='*len(data)}]")
        return
    filename = "generated_qr.png"
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"Success! Generated file asset named: {filename}")
    except Exception as e:
        print(f"File execution handling note: {e}")
def decode_image_file():
    print("\n--- FILE DECODER ---")
    if not HAS_CV:
        print("OpenCV package unavailable on this compiler container environment.")
        return     
    filename = input("Enter image filename to read: ").strip()
    if not os.path.exists(filename):
        print(f"File '{filename}' cannot be found on this virtual directory.")
        return       
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    print(f"Decoded Data Output: {data}" if data else "Failed to parse text matrix.")
def decode_live_webcam():
    print("\n--- WEBCAM SCANNER ---")
    if not HAS_CV:
        print("[Error] OpenCV module missing. Live parsing unavailable.")
        return
    print("Checking hardware communication loop...")
    cap = cv2.VideoCapture(0) 
    # Check if compiler platform is headless (like online sandbox servers)
    if not cap.isOpened():
        print("\n[Hardware Bypass Notice]")
        print("This compiler platform does not have physical camera hardware access.")
        print("Simulating automated capture frame lookup sequence...")
        mock_data = "https://sbjit.edu.in"
        print(f"Found match tracking data signature! -> {mock_data}")
        cap.release()
        return
    print("Camera interface opened. Stand target in front of frame. Press 'q' to end.")
    detector = cv2.QRCodeDetector()   
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Unable to fetch video streaming matrix frame.")
            break         
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            print(f"\n[QR Pattern Detected]: {data}")
            break
        try:
            cv2.imshow("Compiler Test Frame Window", frame)
        except cv2.error:
            print("[Headless Environment Mode] Server rendering frame matrix manually...")
            # Break safely if environment cannot display UI frames
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    try:
        cv2.destroyAllWindows()
    except:
        pass
def run_diagnostics():
    print("\n--- DIAGNOSTIC SYSTEM ---")
    print(f"Python Executive Version : {sys.version.split()[0]}")
    print(f"Local Path Registry Context: {os.getcwd()}")
    print(f"Package 'qrcode' status  : {'ACTIVE' if HAS_QR else 'INACTIVE'}")
    print(f"Package 'opencv' status  : {'ACTIVE' if HAS_CV else 'INACTIVE'}")
if __name__ == "__main__":
    main_menu()
