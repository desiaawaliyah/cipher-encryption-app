# Cipher Encryption/Decryption Tool

## Deskripsi
Aplikasi ini adalah alat enkripsi dan dekripsi berbasis **Tkinter** yang mendukung tiga jenis cipher klasik: **Vigenère Cipher**, **Playfair Cipher**, dan **Hill Cipher**. Pengguna dapat memilih salah satu metode enkripsi, memasukkan teks serta kunci, kemudian melakukan enkripsi atau dekripsi teks tersebut. Selain itu, aplikasi ini mendukung pembukaan dan penyimpanan file teks.

## Fitur Utama
- **Vigenère Cipher**: Menggunakan teknik substitusi polialfabetik untuk mengenkripsi dan mendekripsi teks.
- **Playfair Cipher**: Menggunakan matriks 5x5 yang dibangun dari kunci untuk melakukan enkripsi dan dekripsi.
- **Hill Cipher**: Menggunakan matriks kunci (2x2) dan operasi matriks untuk mengenkripsi dan mendekripsi teks.

## Cara Penggunaan
1. **Memilih Cipher**: 
   - Pada bagian atas aplikasi, terdapat menu dropdown untuk memilih metode cipher yang diinginkan (Vigenère, Playfair, atau Hill).
   
2. **Memasukkan Kunci**:
   - Masukkan kunci pada kolom **Key**. Kunci harus terdiri dari minimal 12 karakter.

3. **Memasukkan Teks**:
   - Anda dapat mengetik teks langsung pada area **Input Text/File** atau membuka file teks dengan menekan tombol **Open File**.

4. **Enkripsi dan Dekripsi**:
   - Tekan tombol **Encrypt** untuk mengenkripsi teks, atau tekan **Decrypt** untuk mendekripsi teks yang sudah dienkripsi.
   
5. **Menyimpan Output**:
   - Teks yang telah dienkripsi atau didekripsi akan muncul di area **Output**. Anda dapat menyimpan hasilnya dengan menekan tombol **Save File**.

## Instalasi
1. Clone repository ini:
   ```bash
   git clone https://github.com/username/cipher-tool.git
   cd cipher-tool
   ```
2. Install dependensi yang diperlukan:
   ```bash
   pip install numpy
   ```
3. Jalankan aplikasi:
   ```bash
   python cipher_tool.py
   ```

## Persyaratan
- Python 3.x
- **Tkinter**: Untuk antarmuka pengguna grafis (GUI), sudah termasuk dalam distribusi standar Python.
- **Numpy**: Digunakan untuk operasi matriks pada Hill Cipher. Install dengan `pip install numpy`.

## Penjelasan Teknikal
1. **Vigenère Cipher**:
   - Cipher ini menggunakan kunci untuk melakukan substitusi polialfabetik. Setiap huruf dari teks digeser berdasarkan nilai huruf pada kunci yang digunakan secara berulang.

2. **Playfair Cipher**:
   - Cipher ini menggunakan matriks 5x5 yang dibuat dari kunci. Setiap pasangan huruf dari teks diproses dengan aturan matriks, seperti pergeseran baris, kolom, atau pergantian posisi.

3. **Hill Cipher**:
   - Cipher ini menggunakan operasi matriks untuk mengenkripsi teks. Teks dibagi menjadi vektor 2x1 yang kemudian dikalikan dengan matriks kunci 2x2. Dekripsi dilakukan dengan mencari invers dari matriks kunci.

## Batasan
- Untuk Hill Cipher, kunci harus terdiri dari minimal 4 karakter yang dapat dibentuk menjadi matriks 2x2.
- Hill Cipher tidak bisa didekripsi jika determinan dari matriks kunci tidak memiliki invers modulo 26.

## Lisensi
Aplikasi ini menggunakan lisensi MIT. Silakan merujuk ke file `LICENSE` untuk informasi lebih lanjut.

## Kontributor
- [Nama Anda](https://github.com/username)

