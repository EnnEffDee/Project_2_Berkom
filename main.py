import math_functions
import prog_utils
import csv

def rank_index(array, val):
    rank = 1  # mulai dari 1
    for ipk in array:
        if ipk > val:
            rank += 1
    return rank 

def open_file(file_name, n):
    data = [0.0 for _ in range(n)]
    k = 0
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data[k] = float(row[0])
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

    data_ipk_total = [0.0 for _ in range(285)]
    data_ipk_if_g = [0.0 for _ in range(72)]
    data_ipk_if_j = [0.0 for _ in range(71)]
    data_ipk_sti_g = [0.0 for _ in range(71)]
    data_ipk_sti_j = [0.0 for _ in range(71)]

    nama_jurusan = [
        "Informatika Ganesha",
        "Informatika Jatinangor",
        "Sistem dan Teknologi Informasi Ganesha",
        "Sistem dan Teknologi Informasi Jatinangor"
    ]

    ipk = float(prog_utils.retry_input_range("f", "Masukkan indeks prestasi kumulatif (IPK) Anda: ", 0, 4))

    while True:
        print("\n\n\n====================================")
        print("Apa yang ingin Anda lakukan?\n1. Menampilkan nilai indeks angkatan\n2. Menghitung peluang memasuki jurusan\n3. Memberikan rekomendasi\n4. Keluar")
        print("====================================")
        pilihan = prog_utils.retry_input_range("i", "Pilihan: ", 1, 4)

        if pilihan == 4:
            print("Terima kasih!")
            return 0

        elif pilihan == 1:
            print("\n\n=== PILIH DATASET ===\n1. Informatika Ganesha\n2. Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor\n5. Total Gabungan")
            print("========================")
            dataset = prog_utils.retry_input_range("i", "Pilihan: ", 1, 5)

            print("------------------------")

            if dataset == 1:
                data_ipk_if_g = open_file("data_ipk_if_g.csv", 72)
                rank = rank_index(data_ipk_if_g, ipk)
                print(f"\nRata-rata indeks: {mean_if_g}\nPeringkatmu: {rank} dari {len(data_ipk_if_g)}")
                print("------------------------")
            elif dataset == 2:
                data_ipk_if_j = open_file("data_ipk_if_j.csv", 71)
                rank = rank_index(data_ipk_if_j, ipk)
                print(f"\nRata-rata indeks: {mean_if_j}\nPeringkatmu: {rank} dari {len(data_ipk_if_j)}")
                print("------------------------")
            elif dataset == 3:
                data_ipk_sti_g = open_file("data_ipk_sti_g.csv", 71)
                rank = rank_index(data_ipk_sti_g, ipk)
                print(f"\nRata-rata indeks: {mean_sti_g}\nPeringkatmu: {rank} dari {len(data_ipk_sti_g)}")
                print("------------------------")
            elif dataset == 4:
                data_ipk_sti_j = open_file("data_ipk_sti_j.csv", 71)
                rank = rank_index(data_ipk_sti_j, ipk)
                print(f"\nRata-rata indeks: {mean_sti_j}\nPeringkatmu: {rank} dari {len(data_ipk_sti_j)}")
                print("------------------------")
            else:
                data_ipk_total = open_file("data_ipk_total.csv", 285)
                rank = rank_index(data_ipk_total, ipk)
                print(f"\nRata-rata indeks: {mean_total}\nPeringkatmu: {rank} dari {len(data_ipk_total)}")
                print("------------------------")

        elif pilihan == 2:
            print("\n\n=== PILIH JURUSAN ===\n1. Informatika Ganesha\n2. Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor")
            print("========================")

            pilihan_jurusan = [0 for _ in range(4)]
            for i in range(4):
                pilihan_jurusan[i] = int(prog_utils.retry_input_range("i", f"Pilihan {i + 1}: ", 1, 4))

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

            print("------------------------")
            print("Jadi, probabilitasmu untuk memasuki masing-masing jurusan adalah ")
            for i in range(4):
                jurusan = nama_jurusan[pilihan_jurusan[i] - 1]
                print(f"{i + 1}. Pilihan {i + 1} \"{jurusan}\": {100 * probs[i]:.2f}%")

        else:
            print("\n\n=== REKOMENDASI BERDASARKAN IPK GABUNGAN ===")

            xi_total = math_functions.compute_xi(mean_total, omega, alpha)
            P_eval = math_functions.truncated_skew_norm_cdf(ipk, xi_total, omega, alpha)

            print("========================")
            print(f"IPK Anda: {ipk} (Rata-rata Kelompok: {mean_total})")
            print(f"Indeks Kuantil (Peluang Kumulatif): {(100 * P_eval):.2f}%")
            print("========================")

            print("\n- Poin Rekomendasi -")
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

            print("------------------------")
            print("\nTambahan:")
            if ipk > mean_total:
                print(f"Anda berada di atas rata-rata ({mean_total}). Terus pertahankan!")
            elif ipk == mean_total:
                print(f"IPK Anda berada sama dengan di rata-rata angkatan ({mean_total}).")
            else:
                print(f"IPK Anda di bawah rata-rata ({mean_total}). Fokus di mata kuliah berbobot tinggi seperti matematika, fisika, dan kimia.")
            print("------------------------")

if __name__ == "__main__":
    main()
