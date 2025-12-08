def retry_input_range(type, msg, min, max):
    while True:
        ans = input(msg).replace(",", ".")

        if type == "i":
            try:
                nilai_int = int(ans)
                min, max = int(min), int(max)
                if (min <= nilai_int <= max):
                    return nilai_int
                print(f"Input tidak berada di dalam batas {min} - {max}")
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan bulat (integer).")
        elif type == "f":
            try:
                nilai_float = float(ans)
                min, max = float(min), float(max)
                if (min <= nilai_float <= max):
                    return nilai_float
                print(f"Input tidak berada di dalam batas {min} - {max}")
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan desimal (float).")
        else:
            print(f"Peringatan: Tipe '{type}' tidak dikenali. Mengembalikan input mentah.")
            return ans
