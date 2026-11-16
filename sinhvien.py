
# Danh sach sinh vien
danh_sach_sinh_vien = []

# Them sinh vien
def them_sinh_vien():
    ma_sv = input("Nhap ma sinh vien: ")
    ten = input("Nhap ten sinh vien: ")
    tuoi = int(input("Nhap tuoi: "))

    sinh_vien = {
        "ma_sv": ma_sv,
        "ten": ten,
        "tuoi": tuoi
    }

    danh_sach_sinh_vien.append(sinh_vien)
    print("Them sinh vien thanh cong!")

# Hien thi sinh vien
def hien_thi_sinh_vien():
    for sv in danh_sach_sinh_vien:
        print(sv)
