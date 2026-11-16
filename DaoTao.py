"""Huong 1 - Quan ly dao tao: mon hoc, diem, GPA, canh bao hoc vu, dang ky tin chi, tien do tot nghiep."""
import csv
import re

from dulieu import du_lieu, nhap_so, ghi_log, luu

DIEM_QUA_MON = 4.0          # diem he 10 toi thieu de qua mon
NGUONG_MUC_1 = 1.5          # GPA < 1.5 -> canh bao muc 1
NGUONG_MUC_2 = 1.0          # GPA < 1.0 -> canh bao muc 2
NGUONG_NO_TIN_CHI = 6       # no tu 6 tin chi tro len -> it nhat muc 1
MAU_LICH = re.compile(r"^T[2-7]-([1-9]|1[0-2])$")   # vd T2-1 = thu 2, tiet 1
BANG_QUY_DOI = [(8.5, 4.0), (8.0, 3.5), (7.0, 3.0), (6.5, 2.5), (5.5, 2.0), (5.0, 1.5), (4.0, 1.0)]


def quy_doi_4(diem):
    for nguong, he4 in BANG_QUY_DOI:
        if diem >= nguong:
            return he4
    return 0.0


def tim_mon(ma_mon):
    for m in du_lieu["mon_hoc"]:
        if m["ma_mon"] == ma_mon:
            return m
    return None


def _tin_chi(ma_mon):
    mon = tim_mon(ma_mon)
    return mon["tin_chi"] if mon else 0


def _lay_sv(ma_sv=None):
    if ma_sv is None:
        ma_sv = input("Nhap ma sinh vien: ").strip()
    sv = next((s for s in du_lieu["sinh_vien"] if s["ma_sv"] == ma_sv), None)
    if not sv:
        print("Sinh vien khong ton tai!")
    return sv


# ---------- Mon hoc ----------
def them_mon_hoc():
    ma = input("Ma mon hoc: ").strip().upper()
    if not ma or tim_mon(ma):
        print("Ma mon trong hoac da ton tai!")
        return
    ten = input("Ten mon hoc: ").strip()
    tin_chi = nhap_so("So tin chi (1-6): ", int, 1, 6)
    tq = [x.strip().upper() for x in input("Mon tien quyet (cach nhau dau phay, Enter neu khong co): ").split(",") if x.strip()]
    for m in tq:
        if not tim_mon(m):
            print(f"Mon tien quyet {m} chua ton tai trong khung chuong trinh!")
            return
    lich = [x.strip().upper() for x in input("Lich hoc (vd T2-1,T4-1 = thu 2 tiet 1, thu 4 tiet 1): ").split(",") if x.strip()]
    for ca in lich:
        if not MAU_LICH.match(ca):
            print(f"Sai dinh dang lich '{ca}' (dung: T2..T7 - tiet 1..12, vd T3-2).")
            return
    du_lieu["mon_hoc"].append({"ma_mon": ma, "ten_mon": ten, "tin_chi": tin_chi,
                               "tien_quyet": tq, "lich": lich})
    luu()
    ghi_log("THEM_MON", f"{ma} | {ten} | {tin_chi} TC | tien quyet: {tq}")
    print("Them mon hoc thanh cong!")


def hien_thi_mon_hoc():
    if not du_lieu["mon_hoc"]:
        print("Chua co mon hoc.")
        return
    print(f"  {'Ma':<8}{'Ten mon':<28}{'TC':<4}{'Tien quyet':<14}Lich")
    for m in du_lieu["mon_hoc"]:
        print(f"  {m['ma_mon']:<8}{m['ten_mon']:<28}{m['tin_chi']:<4}{','.join(m['tien_quyet']) or '-':<14}{','.join(m['lich']) or '-'}")


# ---------- Nhap diem (giang vien) ----------
def nhap_diem():
    sv = _lay_sv()
    if not sv:
        return
    ma_mon = input("Ma mon hoc: ").strip().upper()
    if not tim_mon(ma_mon):
        print("Mon hoc khong ton tai!")
        return
    hoc_ky = input("Hoc ky (vd 2026-1): ").strip()
    diem = nhap_so("Diem (0-10): ", float, 0, 10)
    ban_ghi = next((b for b in du_lieu["diem"]
                    if b["ma_sv"] == sv["ma_sv"] and b["ma_mon"] == ma_mon and b["hoc_ky"] == hoc_ky), None)
    if ban_ghi:
        cu = ban_ghi["diem"]
        ban_ghi["diem"] = diem
        ghi_log("SUA_DIEM", f"{sv['ma_sv']} | {ma_mon} | {hoc_ky} | {cu} -> {diem}")
        print(f"Da sua diem: {cu} -> {diem} (da ghi nhat ky).")
    else:
        du_lieu["diem"].append({"ma_sv": sv["ma_sv"], "ma_mon": ma_mon, "hoc_ky": hoc_ky, "diem": diem})
        ghi_log("NHAP_DIEM", f"{sv['ma_sv']} | {ma_mon} | {hoc_ky} | {diem}")
        print("Da nhap diem.")
    luu()


