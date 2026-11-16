"""Quan ly sinh vien (them, hien thi, tim, xoa, sua) - du lieu luu vao data.json."""
from dulieu import du_lieu, nhap_so, ghi_log, luu, bam

# Danh sach sinh vien (dung chung voi du_lieu["sinh_vien"] de duoc luu ra file)
danh_sach_sinh_vien = du_lieu["sinh_vien"]
MAT_KHAU_MAC_DINH = "123456"


def _tim_theo_ma(ma_sv):
    for sv in danh_sach_sinh_vien:
        if sv["ma_sv"] == ma_sv:
            return sv
    return None


def them_sv_vao_danh_sach(ma_sv, ten, tuoi):
    """Them sinh vien va tao tai khoan dang nhap (ten dn = ma sv). Tra ve False neu trung ma."""
    if not ma_sv or _tim_theo_ma(ma_sv):
        return False
    if any(tk["ten_dn"] == ma_sv for tk in du_lieu["tai_khoan"]):
        return False
    danh_sach_sinh_vien.append({"ma_sv": ma_sv, "ten": ten, "tuoi": tuoi})
    du_lieu["tai_khoan"].append({"ten_dn": ma_sv, "mat_khau": bam(MAT_KHAU_MAC_DINH),
                                 "vai_tro": "sinh_vien", "ho_ten": ten, "chuyen_nganh": ""})
    return True


def _in(sv):
    print(f"  Ma: {sv['ma_sv']:<10} | Ten: {sv['ten']:<22} | Tuoi: {sv['tuoi']}")


# Them sinh vien
def them_sinh_vien():
    ma_sv = input("Nhap ma sinh vien: ").strip()
    ten = input("Nhap ten sinh vien: ").strip()
    tuoi = nhap_so("Nhap tuoi: ", int, 1, 120)
    if them_sv_vao_danh_sach(ma_sv, ten, tuoi):
        luu()
        ghi_log("THEM_SV", f"{ma_sv} | {ten} | {tuoi}")
        print(f"Them sinh vien thanh cong! (tai khoan: {ma_sv} / mat khau: {MAT_KHAU_MAC_DINH})")
    else:
        print("Ma sinh vien trong hoac da ton tai!")


# Hien thi sinh vien
def hien_thi_sinh_vien():
    if not danh_sach_sinh_vien:
        print("Danh sach trong.")
        return
    for sv in danh_sach_sinh_vien:
        _in(sv)


# Tim sinh vien theo ma
def tim_sinh_vien():
    sv = _tim_theo_ma(input("Nhap ma sinh vien can tim: ").strip())
    if sv:
        _in(sv)
    else:
        print("Sinh vien khong ton tai!")


# Xoa sinh vien theo ma (xoa kem tai khoan, diem, dang ky, de tai)
def xoa_sinh_vien():
    ma_sv = input("Nhap ma sinh vien can xoa: ").strip()
    sv = _tim_theo_ma(ma_sv)
    if not sv:
        print("Sinh vien khong ton tai!")
        return
    danh_sach_sinh_vien.remove(sv)
    for khoa in ("tai_khoan", "diem", "dang_ky", "de_tai"):
        du_lieu[khoa][:] = [x for x in du_lieu[khoa]
                            if x.get("ma_sv", x.get("ten_dn")) != ma_sv]
    luu()
    ghi_log("XOA_SV", f"{ma_sv} | {sv['ten']}")
    print("Xoa sinh vien thanh cong!")


# Sua thong tin sinh vien
def sua_sinh_vien():
    ma_sv = input("Nhap ma sinh vien can sua: ").strip()
    sv = _tim_theo_ma(ma_sv)
    if not sv:
        print("Sinh vien khong ton tai!")
        return
    ten_cu, tuoi_cu = sv["ten"], sv["tuoi"]
    ten_moi = input("Nhap ten moi (Enter de giu nguyen): ").strip()
    if ten_moi:
        sv["ten"] = ten_moi
    sv["tuoi"] = nhap_so("Nhap tuoi moi: ", int, 1, 120)
    for tk in du_lieu["tai_khoan"]:
        if tk["ten_dn"] == ma_sv:
            tk["ho_ten"] = sv["ten"]
    luu()
    ghi_log("SUA_SV", f"{ma_sv} | ten: {ten_cu} -> {sv['ten']} | tuoi: {tuoi_cu} -> {sv['tuoi']}")
    print("Sua thong tin thanh cong!")
