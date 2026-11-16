# Danh sach sinh vien
danh_sach_sinh_vien = []


def _nhap_tuoi(thong_bao="Nhap tuoi: "):
    # Lap lai den khi nhap dung so nguyen duong
    while True:
        try:
            tuoi = int(input(thong_bao))
            if tuoi > 0:
                return tuoi
            print("Tuoi phai lon hon 0.")
        except ValueError:
            print("Vui long nhap so nguyen.")


def _tim_theo_ma(ma_sv):
    for sv in danh_sach_sinh_vien:
        if sv["ma_sv"] == ma_sv:
            return sv
    return None


# Them sinh vien
def them_sinh_vien():
    ma_sv = input("Nhap ma sinh vien: ").strip()
    if _tim_theo_ma(ma_sv):
        print("Ma sinh vien da ton tai!")
        return
    ten = input("Nhap ten sinh vien: ").strip()
    tuoi = _nhap_tuoi()

    sinh_vien = {
        "ma_sv": ma_sv,
        "ten": ten,
        "tuoi": tuoi
    }

    danh_sach_sinh_vien.append(sinh_vien)
    print("Them sinh vien thanh cong!")


# Hien thi sinh vien
def hien_thi_sinh_vien():
    if not danh_sach_sinh_vien:
        print("Danh sach trong.")
        return
    for sv in danh_sach_sinh_vien:
        print(sv)


# Tim sinh vien theo ma
def tim_sinh_vien():
    ma_sv = input("Nhap ma sinh vien can tim: ").strip()
    sv = _tim_theo_ma(ma_sv)
    if sv:
        print(sv)
    else:
        print("Sinh vien khong ton tai!")


# Xoa sinh vien theo ma
def xoa_sinh_vien():
    ma_sv = input("Nhap ma sinh vien can xoa: ").strip()
    sv = _tim_theo_ma(ma_sv)
    if sv:
        danh_sach_sinh_vien.remove(sv)
        print("Xoa sinh vien thanh cong!")
    else:
        print("Sinh vien khong ton tai!")


# Sua thong tin sinh vien
def sua_sinh_vien():
    ma_sv = input("Nhap ma sinh vien can sua: ").strip()
    sv = _tim_theo_ma(ma_sv)
    if not sv:
        print("Sinh vien khong ton tai!")
        return
    ten_moi = input("Nhap ten moi (Enter de giu nguyen): ").strip()
    if ten_moi:
        sv["ten"] = ten_moi
    sv["tuoi"] = _nhap_tuoi("Nhap tuoi moi: ")
    print("Sua thong tin thanh cong!")
