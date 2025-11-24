import random

def insert():

def main():
    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))
    print(f"{ipk}")
    menu = input("Apa yang ingin Anda lakukan?\n1. Menampilkan daftar peringkat IPK\n2. Memulai prediktor hasil penjurusan\n3. Meminta rekomendasi belajar\n4. Keluar")

    # Daftar Peringkat IPK
    ## Kalau menurutku sih buat daftar peringkat boleh pakai CSV atau langsung array Python. Fitur sortnya buat pas menampilkan peringkat aja. Jadi, kita declare array baru yang mencakup nilai yang diinput user buat menganalisis data peringkat.
    indeks = [random.uniform() for _ in range(281)] # untuk sementara membuka daftar indeks pakai algoritma ini
    

if __name__ == "__main__":
    main()