# ---------- GPA va canh bao hoc vu ----------
def _diem_theo_mon(ma_sv, hoc_ky=None):
    """{ma_mon: diem}. Khong chon hoc ky -> lay diem cao nhat cua moi mon (hoc lai se thay the)."""
    ket_qua = {}
    for b in du_lieu["diem"]:
        if b["ma_sv"] != ma_sv or (hoc_ky and b["hoc_ky"] != hoc_ky):
            continue
        ket_qua[b["ma_mon"]] = max(b["diem"], ket_qua.get(b["ma_mon"], -1))
    return ket_qua


def tinh_gpa(ma_sv, hoc_ky=None):
    tong, tong_tc = 0.0, 0
    for ma_mon, diem in _diem_theo_mon(ma_sv, hoc_ky).items():
        tc = _tin_chi(ma_mon)
        tong += quy_doi_4(diem) * tc
        tong_tc += tc
    return tong / tong_tc if tong_tc else None


def tin_chi_no(ma_sv):
    return sum(_tin_chi(m) for m, d in _diem_theo_mon(ma_sv).items() if d < DIEM_QUA_MON)


def tin_chi_tich_luy(ma_sv):
    return sum(_tin_chi(m) for m, d in _diem_theo_mon(ma_sv).items() if d >= DIEM_QUA_MON)


def muc_canh_bao(gpa, tc_no):
    muc = 0
    if gpa is not None:
        if gpa < NGUONG_MUC_2:
            muc = 2
        elif gpa < NGUONG_MUC_1:
            muc = 1
    if tc_no >= NGUONG_NO_TIN_CHI:
        muc = max(muc, 1)
    return muc


def xem_diem(ma_sv=None):
    sv = _lay_sv(ma_sv)
    if not sv:
        return
    ma = sv["ma_sv"]
    print(f"\nBang diem: {ma} - {sv['ten']}")
    ban_ghi = sorted((b for b in du_lieu["diem"] if b["ma_sv"] == ma),
                     key=lambda b: (b["hoc_ky"], b["ma_mon"]))
    if not ban_ghi:
        print("  Chua co diem.")
        return
    for b in ban_ghi:
        mon = tim_mon(b["ma_mon"])
        ten_mon = mon["ten_mon"] if mon else b["ma_mon"]
        kq = "Dat" if b["diem"] >= DIEM_QUA_MON else "Rot"
        print(f"  {b['hoc_ky']} | {b['ma_mon']:<7}{ten_mon:<26}| {b['diem']:>4.1f} (he 4: {quy_doi_4(b['diem']):.1f}) | {kq}")
    for hk in sorted({b["hoc_ky"] for b in ban_ghi}):
        print(f"  GPA hoc ky {hk}: {tinh_gpa(ma, hk):.2f}")
    gpa, no = tinh_gpa(ma), tin_chi_no(ma)
    print(f"  GPA tich luy: {gpa:.2f} | Tin chi tich luy: {tin_chi_tich_luy(ma)} | Tin chi no: {no}")
    muc = muc_canh_bao(gpa, no)
    if muc:
        print(f"  >>> CANH BAO HOC VU MUC {muc}")


