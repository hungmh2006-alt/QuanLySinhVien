"""Du lieu dung chung: luu/doc JSON, nhat ky thao tac (audit log), phien dang nhap, ham nhap lieu."""
import hashlib
import json
import os
from datetime import datetime

FILE_DU_LIEU = "data.json"
FILE_LOG = "audit.log"

du_lieu = {
    "sinh_vien": [],   # {ma_sv, ten, tuoi}
    "mon_hoc": [],     # {ma_mon, ten_mon, tin_chi, tien_quyet, lich}
    "diem": [],        # {ma_sv, ma_mon, hoc_ky, diem}
    "dang_ky": [],     # {ma_sv, ma_mon, hoc_ky}
    "de_tai": [],      # {id, ten, ma_sv, gv, trang_thai, moc}
    "tai_khoan": [],   # {ten_dn, mat_khau, vai_tro, ho_ten, chuyen_nganh}
}
phien = {"tai_khoan": None}


def bam(mat_khau):
    return hashlib.sha256(mat_khau.encode("utf-8")).hexdigest()


def luu():
    with open(FILE_DU_LIEU, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=2)


def _khoi_tao_mac_dinh():
    du_lieu["tai_khoan"].extend([
        {"ten_dn": "admin", "mat_khau": bam("admin123"), "vai_tro": "admin",
         "ho_ten": "Phong Dao Tao", "chuyen_nganh": ""},
        {"ten_dn": "gv01", "mat_khau": bam("gv123"), "vai_tro": "giang_vien",
         "ho_ten": "Nguyen Van A", "chuyen_nganh": "Phan mem"},
        {"ten_dn": "gv02", "mat_khau": bam("gv123"), "vai_tro": "giang_vien",
         "ho_ten": "Tran Thi B", "chuyen_nganh": "Mang may tinh"},
    ])
    du_lieu["mon_hoc"].extend([
        {"ma_mon": "INT101", "ten_mon": "Nhap mon lap trinh", "tin_chi": 3,
         "tien_quyet": [], "lich": ["T2-1", "T4-1"]},
        {"ma_mon": "MAT101", "ten_mon": "Toan roi rac", "tin_chi": 2,
         "tien_quyet": [], "lich": ["T3-3"]},
        {"ma_mon": "ENG101", "ten_mon": "Tieng Anh 1", "tin_chi": 3,
         "tien_quyet": [], "lich": ["T6-3"]},
        {"ma_mon": "INT102", "ten_mon": "Cau truc du lieu", "tin_chi": 3,
         "tien_quyet": ["INT101"], "lich": ["T3-1", "T5-1"]},
        {"ma_mon": "INT103", "ten_mon": "Co so du lieu", "tin_chi": 3,
         "tien_quyet": ["INT101"], "lich": ["T3-1", "T6-1"]},
        {"ma_mon": "INT201", "ten_mon": "Lap trinh huong doi tuong", "tin_chi": 3,
         "tien_quyet": ["INT101"], "lich": ["T4-3", "T6-5"]},
    ])


def tai():
    """Doc du lieu tu data.json (giu nguyen doi tuong list de cac module khac dung chung)."""
    if os.path.exists(FILE_DU_LIEU):
        with open(FILE_DU_LIEU, "r", encoding="utf-8") as f:
            data = json.load(f)
        for khoa in du_lieu:
            du_lieu[khoa][:] = data.get(khoa, [])
    else:
        _khoi_tao_mac_dinh()
        luu()


def ghi_log(hanh_dong, chi_tiet=""):
    """Ghi nhat ky: thoi gian | nguoi thuc hien | hanh dong | chi tiet."""
    nguoi = phien["tai_khoan"]["ten_dn"] if phien["tai_khoan"] else "he_thong"
    with open(FILE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {nguoi} | {hanh_dong} | {chi_tiet}\n")


def nhap_so(thong_bao, kieu=int, tu=None, den=None):
    """Nhap so, lap lai den khi hop le va nam trong khoang [tu, den]."""
    while True:
        try:
            gia_tri = kieu(input(thong_bao))
        except ValueError:
            print("Gia tri khong hop le, vui long nhap so.")
            continue
        if (tu is not None and gia_tri < tu) or (den is not None and gia_tri > den):
            print(f"Gia tri phai nam trong khoang {tu} - {den}.")
            continue
        return gia_tri


SV_MAU = [("SV01", "An", 19), ("SV02", "Binh", 19), ("SV03", "Chi", 20),
          ("SV04", "Dung", 20), ("SV05", "Em", 19), ("SV06", "Phuc", 21)]
DIEM_MAU = {"SV01": (8.5, 7.0), "SV02": (5.0, 4.5), "SV03": (3.0, 6.0),
            "SV04": (7.0, 3.5), "SV05": (9.0, 8.0), "SV06": (6.5, 5.5)}
DANG_KY_MAU = [("SV01", "INT102"), ("SV01", "INT201"), ("SV05", "INT103"),
               ("SV05", "INT201"), ("SV06", "INT102"), ("SV06", "ENG101"),
               ("SV04", "INT103"), ("SV04", "ENG101"), ("SV02", "INT102")]


def nap_du_lieu_mau():
    """Them 6 sinh vien mau (mat khau 123456), diem hoc ky 2025-2 va dang ky hoc ky 2026-1."""
    them = 0
    for ma, ten, tuoi in SV_MAU:
        if any(s["ma_sv"] == ma for s in du_lieu["sinh_vien"]):
            continue
        du_lieu["sinh_vien"].append({"ma_sv": ma, "ten": ten, "tuoi": tuoi})
        du_lieu["tai_khoan"].append({"ten_dn": ma, "mat_khau": bam("123456"),
                                     "vai_tro": "sinh_vien", "ho_ten": ten, "chuyen_nganh": ""})
        d1, d2 = DIEM_MAU[ma]
        du_lieu["diem"].append({"ma_sv": ma, "ma_mon": "INT101", "hoc_ky": "2025-2", "diem": d1})
        du_lieu["diem"].append({"ma_sv": ma, "ma_mon": "MAT101", "hoc_ky": "2025-2", "diem": d2})
        them += 1
    for ma, mon in DANG_KY_MAU:
        dk = {"ma_sv": ma, "ma_mon": mon, "hoc_ky": "2026-1"}
        if dk not in du_lieu["dang_ky"] and any(s["ma_sv"] == ma for s in du_lieu["sinh_vien"]):
            du_lieu["dang_ky"].append(dk)
    luu()
    ghi_log("NAP_DU_LIEU_MAU", f"them {them} sinh vien")
    print(f"Da nap du lieu mau ({them} sinh vien moi, mat khau 123456).")
