import cv2
import os
import base64
import time
from Crypto.Cipher import AES
from tkinter import filedialog, simpledialog, messagebox, Tk, Label, Button

def pad_message(message):
    pad_length = 16 - (len(message) % 16)
    return message + chr(pad_length) * pad_length

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_msg = pad_message(message)
    return base64.b64encode(cipher.encrypt(padded_msg.encode())).decode()

def generate_filename(prefix, extension):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}.{extension}"

def encode_text():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return
    
    message = simpledialog.askstring("Input", "Enter message to hide:")
    key = simpledialog.askstring("Input", "Enter encryption key (16 chars max):").ljust(16).encode()
    
    encrypted_message = encrypt_message(message, key)
    binary_message = ''.join(format(ord(i), '08b') for i in encrypted_message) + '1111111111111110'
    
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    
    if len(binary_message) > h * w * 3:
        messagebox.showerror("Error", "Message is too long for the image.")
        return
    
    flat_image = image.flatten()
    for i in range(len(binary_message)):
        flat_image[i] = (flat_image[i] & 0xFE) | int(binary_message[i])
    
    image = flat_image.reshape(h, w, 3)
    os.makedirs("encrypted", exist_ok=True)
    output_path = os.path.join("encrypted", generate_filename("encoded_image", "png"))
    cv2.imwrite(output_path, image)
    messagebox.showinfo("Success", f"Encoded image saved at:\n{output_path}")

def encryption_gui():
    root = Tk()
    root.title("Image Steganography - Encryption")
    root.geometry("400x300")
    
    Label(root, text="Encrypt Message in Image", font=("Arial", 14)).pack(pady=10)
    Button(root, text="Select Image and Encrypt", command=encode_text).pack(pady=10)
    Button(root, text="Back", command=root.destroy).pack(pady=10)
    
    root.mainloop()