def canh_bao_hoc_vu():
    """Quet toan bo sinh vien, gan co canh bao muc 1/2 va xuat danh sach gui co van hoc tap."""
    ds = []
    for sv in du_lieu["sinh_vien"]:
        gpa, no = tinh_gpa(sv["ma_sv"]), tin_chi_no(sv["ma_sv"])
        muc = muc_canh_bao(gpa, no)
        if muc:
            ds.append((muc, sv, gpa, no))
    if not ds:
        print("Khong co sinh vien nao bi canh bao hoc vu.")
        return
    ds.sort(key=lambda x: (-x[0], x[2] if x[2] is not None else 0))
    print(f"{'Muc':<5}{'Ma SV':<10}{'Ten':<20}{'GPA':<7}No TC")
    for muc, sv, gpa, no in ds:
        print(f"{muc:<5}{sv['ma_sv']:<10}{sv['ten']:<20}{gpa:<7.2f}{no}")
    with open("canh_bao_hoc_vu.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ma_sv", "ten", "gpa_tich_luy", "tin_chi_no", "muc_canh_bao", "ghi_chu"])
        for muc, sv, gpa, no in ds:
            w.writerow([sv["ma_sv"], sv["ten"], f"{gpa:.2f}", no, muc, "Gui co van hoc tap"])
    ghi_log("XUAT_CANH_BAO", f"{len(ds)} sinh vien")
    print(f"Da xuat danh sach gui co van hoc tap: canh_bao_hoc_vu.csv ({len(ds)} sinh vien)")


# ---------- Dang ky tin chi ----------
def _da_qua(ma_sv):
    return {m for m, d in _diem_theo_mon(ma_sv).items() if d >= DIEM_QUA_MON}


def goi_y_dang_ky(ma_sv=None):
    sv = _lay_sv(ma_sv)
    if not sv:
        return
    da_qua = _da_qua(sv["ma_sv"])
    goi_y = [m for m in du_lieu["mon_hoc"]
             if m["ma_mon"] not in da_qua and all(t in da_qua for t in m["tien_quyet"])]
    if not goi_y:
        print("Khong con mon nao de goi y.")
        return
    print("Cac mon co the dang ky (da qua tien quyet, chua qua mon):")
    for m in goi_y:
        print(f"  {m['ma_mon']:<8}{m['ten_mon']:<28}{m['tin_chi']} TC | Lich: {','.join(m['lich']) or '-'}")


def dang_ky_mon(ma_sv=None):
    sv = _lay_sv(ma_sv)
    if not sv:
        return
    ma = sv["ma_sv"]
    hoc_ky = input("Hoc ky dang ky (vd 2026-1): ").strip()
    ma_mon = input("Ma mon can dang ky: ").strip().upper()
    mon = tim_mon(ma_mon)
    if not mon:
        print("Mon hoc khong ton tai!")
        return
    da_qua = _da_qua(ma)
    if ma_mon in da_qua:
        print("Ban da qua mon nay roi.")
        return
    if any(d["ma_sv"] == ma and d["ma_mon"] == ma_mon and d["hoc_ky"] == hoc_ky for d in du_lieu["dang_ky"]):
        print("Ban da dang ky mon nay trong hoc ky nay.")
        return
    thieu = [t for t in mon["tien_quyet"] if t not in da_qua]
    if thieu:
        print(f"Khong the dang ky: chua qua mon tien quyet {', '.join(thieu)}.")
        return
    for d in du_lieu["dang_ky"]:
        if d["ma_sv"] == ma and d["hoc_ky"] == hoc_ky:
            khac = tim_mon(d["ma_mon"])
            trung = set(mon["lich"]) & set(khac["lich"] if khac else [])
            if trung:
                print(f"Khong the dang ky: trung lich {', '.join(sorted(trung))} voi mon {d['ma_mon']}.")
                return
    du_lieu["dang_ky"].append({"ma_sv": ma, "ma_mon": ma_mon, "hoc_ky": hoc_ky})
    luu()
    ghi_log("DANG_KY_MON", f"{ma} | {ma_mon} | {hoc_ky}")
    print(f"Dang ky thanh cong mon {ma_mon} - {mon['ten_mon']}.")


def tien_do_tot_nghiep(ma_sv=None):
    sv = _lay_sv(ma_sv)
    if not sv:
        return
    tong = sum(m["tin_chi"] for m in du_lieu["mon_hoc"])
    dat = tin_chi_tich_luy(sv["ma_sv"])
    ti_le = dat / tong * 100 if tong else 0
    o = int(ti_le // 5)
    print(f"Tien do tot nghiep cua {sv['ma_sv']} - {sv['ten']}")
    print(f"  [{'#' * o}{'.' * (20 - o)}] {dat}/{tong} tin chi ({ti_le:.0f}%)")
    da_qua = _da_qua(sv["ma_sv"])
    con_lai = [m["ma_mon"] for m in du_lieu["mon_hoc"] if m["ma_mon"] not in da_qua]
    print(f"  Con lai: {', '.join(con_lai) if con_lai else 'Da hoan thanh khung chuong trinh'}")
