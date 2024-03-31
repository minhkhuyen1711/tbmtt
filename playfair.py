import tkinter as tk
from tkinter import messagebox

def create_playfair_matrix(key):
    key = key.replace(" ", "").upper().replace("J", "I")
    key_set = set(key)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matrix = []
    for char in key:
        if char not in matrix and char in alphabet:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix and char not in key_set:
            matrix.append(char)
    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return playfair_matrix

def encode(text, key):
    try:
        playfair_matrix = create_playfair_matrix(key)
        text = text.replace(" ", "").upper().replace("J", "I")
        text = ''.join(text[i] + ('X' if text[i] == text[i + 1] else text[i + 1]) for i in range(0, len(text), 2))
        encoded_text = ""
        for i in range(0, len(text), 2):
            pair = text[i:i+2]
            try:
                row1, col1 = next((i, row.index(pair[0])) for i, row in enumerate(playfair_matrix) if pair[0] in row)
                row2, col2 = next((i, row.index(pair[1])) for i, row in enumerate(playfair_matrix) if pair[1] in row)
            except StopIteration:
                continue
            if row1 == row2:
                encoded_text += playfair_matrix[row1][(col1 + 1) % 5] + playfair_matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encoded_text += playfair_matrix[(row1 + 1) % 5][col1] + playfair_matrix[(row2 + 1) % 5][col2]
            else:
                encoded_text += playfair_matrix[row1][col2] + playfair_matrix[row2][col1]
        return encoded_text
    except Exception as e:
        print("Error during encoding:", str(e))
        return None

def decode(encoded_text, key):
    try:
        playfair_matrix = create_playfair_matrix(key)
        decoded_text = ""
        for i in range(0, len(encoded_text), 2):
            pair = encoded_text[i:i+2]
            try:
                row1, col1 = next((i, row.index(pair[0])) for i, row in enumerate(playfair_matrix) if pair[0] in row)
                row2, col2 = next((i, row.index(pair[1])) for i, row in enumerate(playfair_matrix) if pair[1] in row)
            except StopIteration:
                continue
            if row1 == row2:
                decoded_text += playfair_matrix[row1][(col1 - 1) % 5] + playfair_matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decoded_text += playfair_matrix[(row1 - 1) % 5][col1] + playfair_matrix[(row2 - 1) % 5][col2]
            else:
                decoded_text += playfair_matrix[row1][col2] + playfair_matrix[row2][col1]
        return decoded_text
    except Exception as e:
        print("Error during decoding:", str(e))
        return None

def validate_input(text):
    if text.isalpha() and 'J' not in text:
        return True
    return False

def encrypt_message():
    key = key_entry.get().upper()
    message = message_entry.get("1.0", 'end-1c').upper()

    if not validate_input(key):
        show_error("Key must contain only non-repeating alphabetic characters (excluding 'J').")
        return
    if not all(validate_input(char) for char in message if char != ' '):
        show_error("Message must contain only alphabetic characters.")
        return

    encrypted_message = encode(message, key)
    if encrypted_message:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted_message)

def decrypt_message():
    key = key_entry.get().upper()
    message = message_entry.get("1.0", 'end-1c').upper()

    if not validate_input(key):
        show_error("Key must contain only non-repeating alphabetic characters (excluding 'J').")
        return
    if not all(validate_input(char) for char in message if char != ' '):
        show_error("Message must contain only alphabetic characters.")
        return

    decrypted_message = decode(message, key)
    if decrypted_message:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted_message)

def show_error(message):
    messagebox.showerror("Error", message)

root = tk.Tk()
root.title("Playfair Cipher")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

key_label = tk.Label(frame, text="Key:")
key_label.grid(row=0, column=0, sticky="w")

key_entry = tk.Entry(frame)
key_entry.grid(row=0, column=1, padx=5, pady=5)

message_label = tk.Label(frame, text="Message:")
message_label.grid(row=1, column=0, sticky="w")

message_entry = tk.Text(frame, height=5, width=30)
message_entry.grid(row=1, column=1, padx=5, pady=5)

encrypt_button = tk.Button(frame, text="Encrypt", command=encrypt_message)
encrypt_button.grid(row=2, column=0, padx=5, pady=5)

decrypt_button = tk.Button(frame, text="Decrypt", command=decrypt_message)
decrypt_button.grid(row=2, column=1, padx=5, pady=5)

output_label = tk.Label(frame, text="Result:")
output_label.grid(row=3, column=0, sticky="w", pady=5)

output_text = tk.Text(frame, height=5, width=30)
output_text.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()