import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import re

# GUI setup
root = tk.Tk()
root.title("Cipher Encryption/Decryption Tool")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, file.read())

def save_file(output_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(output_text)

# Vigenère Cipher
def vigenere_encrypt(plaintext, key):
    key = key.upper()
    plaintext = plaintext.upper()
    ciphertext = ''
    key_length = len(key)
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            char = chr((ord(plaintext[i]) + ord(key[i % key_length]) - 130) % 26 + 65)
            ciphertext += char
        else:
            ciphertext += plaintext[i]
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    ciphertext = ciphertext.upper()
    plaintext = ''
    key_length = len(key)
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            char = chr((ord(ciphertext[i]) - ord(key[i % key_length]) + 26) % 26 + 65)
            plaintext += char
        else:
            plaintext += ciphertext[i]
    return plaintext

# Playfair Cipher
def create_playfair_matrix(key):
    key = ''.join(sorted(set(key), key=key.index))  # Remove duplicates
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Excludes 'J'
    matrix = []
    for char in key.upper():
        if char not in matrix and char in alphabet:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    # Store non-alphabet positions
    positions = [(i, char) for i, char in enumerate(plaintext) if not char.isalpha()]
    
    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper().replace('J', 'I'))
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    
    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b] + matrix[row_b][col_a]
    
    # Reinsert non-alphabet characters at their original positions
    for pos, char in positions:
        ciphertext = ciphertext[:pos] + char + ciphertext[pos:]
    
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    positions = [(i, char) for i, char in enumerate(ciphertext) if not char.isalpha()]
    
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper().replace('J', 'I'))
    
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]
    
    # Reinsert non-alphabet characters at their original positions
    for pos, char in positions:
        plaintext = plaintext[:pos] + char + plaintext[pos:]

    # Remove padding 'X' if necessary
    if plaintext.endswith('X'):
        plaintext = plaintext[:-1]
    
    return plaintext

# Hill Cipher
def create_hill_matrix(key):
    key = key.upper()
    key_matrix = [ord(c) - 65 for c in key[:4]]  # Get first 4 characters for 2x2 matrix
    return np.array(key_matrix).reshape(2, 2)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def hill_encrypt(plaintext, key):
    key_matrix = create_hill_matrix(key)
    # Store non-alphabet positions
    positions = [(i, char) for i, char in enumerate(plaintext) if not char.isalpha()]

    plaintext = re.sub(r'[^A-Z]', '', plaintext.upper())
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    
    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        vector = np.array([[ord(plaintext[i]) - 65], [ord(plaintext[i+1]) - 65]])
        encrypted_vector = np.dot(key_matrix, vector) % 26
        ciphertext += chr(encrypted_vector[0][0] + 65) + chr(encrypted_vector[1][0] + 65)
    
    # Reinsert non-alphabet characters at their original positions
    for pos, char in positions:
        ciphertext = ciphertext[:pos] + char + ciphertext[pos:]
    
    return ciphertext

def hill_decrypt(ciphertext, key):
    key_matrix = create_hill_matrix(key)
    determinant = int(np.linalg.det(key_matrix))
    determinant_inverse = mod_inverse(determinant, 26)
    
    if determinant_inverse is None:
        raise ValueError("Key matrix is not invertible.")
    
    adjugate = np.array([[key_matrix[1, 1], -key_matrix[0, 1]], [-key_matrix[1, 0], key_matrix[0, 0]]])
    inverse_matrix = (determinant_inverse * adjugate) % 26

    # Store non-alphabet positions
    positions = [(i, char) for i, char in enumerate(ciphertext) if not char.isalpha()]

    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())

    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        vector = np.array([[ord(ciphertext[i]) - 65], [ord(ciphertext[i+1]) - 65]])
        decrypted_vector = np.dot(inverse_matrix, vector) % 26
        plaintext += chr(int(decrypted_vector[0][0]) + 65) + chr(int(decrypted_vector[1][0]) + 65)
    
    # Reinsert non-alphabet characters at their original positions
    for pos, char in positions:
        plaintext = plaintext[:pos] + char + plaintext[pos:]

    # Remove padding 'X' if necessary
    if plaintext.endswith('X'):
        plaintext = plaintext[:-1]
    
    return plaintext

# Encryption/Decryption Handlers
def encrypt_text():
    plaintext = input_text.get(1.0, tk.END).strip()
    key = key_entry.get().strip()
    if len(key) < 12:
        messagebox.showerror("Error", "Key must be at least 12 characters long!")
        return
    if cipher_choice.get() == "Vigenère":
        output = vigenere_encrypt(plaintext, key)
    elif cipher_choice.get() == "Playfair":
        output = playfair_encrypt(plaintext, key)
    elif cipher_choice.get() == "Hill":
        output = hill_encrypt(plaintext, key)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

def decrypt_text():
    ciphertext = input_text.get(1.0, tk.END).strip()
    key = key_entry.get().strip()
    if len(key) < 12:
        messagebox.showerror("Error", "Key must be at least 12 characters long!")
        return
    if cipher_choice.get() == "Vigenère":
        output = vigenere_decrypt(ciphertext, key)
    elif cipher_choice.get() == "Playfair":
        output = playfair_decrypt(ciphertext, key)
    elif cipher_choice.get() == "Hill":
        output = hill_decrypt(ciphertext, key)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

# GUI Layout
cipher_choice = tk.StringVar(value="Vigenère")
tk.Label(root, text="Choose Cipher:").grid(row=0, column=0, padx=5, pady=5)
cipher_menu = tk.OptionMenu(root, cipher_choice, "Vigenère", "Playfair", "Hill")
cipher_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Key:").grid(row=1, column=0, padx=5, pady=5)
key_entry = tk.Entry(root, width=50)
key_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Input Text/File:").grid(row=2, column=0, padx=5, pady=5)
input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=2, column=1, padx=5, pady=5)

open_file_btn = tk.Button(root, text="Open File", command=open_file)
open_file_btn.grid(row=2, column=2, padx=5, pady=5)

encrypt_btn = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_btn.grid(row=3, column=1, padx=5, pady=5)

decrypt_btn = tk.Button(root, text="Decrypt", command=decrypt_text)
decrypt_btn.grid(row=3, column=2, padx=5, pady=5)

tk.Label(root, text="Output:").grid(row=4, column=0, padx=5, pady=5)
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=4, column=1, padx=5, pady=5)

save_file_btn = tk.Button(root, text="Save File", command=lambda: save_file(output_text.get(1.0, tk.END)))
save_file_btn.grid(row=4, column=2, padx=5, pady=5)

root.mainloop()
