import math_functions
import prog_utils
import csv

def rank_index(array, val):
    sorted_arr = sorted(array, reverse=True)
    for i, v in enumerate(sorted_arr):
        if val >= v:
            return i + 1
    return len(sorted_arr)

def open_file(file_name):
    data = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(float(row[0]))
    return data

def main():
    mean_if_g = 3.84
    mean_if_j = 3.68
    mean_sti_g = 3.61
    mean_sti_j = 3.71
    mean_total = 3.71
    alpha = -0.8
    omega = 0.2

    nama_jurusan = [
        "Informatika Ganesha",
        "Informatika Jatinangor",
        "Sistem dan Teknologi Informasi Ganesha",
        "Sistem dan Teknologi Informasi Jatinangor"
    ]

    ipk = prog_utils.retry_input_range("f", "Masukkan indeks prestasi kumulatif (IPK) Anda: ", 0, 4)

    while True:
        print("Apa yang ingin Anda lakukan?\n1. Menampilkan nilai indeks angkatan\n2. Menghitung peluang memasuki jurusan\n3. Memberikan rekomendasi\n4. Keluar")
        pilihan = prog_utils.retry_input_range("i", "Pilihan: ", 1, 4)

        if pilihan == 4:
            print("Terima kasih!")
            return 0

        if pilihan == 1:
            print("\n=== PILIH DATASET ===\n1. Informatika Ganesha\n2. Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor\n5. Total Gabungan")
            dataset = prog_utils.retry_input_range("i", "Pilihan: ", 1, 5)
            print("========================")

            if dataset == 1:
                data = open_file("data_ipk_if_g.csv")
                rank = rank_index(data, ipk)
                print(f"Rata-rata indeks: {mean_if_g}\nPeringkatmu: {rank}\n========================")

            elif dataset == 2:
                data = open_file("data_ipk_if_j.csv")
                rank = rank_index(data, ipk)
                print(f"Rata-rata indeks: {mean_if_j}\nPeringkatmu: {rank}\n========================")

            elif dataset == 3:
                data = open_file("data_ipk_sti_g.csv")
                rank = rank_index(data, ipk)
                print(f"Rata-rata indeks: {mean_sti_g}\nPeringkatmu: {rank}\n========================")

            elif dataset == 4:
                data = open_file("data_ipk_sti_j.csv")
                rank = rank_index(data, ipk)
                print(f"Rata-rata indeks: {mean_sti_j}\nPeringkatmu: {rank}\n========================")

            else:
                data = open_file("data_ipk_total.csv")
                rank = rank_index(data, ipk)
                print(f"Rata-rata indeks: {mean_total}\nPeringkatmu: {rank}\n========================")

        elif pilihan == 2:
            print("\n=== PILIH JURUSAN ===\n1. Informatika Ganesha\n2. Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor")

            pilihan_jurusan = []
            for i in range(4):
                pilihan_jurusan.append(prog_utils.retry_input_range("i", f"Pilihan {i + 1}: ", 1, 4))

            xi_if_g = math_functions.compute_xi(mean_if_g, omega, alpha)
            xi_if_j = math_functions.compute_xi(mean_if_j, omega, alpha)
            xi_sti_g = math_functions.compute_xi(mean_sti_g, omega, alpha)
            xi_sti_j = math_functions.compute_xi(mean_sti_j, omega, alpha)

            probs = [
                math_functions.truncated_skew_norm_cdf(ipk, xi_if_g, omega, alpha),
                math_functions.truncated_skew_norm_cdf(ipk, xi_if_j, omega, alpha),
                math_functions.truncated_skew_norm_cdf(ipk, xi_sti_g, omega, alpha),
                math_functions.truncated_skew_norm_cdf(ipk, xi_sti_j, omega, alpha),
            ]

            print("Jadi, probabilitasmu untuk memasuki masing-masing jurusan adalah ")
            for i in range(4):
                jurusan = nama_jurusan[pilihan_jurusan[i] - 1]
                print(f"{i + 1}. Pilihan {i + 1} \"{jurusan}\": {100 * probs[i]:.2f}%")

        elif pilihan == 3:
            print("\n=== REKOMENDASI BERDASARKAN IPK GABUNGAN ===")

            xi_total = math_functions.compute_xi(mean_total, omega, alpha)
            P_eval = math_functions.truncated_skew_norm_cdf(ipk, xi_total, omega, alpha)

            print(f"IPK Anda: {ipk} (Rata-rata Kelompok: {mean_total})")
            print(f"Indeks Kuantil (Peluang Kumulatif): {(100 * P_eval):.2f}%")

            print("\nPoin Rekomendasi:")

            if P_eval >= 0.85:
                print("Kategori: Prestasi Sangat Tinggi.")
                print("1. Coba Tantangan Internasional.")
                print("2. Riset & Publikasi.")
                print("3. Kepemimpinan Profesional.")

            elif P_eval >= 0.30:
                print("Kategori: Prestasi Baik. Konsisten dan berkembang.")
                print("1. Ambil Sertifikasi.")
                print("2. Magang.")
                print("3. Networking.")

            else:
                print("Kategori: Perlu Fokus Peningkatan Akademik.")
                print("1. Fokus Mata Kuliah Dasar.")
                print("2. Manajemen Waktu.")
                print("3. Perbaiki Nilai.")

            print("\nTambahan:")
            if ipk > mean_total:
                print(f"Anda berada di atas rata-rata ({mean_total}). Terus pertahankan!")
            elif ipk == mean_total:
                print("IPK Anda berada tepat di rata-rata. Pertahankan!")
            else:
                print(f"IPK Anda di bawah rata-rata ({mean_total}). Fokus memperbaiki nilai.")

if __name__ == "__main__":
    main()
