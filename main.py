import math_functions
import prog_utils
import csv

# Rank: IPK tertinggi = rank 1
def rank_index(array, val):
    rank = 1  # mulai dari 1
    for ipk in array:
        if ipk > val:
            rank += 1
    return rank

# Open file TANPA append/pop/split
# Mengisi sisa elemen dengan angka besar agar tidak mengganggu ranking
def open_file(data, file_name):
    k = 0
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if k >= len(data):
                break
            data[k] = float(row[0])
            k += 1

    # Sisa data diisi angka besar, supaya tidak dihitung sebagai IPK rendah
    while k < len(data):
        data[k] = 10.0
        k += 1

    return data


def main():
    mean_if_g = 3.84
    mean_if_j = 3.68
    mean_sti_g = 3.61
    mean_sti_j = 3.71
    mean_total = 3.71
    alpha = -0.8
    omega = 0.2

    # Allocate fixed-size arrays
    data_ipk_total = [0.0 for i in range(285)]
    data_ipk_if_g = [0.0 for i in range(72)]
    data_ipk_if_j = [0.0 for i in range(71)]
    data_ipk_sti_g = [0.0 for i in range(71)]
    data_ipk_sti_j = [0.0 for i in range(71)]

    nama_jurusan = [
        "Informatika Ganesha",
        "Informatika Jatinangor",
        "Sistem dan Teknologi Informasi Ganesha",
        "Sistem dan Teknologi Informasi Jatinangor"
    ]

    # Input IPK
    ipk = prog_utils.retry_input_range("f", "Masukkan indeks prestasi kumulatif (IPK) Anda: ", 0, 4)

    while True:
        print("\nApa yang ingin Anda lakukan?\n"
              "1. Menampilkan nilai indeks angkatan\n"
              "2. Menghitung peluang memasuki jurusan\n"
              "3. Memberikan rekomendasi\n"
              "4. Keluar")

        pilihan = prog_utils.retry_input_range("i", "Pilihan: ", 1, 4)

        if pilihan == 4:
            print("Terima kasih!")
            return 0

        # ============================
        # 1. Tampilkan nilai indeks
        # ============================
        if pilihan == 1:
            print("\n=== PILIH DATASET ===\n"
                  "1. Informatika Ganesha\n"
                  "2. Informatika Jatinangor\n"
                  "3. Sistem dan Teknologi Informasi Ganesha\n"
                  "4. Sistem dan Teknologi Informasi Jatinangor\n"
                  "5. Total Gabungan")
            
            dataset = prog_utils.retry_input_range("i", "Pilihan: ", 1, 5)

            print("========================")
            if dataset == 1:
                data_ipk_if_g = open_file(data_ipk_if_g, "data_ipk_if_g.csv")
                rank = rank_index(data_ipk_if_g, ipk)

                print(f"Rata-rata indeks: {mean_if_g}")
                print(f"Peringkatmu: {rank}")
                print("========================")

            elif dataset == 2:
                data_ipk_if_j = open_file(data_ipk_if_j, "data_ipk_if_j.csv")
                rank = rank_index(data_ipk_if_j, ipk)

                print(f"Rata-rata indeks: {mean_if_j}")
                print(f"Peringkatmu: {rank}")
                print("========================")

            elif dataset == 3:
                data_ipk_sti_g = open_file(data_ipk_sti_g, "data_ipk_sti_g.csv")
                rank = rank_index(data_ipk_sti_g, ipk)

                print(f"Rata-rata indeks: {mean_sti_g}")
                print(f"Peringkatmu: {rank}")
                print("========================")

            elif dataset == 4:
                data_ipk_sti_j = open_file(data_ipk_sti_j, "data_ipk_sti_j.csv")
                rank = rank_index(data_ipk_sti_j, ipk)

                print(f"Rata-rata indeks: {mean_sti_j}")
                print(f"Peringkatmu: {rank}")
                print("========================")

            else:
                data_ipk_total = open_file(data_ipk_total, "data_ipk_total.csv")
                rank = rank_index(data_ipk_total, ipk)

                print(f"Rata-rata indeks: {mean_total}")
                print(f"Peringkatmu: {rank}")
                print("========================")

        # ============================
        # 2. Hitung peluang jurusan
        # ============================
        elif pilihan == 2:
            print("\n=== PILIH JURUSAN ===\n"
                  "1. Informatika Ganesha\n"
                  "2. Informatika Jatinangor\n"
                  "3. Sistem dan Teknologi Informasi Ganesha\n"
                  "4. Sistem dan Teknologi Informasi Jatinangor")

            pilihan_jurusan = [0 for i in range(4)]
            for i in range(4):
                pilihan_jurusan[i] = prog_utils.retry_input_range("i", f"Pilihan {i+1}: ", 1, 4)

            xi_if_g = math_functions.compute_xi(mean_if_g, omega, alpha)
            xi_if_j = math_functions.compute_xi(mean_if_j, omega, alpha)
            xi_sti_g = math_functions.compute_xi(mean_sti_g, omega, alpha)
            xi_sti_j = math_functions.compute_xi(mean_sti_j, omega, alpha)

            probabilitas = [0 for i in range(4)]
            probabilitas[0] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_g, omega, alpha)
            probabilitas[1] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_j, omega, alpha)
            probabilitas[2] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_g, omega, alpha)
            probabilitas[3] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_j, omega, alpha)

            print("\nJadi, probabilitasmu untuk memasuki masing-masing jurusan adalah:")
            for i in range(4):
                print(f"{i+1}. Pilihan {i+1} \"{nama_jurusan[pilihan_jurusan[i]-1]}\": {(100 * probabilitas[i]):.2f}%")

        # ============================
        # 3. Rekomendasi
        # ============================
        elif pilihan == 3:
            print("\n=== REKOMENDASI BERDASARKAN IPK GABUNGAN ===")

            xi_total = math_functions.compute_xi(mean_total, omega, alpha)
            P_eval = math_functions.truncated_skew_norm_cdf(ipk, xi_total, omega, alpha)

            print(f"IPK Anda: {ipk} (Rata-rata Kelompok: {mean_total})")
            print(f"Indeks Kuantil (Peluang Kumulatif): {(100 * P_eval):.2f}%")

            print("\nPoin Rekomendasi:")
            if P_eval >= 0.85:
                print("Kategori: Prestasi Sangat Tinggi.")
                print("1. Ambil program pertukaran atau double degree.")
                print("2. Mulai proyek riset dan targetkan publikasi.")
                print("3. Ambil posisi kepemimpinan profesional.")

            elif P_eval >= 0.30:
                print("Kategori: Prestasi Baik.")
                print("1. Ambil sertifikasi industri.")
                print("2. Cari kesempatan magang.")
                print("3. Perluas jaringan profesional (seminar/workshop).")

            else:
                print("Kategori: Perlu Peningkatan.")
                print("1. Fokus pada mata kuliah fundamental.")
                print("2. Perbaiki manajemen waktu.")
                print("3. Targetkan kenaikan IPK 0.1–0.2.")

            if ipk > mean_total:
                print(f"\nAnda berada di atas rata-rata ({mean_total}). Terus pertahankan!")
            elif ipk == mean_total:
                print(f"\nIPK Anda sama dengan rata-rata angkatan.")
            else:
                print(f"\nAnda berada di bawah rata-rata ({mean_total}). Fokus di mata kuliah berbobot tinggi.")


if __name__ == "__main__":
    main()
