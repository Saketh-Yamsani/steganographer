import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from Crypto.Cipher import AES
import base64
import time

# Ensure folders exist
os.makedirs("encrypted", exist_ok=True)
os.makedirs("decrypted", exist_ok=True)

# AES Encryption with Padding
def pad_message(message):
    pad_length = 16 - (len(message) % 16)
    return message + chr(pad_length) * pad_length

def unpad_message(message):
    return message[:-ord(message[-1])]

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_msg = pad_message(message)
    return base64.b64encode(cipher.encrypt(padded_msg.encode()))

def decrypt_message(encrypted, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted))
    return unpad_message(decrypted.decode())

# Generate unique file name with timestamp
def generate_filename(prefix, extension):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}.{extension}"

# Encode message in image
def encode_text(image_path, message, key):
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return

    encrypted_message = encrypt_message(message, key).decode()
    binary_message = ''.join(format(ord(i), '08b') for i in encrypted_message) + '1111111111111110'

    image = cv2.imread(image_path)
    h, w, _ = image.shape

    if len(binary_message) > h * w * 3:
        messagebox.showerror("Error", "Message is too long for the image.")
        return

    # Convert image to a 1D array for faster processing
    flat_image = image.flatten()
    for i in range(len(binary_message)):
        flat_image[i] = (flat_image[i] & 0xFE) | int(binary_message[i])

    # Reshape the image back
    image = flat_image.reshape(h, w, 3)

    # Save with a unique name
    output_path = os.path.join("encrypted", generate_filename("encoded_image", "png"))
    cv2.imwrite(output_path, image)

    messagebox.showinfo("Success", f"Encoded image saved at:\n{output_path}")
    return_to_main()

# Decode message from image
def decode_text(image_path, key):
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return

    image = cv2.imread(image_path)
    binary_message = ""
    stop_sequence = "1111111111111110"

    flat_image = image.flatten()
    for i in range(len(flat_image)):
        binary_message += str(flat_image[i] & 1)
        if binary_message.endswith(stop_sequence):
            binary_message = binary_message[:-len(stop_sequence)]  # Remove stop sequence
            break

    if len(binary_message) % 8 != 0:
        messagebox.showerror("Error", "Extracted message is corrupted.")
        return

    try:
        message = "".join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        decrypted_message = decrypt_message(message, key)

        # Save decrypted message with a unique name
        output_path = os.path.join("decrypted", generate_filename("decrypted_message", "txt"))
        with open(output_path, "w") as f:
            f.write(decrypted_message)

        messagebox.showinfo("Success", f"Decrypted message saved at:\n{output_path}")
        return_to_main()
    except Exception as e:
        messagebox.showerror("Decryption Failed", str(e))

# Open file dialog
def open_file(label):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if file_path:
        load_image_preview(file_path, label)
    return file_path

# Load image preview
def load_image_preview(path, label):
    image = Image.open(path)
    image = image.resize((250, 250))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img  # Store reference

# Return to Main Page
def return_to_main():
    global root
    root.destroy()
    main_gui()

# Encryption GUI
def encryption_gui():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("Encrypt Message in Image")
    root.geometry("600x500")
    root.configure(bg="#2C2F33")

    ttk.Label(root, text="Select an Image:").pack()
    image_label = ttk.Label(root)
    image_label.pack()

    file_path_var = tk.StringVar()

    def select_file():
        file_path_var.set(open_file(image_label))

    ttk.Button(root, text="Browse", command=select_file).pack()

    ttk.Label(root, text="Enter Message:").pack()
    text_entry = ttk.Entry(root, width=50)
    text_entry.pack()

    ttk.Label(root, text="Enter Key (16 chars max):").pack()
    key_entry = ttk.Entry(root, width=50, show='*')
    key_entry.pack()

    def encode_now():
        file_path = file_path_var.get()
        message = text_entry.get()
        key = key_entry.get().ljust(16).encode()
        encode_text(file_path, message, key)

    ttk.Button(root, text="Encrypt and Save", command=encode_now).pack(pady=10)
    ttk.Button(root, text="Back", command=return_to_main).pack(pady=10)

    root.mainloop()

# Decryption GUI
def decryption_gui():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("Decrypt Hidden Message")
    root.geometry("600x500")
    root.configure(bg="#2C2F33")

    ttk.Label(root, text="Select Encrypted Image:").pack()
    image_label = ttk.Label(root)
    image_label.pack()

    file_path_var = tk.StringVar()

    def select_file():
        file_path_var.set(open_file(image_label))

    ttk.Button(root, text="Browse", command=select_file).pack()

    ttk.Label(root, text="Enter Key:").pack()
    key_entry = ttk.Entry(root, width=50, show='*')
    key_entry.pack()

    def decode_now():
        file_path = file_path_var.get()
        key = key_entry.get().ljust(16).encode()
        decode_text(file_path, key)

    ttk.Button(root, text="Decrypt and Save", command=decode_now).pack(pady=10)
    ttk.Button(root, text="Back", command=return_to_main).pack(pady=10)

    root.mainloop()

# Main GUI
def main_gui():
    global root
    root = tk.Tk()
    root.title("Image Steganography")
    root.geometry("400x300")
    root.configure(bg="#2C2F33")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12), background="#2C2F33", foreground="white")
    style.configure("TButton", font=("Arial", 12), padding=5)

    ttk.Label(root, text="Choose an Option:").pack(pady=20)
    ttk.Button(root, text="Encrypt Message in Image", command=encryption_gui).pack(pady=10)
    ttk.Button(root, text="Decrypt Message from Image", command=decryption_gui).pack(pady=10)

    root.mainloop()
main_gui()
