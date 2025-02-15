Image Steganography with AES Encryption

This project implements **image steganography** using **Least Significant Bit (LSB) encoding** along with **AES encryption** to securely hide and extract messages within images.

## Features
✅ Encrypt and hide messages inside images  
✅ Secure messages using **AES encryption (ECB Mode)**  
✅ Extract and decrypt messages from steganographic images  
✅ Supports `.png`, `.jpg`, and `.bmp` images  
✅ Simple and intuitive **GUI using Tkinter**  


## Installation
### Prerequisites
Ensure you have Python 3.x installed along with the required dependencies.

### Install Dependencies
Run the following command:

```bash
pip install numpy opencv-python pillow pycryptodome
```

---

## **Usage**
### **Run the Application**
Execute the following command:

```bash
python stegno.py
```

### **Encrypt a Message into an Image**
1. Click **"Encrypt Message in Image"**
2. Select an image (`.png`, `.jpg`, or `.bmp`)
3. Enter the secret message
4. Enter a **16-character key** for AES encryption
5. Click **"Encrypt and Save"**
6. The encoded image is saved in the `encrypted/` folder

### **Decrypt a Message from an Image**
1. Click **"Decrypt Message from Image"**
2. Select the steganographic image
3. Enter the **same AES key** used during encryption
4. Click **"Decrypt and Save"**
5. The extracted message is saved in the `decrypted/` folder

---

## How It Works
1. AES Encryption
   - The message is **encrypted** using AES (ECB mode).
   - The ciphertext is converted to a **binary sequence**.
   
2. LSB Steganography
   - The binary message is embedded into the least significant bits (LSB) of the image pixels.
   - A stop sequence (`1111111111111110`) marks the end of the hidden message.

3. Extraction & Decryption 
   - The binary message is retrieved from the **LSB** of the image.
   - It is **decoded and decrypted** using the AES key.

---

## Folder Structure
```
├── encrypted/       # Stores encoded images
├── decrypted/       # Stores extracted text messages
├── main.py          # Main script with GUI
├── README.md        # Project documentation
```
