"""Tinh nang chung: import/export CSV, dashboard thong ke, xem audit log."""
import csv
import os

from dulieu import du_lieu, ghi_log, luu, FILE_LOG
from sinhvien import them_sv_vao_danh_sach
from daotao import tim_mon, tinh_gpa, DIEM_QUA_MON, quy_doi_4


def nhap_csv_sinh_vien():
    duong_dan = input("Duong dan file CSV (cot: ma_sv,ten,tuoi): ").strip().strip('"')
    if not os.path.exists(duong_dan):
        print("Khong tim thay file.")
        return
    them = bo_qua = 0
    with open(duong_dan, newline="", encoding="utf-8-sig") as f:
        for dong in csv.DictReader(f):
            try:
                ok = them_sv_vao_danh_sach(dong["ma_sv"].strip(), dong["ten"].strip(), int(dong["tuoi"]))
            except (KeyError, ValueError, AttributeError):
                ok = False
            them, bo_qua = (them + 1, bo_qua) if ok else (them, bo_qua + 1)
    luu()
    ghi_log("NHAP_CSV", f"{duong_dan} | them {them}, bo qua {bo_qua}")
    print(f"Nhap xong: them {them} sinh vien, bo qua {bo_qua} dong loi/trung ma.")


def xuat_bang_diem_csv():
    ma = input("Ma sinh vien (Enter de xuat tat ca): ").strip()
    ten_sv = {s["ma_sv"]: s["ten"] for s in du_lieu["sinh_vien"]}
    ds = [b for b in du_lieu["diem"] if not ma or b["ma_sv"] == ma]
    if not ds:
        print("Khong co du lieu diem de xuat.")
        return
    ten_file = f"bang_diem_{ma or 'tat_ca'}.csv"
    with open(ten_file, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ma_sv", "ten", "ma_mon", "ten_mon", "tin_chi", "hoc_ky", "diem_10", "diem_4"])
        for b in sorted(ds, key=lambda x: (x["ma_sv"], x["hoc_ky"], x["ma_mon"])):
            mon = tim_mon(b["ma_mon"]) or {"ten_mon": "", "tin_chi": 0}
            w.writerow([b["ma_sv"], ten_sv.get(b["ma_sv"], ""), b["ma_mon"], mon["ten_mon"],
                        mon["tin_chi"], b["hoc_ky"], b["diem"], quy_doi_4(b["diem"])])
    ghi_log("XUAT_BANG_DIEM", ten_file)
    print(f"Da xuat {len(ds)} dong ra file {ten_file} (mo duoc bang Excel).")


def _xep_loai(gpa):
    if gpa >= 3.6:
        return "Xuat sac"
    if gpa >= 3.2:
        return "Gioi"
    if gpa >= 2.5:
        return "Kha"
    if gpa >= 2.0:
        return "Trung binh"
    return "Yeu"


def _thanh(so, toi_da, dai=30):
    return "#" * (round(so / toi_da * dai) if toi_da else 0)


def dashboard():
    dem = {k: 0 for k in ("Xuat sac", "Gioi", "Kha", "Trung binh", "Yeu")}
    chua_co = 0
    for sv in du_lieu["sinh_vien"]:
        gpa = tinh_gpa(sv["ma_sv"])
        if gpa is None:
            chua_co += 1
        else:
            dem[_xep_loai(gpa)] += 1
    print(f"=== Xep loai hoc luc (tong {len(du_lieu['sinh_vien'])} sinh vien) ===")
    toi_da = max(dem.values()) if dem else 0
    for k, v in dem.items():
        print(f"  {k:<11}{v:>3}  {_thanh(v, toi_da)}")
    print(f"  Chua co diem: {chua_co}")
    print("=== Ti le rot mon theo hoc ky ===")
    theo_hk = {}
    for b in du_lieu["diem"]:
        tong, rot = theo_hk.get(b["hoc_ky"], (0, 0))
        theo_hk[b["hoc_ky"]] = (tong + 1, rot + (b["diem"] < DIEM_QUA_MON))
    for hk in sorted(theo_hk):
        tong, rot = theo_hk[hk]
        print(f"  {hk}: {rot}/{tong} luot ({rot / tong * 100:.0f}%)  {_thanh(rot, tong, 20)}")
    if not theo_hk:
        print("  Chua co du lieu diem.")


def xem_audit_log(so_dong=20):
    if not os.path.exists(FILE_LOG):
        print("Chua co nhat ky thao tac.")
        return
    with open(FILE_LOG, encoding="utf-8") as f:
        dong = f.readlines()
    print(f"=== {min(so_dong, len(dong))} thao tac gan nhat (thoi gian | nguoi | hanh dong | chi tiet) ===")
    for d in dong[-so_dong:]:
        print(" ", d.rstrip())
