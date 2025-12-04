import math_functions
import utils
import csv

# Konstanta
INV_PI = 0.31830989
INV_SQRT_2 = 0.70710678

def rank_index(array, val):
    for i in range(len(array) - 1):
        if array[i] < val < array[i + 1]:
            return i + 1

def open_file(data, file_name):
    k = 0
    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            data[k] = float(row[0])
            if k < len(data): 
                try:
                    data[k] = float(row[0]) 
                    k += 1
                except ValueError:
                    print(f"Peringatan: Baris {k} bukan angka. Dilewati.")
                    k += 1
            else:
                break


def main():
    mean_if_g = 3.84
    mean_if_j = 3.68
    mean_sti_g = 3.71
    mean_sti_j = 3.61
    mean_total = 3.71
    alpha = -0.8
    omega = 0.2

    data_ipk_total = [0.0 for i in range(285)]
    data_ipk_if_g = [0.0 for i in range(72)]
    data_ipk_if_j = [0.0 for i in range(71)]
    data_ipk_sti_g = [0.0 for i in range(71)]
    data_ipk_sti_j = [0.0 for i in range(71)]

    nama_jurusan = ["Informatika Ganesha", "Informatika Jatinangor", "Sistem dan Teknologi Informasi Ganesha", "Sistem dan Teknologi Informasi Jatinangor"]

    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))
    if (utils.validate_input(ipk, 0, 4) == False):
        print("Terjadi kesalahan input, cobalah lagi")
        return

    while True:
        print("Apa yang ingin Anda lakukan?\n1. Menampilkan nilai indeks angkatan\n2. Menghitung peluang memasuki jurusan\n3. Keluar")
        pilihan = retry_input_range("i", "Pilihan: ", 1, 3)

        if pilihan == 3:
            print("Terima kasih!")
            return 0
        if pilihan == 1:
            print("\n=== PILIH DATASET ===\n1. Informatika Ganesha\n2.Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor\n5. Total Gabungan")
            dataset = utils.retry_input_range("i", "Pilihan: ", 1, 5)

            print("========================")
            if dataset == 1:
                data_ipk_if_g = open_file(data_ipk_if_g, "data_ipk_if_g.csv")
                rank = rank_index(data_ipk_if_g, ipk)

                print(f"Rata-rata indeks: {mean_if_g}\nPeringkatmu: {rank}\n========================")
            elif dataset == 2:
                data_ipk_if_j = open_file(data_ipk_if_j, "data_ipk_if_j.csv")
                rank = rank_index(data_ipk_if_j, ipk)

                print(f"Rata-rata indeks: {mean_if_j}\nPeringkatmu: {rank}\n========================")
            elif dataset == 3:
                data_ipk_sti_g = open_file(data_ipk_sti_g, "data_ipk_sti_g.csv")
                rank = rank_index(data_ipk_sti_g, ipk)

                print(f"Rata-rata indeks: {mean_sti_g}\nPeringkatmu: {rank}\n========================")
            elif dataset == 4:
                data_ipk_sti_j = open_file(data_ipk_sti_j, "data_ipk_sti_j.csv")
                rank = rank_index(data_ipk_sti_j, ipk)

                print(f"Rata-rata indeks: {mean_sti_j}\nPeringkatmu: {rank}\n========================")
            else:
                data_ipk_total = open_file(data_ipk_total, "data_ipk_total.csv")
                rank = rank_index(data_ipk_total, ipk)

                print(f"Rata-rata indeks: {mean_total}\nPeringkatmu: {rank}\n========================")
        elif pilihan == 2:
            print("\n=== PILIH JURUSAN ===\n1. Informatika Ganesha\n2.Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor")
            pilihan = [0 for i in range(4)]
            for i in range(4):
                pilihan[i] = retry_input_range("i", f"Pilihan {i + 1}: ", 1, 4)

            xi_if_g = math_functions.compute_xi(mean_if_g, omega, alpha)
            xi_if_j = math_functions.compute_xi(mean_if_j, omega, alpha)
            xi_sti_g = math_functions.compute_xi(mean_sti_g, omega, alpha)
            xi_sti_j = math_functions.compute_xi(mean_sti_j, omega, alpha)

            probabilitas = [0 for i in range(4)]
            for i in range(4):
                if pilihan[i] == 1:
                    probabilitas[i] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_g, omega, alpha)
                if pilihan[i] == 2:
                    probabilitas[i] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_j, omega, alpha)
                if pilihan[i] == 3:
                    probabilitas[i] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_g, omega, alpha)
                if pilihan[i] == 4:
                    probabilitas[i] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_j, omega, alpha)
            
            print("Jadi, probabilitasmu untuk memasuki masing-masing jurusan adalah ")
            for i in range(4):
                print(f"{i + 1}. Pilihan {i + 1} \"{nama_jurusan[pilihan[i] - 1]}\": {round(probabilitas[i], 4)}")

if __name__ == "__main__":
    main()
