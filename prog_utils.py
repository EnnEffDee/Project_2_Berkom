def validate_input(n, min, max):
    if n.isnumber():
        if min <= n <= max:
            return True
    return False

def retry_input(type, msg):
    while True:
        ans = input(msg)
        if type == "i":
            try:
                nilai_int = int(ans)
                return nilai_int
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan bulat (integer).")
        elif type == "f":
            try:
                nilai_float = float(ans)
                return nilai_float
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan desimal (float).")
        elif type == "c":
            if ans:
                return ans[0]
            else:
                print("Input tidak valid. Harap masukkan minimal satu karakter.")
        elif type == "s":
            if ans.strip():
                return ans
            else:
                print("Input tidak boleh kosong. Harap masukkan teks.")
        else:
            print(f"Peringatan: Tipe '{type}' tidak dikenali. Mengembalikan input mentah.")
            return ans

def retry_input_range(type, msg, min, max):
    while True:
        ans = input(msg)
        if type == "i":
            try:
                nilai_int = int(ans)
                if (min <= nilai_int <= max):
                    return nilai_int
                print(f"Input tidak berada di dalam batas {min} - {max}")
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan bulat (integer).")
        elif type == "f":
            try:
                nilai_float = float(ans)
                if (min <= nilai_float <= max):
                    return nilai_float
                print(f"Input tidak berada di dalam batas {min} - {max}")
            except ValueError:
                print("Input tidak valid. Harap masukkan bilangan desimal (float).")
        else:
            print(f"Peringatan: Tipe '{type}' tidak dikenali. Mengembalikan input mentah.")
            return ans
