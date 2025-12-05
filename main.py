import math_functions
import prog_utils
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
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if k >= len(data):
                break
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

    data_ipk_total = [0.0 for i in range(285)]
    data_ipk_if_g = [0.0 for i in range(72)]
    data_ipk_if_j = [0.0 for i in range(71)]
    data_ipk_sti_g = [0.0 for i in range(71)]
    data_ipk_sti_j = [0.0 for i in range(71)]

    nama_jurusan = ["Informatika Ganesha", "Informatika Jatinangor", "Sistem dan Teknologi Informasi Ganesha", "Sistem dan Teknologi Informasi Jatinangor"]

    ipk = float(input("Masukkan indeks prestasi kumulatif (IPK) Anda: "))
    if (prog_utils.validate_input(ipk, 0, 4) == False):
        print("Terjadi kesalahan input, cobalah lagi")
        return

    k = 0
    while True:
        print("Apa yang ingin Anda lakukan?\n1. Menampilkan nilai indeks angkatan\n2. Menghitung peluang memasuki jurusan\n3. Memberikan rekomendasi\n4. Keluar")
        pilihan = prog_utils.retry_input_range("i", "Pilihan: ", 1, 4)

        if pilihan == 4:
            print("Terima kasih!")
            return 0
        if pilihan == 1:
            print("\n=== PILIH DATASET ===\n1. Informatika Ganesha\n2.Informatika Jatinangor\n3. Sistem dan Teknologi Informasi Ganesha\n4. Sistem dan Teknologi Informasi Jatinangor\n5. Total Gabungan")
            dataset = prog_utils.retry_input_range("i", "Pilihan: ", 1, 5)

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
                pilihan[i] = int(prog_utils.retry_input_range("i", f"Pilihan {i + 1}: ", 1, 4))

            xi_if_g = math_functions.compute_xi(mean_if_g, omega, alpha)
            xi_if_j = math_functions.compute_xi(mean_if_j, omega, alpha)
            xi_sti_g = math_functions.compute_xi(mean_sti_g, omega, alpha)
            xi_sti_j = math_functions.compute_xi(mean_sti_j, omega, alpha)

            probabilitas = [0 for i in range(4)]
            probabilitas[0] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_g, omega, alpha)
            probabilitas[1] = math_functions.truncated_skew_norm_cdf(ipk, xi_if_j, omega, alpha)
            probabilitas[2] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_g, omega, alpha)
            probabilitas[3] = math_functions.truncated_skew_norm_cdf(ipk, xi_sti_j, omega, alpha)
            
            print("Jadi, probabilitasmu untuk memasuki masing-masing jurusan adalah ")
            for i in range(4):
                print(f"{i + 1}. Pilihan {i + 1} \"{nama_jurusan[pilihan[i] - 1]}\": {(100 * probabilitas[i]):.2f}%")
        elif pilihan == 3:
            print("\n=== REKOMENDASI BERDASARKAN IPK GABUNGAN ===")
            
            xi_total = math_functions.compute_xi(mean_total, omega, alpha)
            
            P_eval = math_functions.truncated_skew_norm_cdf(ipk, xi_total, omega, alpha)
            
            print(f"IPK Anda: {ipk} (Rata-rata Kelompok: {mean_total})")
            print(f"Indeks Kuantil (Peluang Kumulatif): {(100 * P_eval):.2f}%")
            
            print("\nPoin Rekomendasi:")
            
            if P_eval >= 0.85:
                print("Kategori: Prestasi Sangat Tinggi.")
                print("1. Coba Tantangan Internasional: Dianjurkan mengambil program pertukaran pelajar atau double-degree.")
                print("2. Riset & Publikasi: Fokus pada proyek riset dengan target publikasi jurnal/konferensi internasional.")
                print("3. Kepemimpinan Profesional: Ambil peran kepemimpinan di organisasi profesional atau jadi Asisten Dosen senior.")
            
            elif P_eval >= 0.30:
                print("Kategori: Prestasi Baik. Konsisten dan berkembang.")
                print("1. Ambil Sertifikasi: Tingkatkan skill set di luar kurikulum dengan sertifikasi industri (misal: Cloud, Data Science).")
                print("2. Pengalaman Kerja: Cari kesempatan magang di perusahaan besar untuk mengaplikasikan ilmu secara nyata.")
                print("3. Jaringan (Networking): Aktif hadiri seminar dan *workshop* untuk memperluas koneksi profesional.")
                
            else:
                print("Kategori: Perlu Fokus Peningkatan Akademik.")
                print("1. Fokus Mata Kuliah Dasar: Prioritaskan penguatan di mata kuliah kunci dan fundamental. Cari tutor atau kelompok belajar.")
                print("2. Manajemen Waktu: Tingkatkan efisiensi belajar dan kurangi distraksi. Konsultasi dengan dosen wali.")
                print("3. Perbaiki Nilai: Tetapkan target realistis untuk peningkatan IPK 0.1-0.2 poin pada semester berikutnya.")

            print("\nTambahan:")
            if ipk > mean_total:
                print(f"Anda berada di atas rata-rata ({mean_total}). Terus pertahankan!")
            elif ipk == mean_total:
                print(f"IPK Anda berada tepat di rata-rata kelompok. Pertahankan dan dorong sedikit lebih keras!")
            else:
                print(f"IPK Anda berada di bawah rata-rata ({mean_total}). Utamakan mata kuliah dengan bobot SKS tertinggi seperti Matematika.")

if __name__ == "__main__":
    main()
