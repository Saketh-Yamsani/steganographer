import cv2
import base64
import os
import time
from Crypto.Cipher import AES
from tkinter import filedialog, simpledialog, messagebox, Tk, Label, Button

def decrypt_message(encrypted, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted))
    return decrypted.decode().rstrip("\x01..\x10")

def generate_filename(prefix, extension):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}.{extension}"

def decode_text():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return
    
    key = simpledialog.askstring("Input", "Enter decryption key (16 chars max):").ljust(16).encode()
    
    image = cv2.imread(image_path)
    binary_message = ""
    stop_sequence = "1111111111111110"
    
    flat_image = image.flatten()
    for i in range(len(flat_image)):
        binary_message += str(flat_image[i] & 1)
        if binary_message.endswith(stop_sequence):
            binary_message = binary_message[:-len(stop_sequence)]
            break
    
    if len(binary_message) % 8 != 0:
        messagebox.showerror("Error", "Extracted message is corrupted.")
        return
    
    try:
        message = "".join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        decrypted_message = decrypt_message(message, key)
        os.makedirs("decrypted", exist_ok=True)
        output_path = os.path.join("decrypted", generate_filename("decrypted_message", "txt"))
        with open(output_path, "w") as f:
            f.write(decrypted_message)
        
        messagebox.showinfo("Success", f"Decrypted message saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Decryption Failed", str(e))

def decryption_gui():
    root = Tk()
    root.title("Image Steganography - Decryption")
    root.geometry("400x300")
    
    Label(root, text="Decrypt Message from Image", font=("Arial", 14)).pack(pady=10)
    Button(root, text="Select Image and Decrypt", command=decode_text).pack(pady=10)
    Button(root, text="Back", command=root.destroy).pack(pady=10)
    
    root.mainloop()