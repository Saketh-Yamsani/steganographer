from tkinter import Tk, Label, Button
import encrypt
import decrypt

def main_gui():
    root = Tk()
    root.title("Image Steganography")
    root.geometry("400x300")
    
    Label(root, text="Choose an Option", font=("Arial", 14)).pack(pady=20)
    Button(root, text="Encrypt Message in Image", command=encrypt.encryption_gui).pack(pady=10)
    Button(root, text="Decrypt Message from Image", command=decrypt.decryption_gui).pack(pady=10)
    Button(root, text="Exit", command=root.quit).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main_gui()
