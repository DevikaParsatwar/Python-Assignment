import os
import streamlit as st
import numpy as np

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

# Page setup configuration
st.set_page_config(
    page_title="QR Code Universal Web System",
    page_icon="🤖",
    layout="wide"
)

st.title("QR Code System (Universal Compiler Interface)")
st.write("---")

# Navigation menu inside the sidebar
menu = [
    "1. Encode Data to QR",
    "2. Decode QR from File",
    "3. Decode QR Live via Webcam",
    "4. System Diagnostics"
]
choice = st.sidebar.selectbox("Select Option", menu)

# ----------------------------------------------------
# 1. ENCODE DATA TO QR
# ----------------------------------------------------
if choice == "1. Encode Data to QR":
    st.header("🔏 QR Code Generator")
    data = st.text_input("Enter text or URL to encode:")
    
    if data:
        if not HAS_QR:
            st.warning("[Fallback Mode] QR code text art visualization:")
            st.code(f"[{'='*len(data)}]\n DATA: {data}\n[{'='*len(data)}]")
        else:
            try:
                # Generate QR Matrix
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save to a temporary location to serve it
                filename = "generated_qr.png"
                img.save(filename)
                
                # Layout for showing output
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(filename, caption="Generated Asset Matrix", use_container_width=True)
                
                with col2:
                    st.success("Success! QR Code compiled successfully.")
                    # Serve the file as a direct download button
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="📥 Download QR Code PNG",
                            data=file,
                            file_name="generated_qr.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"File execution handling note: {e}")

# ----------------------------------------------------
# 2. DECODE QR FROM FILE
# ----------------------------------------------------
elif choice == "2. Decode QR from File":
    st.header("📂 File QR Decoder")
    if not HAS_CV:
        st.error("OpenCV package unavailable on this web server environment.")
    else:
        uploaded_file = st.file_uploader("Upload an image file containing a QR matrix", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            # Convert the byte stream into an OpenCV readable image matrix
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            
            # Show uploaded file preview
            st.image(uploaded_file, caption="Uploaded Target File", width=250)
            
            # Extract and Decode Data
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)
            
            if data:
                st.success("Decoded Data Found!")
                st.code(data, language="text")
            else:
                st.error("Failed to parse text matrix. No valid QR layout found.")

# ----------------------------------------------------
# 3. DECODE QR LIVE VIA WEBCAM
# ----------------------------------------------------
elif choice == "3. Decode QR Live via Webcam":
    st.header("📸 Live Web Browser Scanner")
    if not HAS_CV:
        st.error("[Error] OpenCV module missing. Live parsing unavailable.")
    else:
        st.info("Allow camera permissions when prompted. This uses your local device hardware safely inside the web environment.")
        
        # Web-native camera inputs wrapper
        img_file_buffer = st.camera_input("Position the QR Pattern squarely in front of the camera frame")
        
        if img_file_buffer is not None:
            # Feed buffer arrays straight to CV matrices
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(cv2_img)
            
            if data:
                st.balloons()
                st.success(f"[QR Pattern Detected]:")
                st.markdown(f"#### `{data}`")
            else:
                st.warning("Frame captured, but no distinct QR pattern detected. Try aligning it closer or improving lighting.")

# ----------------------------------------------------
# 4. SYSTEM DIAGNOSTICS
# ----------------------------------------------------
elif choice == "4. System Diagnostics":
    st.header("🛠️ Diagnostic Hub")
    import sys
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Python Runtime version", value=sys.version.split()[0])
        st.metric(label="Active Directory Context", value=os.getcwd().split("/")[-1])
    with col2:
        st.metric(label="Package 'qrcode' Configuration", value="ACTIVE" if HAS_QR else "INACTIVE")
        st.metric(label="Package 'opencv-python' Configuration", value="ACTIVE" if HAS_CV else "INACTIVE")
