"""Huong 3 - Quan ly do an / khoa luan: ghep cap GV-SV, tien do (milestone), chong trung ten de tai."""
import difflib
import unicodedata
from datetime import datetime

from dulieu import du_lieu, nhap_so, ghi_log, luu

NGUONG_TRUNG = 0.8
GIAI_DOAN = ["Tuan 1: De cuong", "Tuan 2: Phan tich thiet ke", "Tuan 3: Cai dat", "Tuan 4: Bao cao cuoi"]
TEN_TRANG_THAI = {"cho_duyet": "Cho giang vien duyet", "da_duyet": "Dang thuc hien", "tu_choi": "Bi tu choi"}


def _chuan_hoa(van_ban):
    """Bo dau tieng Viet, ve chu thuong, gop khoang trang de so sanh."""
    van_ban = van_ban.replace("đ", "d").replace("Đ", "D")
    nfd = unicodedata.normalize("NFD", van_ban)
    return " ".join("".join(c for c in nfd if unicodedata.category(c) != "Mn").lower().split())


def tim_de_tai_tuong_tu(ten_moi):
    """Tra ve (do tuong dong 0..1, de tai giong nhat) so voi cac de tai chua bi tu choi."""
    tot = (0.0, None)
    moi = _chuan_hoa(ten_moi)
    for dt in du_lieu["de_tai"]:
        if dt["trang_thai"] == "tu_choi":
            continue
        do = difflib.SequenceMatcher(None, moi, _chuan_hoa(dt["ten"])).ratio()
        if do > tot[0]:
            tot = (do, dt)
    return tot


def _de_tai_cua_sv(ma_sv):
    return next((d for d in du_lieu["de_tai"] if d["ma_sv"] == ma_sv and d["trang_thai"] != "tu_choi"), None)


def _ten_sv(ma_sv):
    sv = next((s for s in du_lieu["sinh_vien"] if s["ma_sv"] == ma_sv), None)
    return sv["ten"] if sv else ma_sv


def _in_de_tai(dt):
    da_nop = sum(1 for m in dt["moc"] if m["bao_cao"])
    diem = [m["diem"] for m in dt["moc"] if m["diem"] is not None]
    tb = f"{sum(diem) / len(diem):.1f}" if diem else "-"
    print(f"  #{dt['id']} {dt['ten']}")
    print(f"     SV: {dt['ma_sv']} - {_ten_sv(dt['ma_sv'])} | GVHD: {dt['gv']} | {TEN_TRANG_THAI[dt['trang_thai']]}")
    print(f"     Da nop {da_nop}/{len(dt['moc'])} giai doan | Diem qua trinh TB: {tb}")


def de_xuat_de_tai(ma_sv):
    if ma_sv not in [s["ma_sv"] for s in du_lieu["sinh_vien"]]:
        print("Khong tim thay sinh vien.")
        return
    if _de_tai_cua_sv(ma_sv):
        print("Ban da co de tai dang cho duyet hoac dang thuc hien.")
        return
    gvs = [t for t in du_lieu["tai_khoan"] if t["vai_tro"] == "giang_vien"]
    print("Danh sach giang vien huong dan:")
    for g in gvs:
        print(f"  {g['ten_dn']:<8}{g['ho_ten']:<20}Chuyen nganh: {g['chuyen_nganh']}")
    gv = input("Chon giang vien (nhap ten dang nhap): ").strip()
    if gv not in [g["ten_dn"] for g in gvs]:
        print("Giang vien khong hop le.")
        return
    ten = input("Ten de tai de xuat: ").strip()
    if not ten:
        print("Ten de tai khong duoc de trong.")
        return
    do, giong = tim_de_tai_tuong_tu(ten)
    if do >= NGUONG_TRUNG:
        print(f"De tai bi tu choi: giong {do * 100:.0f}% voi de tai '{giong['ten']}' (#{giong['id']}). Hay doi ten khac.")
        ghi_log("DE_TAI_TRUNG", f"{ma_sv} | '{ten}' ~ #{giong['id']} ({do:.2f})")
        return
    if do >= 0.6:
        print(f"Luu y: ten gan giong ({do * 100:.0f}%) voi de tai '{giong['ten']}'.")
    moi = max((d["id"] for d in du_lieu["de_tai"]), default=0) + 1
    du_lieu["de_tai"].append({
        "id": moi, "ten": ten, "ma_sv": ma_sv, "gv": gv, "trang_thai": "cho_duyet",
        "moc": [{"giai_doan": g, "bao_cao": "", "ngay_nop": "", "nhan_xet": "", "diem": None} for g in GIAI_DOAN],
    })
    luu()
    ghi_log("DE_XUAT_DE_TAI", f"#{moi} | {ma_sv} | {ten} | GV {gv}")
    print(f"Da gui de xuat de tai #{moi}, cho giang vien {gv} duyet.")


def gv_duyet_de_tai(gv):
    cho = [d for d in du_lieu["de_tai"] if d["gv"] == gv and d["trang_thai"] == "cho_duyet"]
    if not cho:
        print("Khong co de tai nao dang cho duyet.")
        return
    for d in cho:
        _in_de_tai(d)
    ma = nhap_so("Nhap id de tai can xu ly (0 de bo qua): ", int, 0)
    dt = next((d for d in cho if d["id"] == ma), None)
    if not dt:
        return
    chon = nhap_so("1 = Chap nhan huong dan, 2 = Tu choi: ", int, 1, 2)
    dt["trang_thai"] = "da_duyet" if chon == 1 else "tu_choi"
    luu()
    ghi_log("DUYET_DE_TAI", f"#{dt['id']} -> {dt['trang_thai']}")
    print("Da cap nhat trang thai de tai.")


def nop_bao_cao(ma_sv):
    dt = _de_tai_cua_sv(ma_sv)
    if not dt:
        print("Ban chua co de tai.")
        return
    if dt["trang_thai"] != "da_duyet":
        print("De tai chua duoc giang vien duyet.")
        return
    moc = next((m for m in dt["moc"] if not m["bao_cao"]), None)
    if not moc:
        print("Ban da nop du cac giai doan.")
        return
    print(f"Giai doan can nop: {moc['giai_doan']}")
    noi_dung = input("Noi dung bao cao / ten file nop: ").strip()
    if not noi_dung:
        print("Noi dung khong duoc de trong.")
        return
    moc["bao_cao"] = noi_dung
    moc["ngay_nop"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    luu()
    ghi_log("NOP_BAO_CAO", f"#{dt['id']} | {moc['giai_doan']}")
    print("Nop bao cao thanh cong.")


def gv_cham_bao_cao(gv):
    cho = [d for d in du_lieu["de_tai"]
           if d["gv"] == gv and d["trang_thai"] == "da_duyet"
           and any(m["bao_cao"] and m["diem"] is None for m in d["moc"])]
    if not cho:
        print("Khong co bao cao nao cho cham.")
        return
    for d in cho:
        _in_de_tai(d)
    ma = nhap_so("Nhap id de tai can cham (0 de bo qua): ", int, 0)
    dt = next((d for d in cho if d["id"] == ma), None)
    if not dt:
        return
    moc = next(m for m in dt["moc"] if m["bao_cao"] and m["diem"] is None)
    print(f"{moc['giai_doan']} | nop luc {moc['ngay_nop']}\n  Noi dung: {moc['bao_cao']}")
    moc["nhan_xet"] = input("Nhan xet: ").strip()
    moc["diem"] = nhap_so("Diem qua trinh (0-10): ", float, 0, 10)
    luu()
    ghi_log("CHAM_BAO_CAO", f"#{dt['id']} | {moc['giai_doan']} | {moc['diem']}")
    print("Da cham diem va luu nhan xet.")


def xem_tien_do_do_an(ma_sv=None, gv=None):
    ds = [d for d in du_lieu["de_tai"]
          if (ma_sv is None or d["ma_sv"] == ma_sv) and (gv is None or d["gv"] == gv)]
    if not ds:
        print("Chua co de tai nao.")
        return
    for d in ds:
        _in_de_tai(d)
        if ma_sv:
            for m in d["moc"]:
                trang_thai = "Chua nop" if not m["bao_cao"] else (f"Diem {m['diem']}" if m["diem"] is not None else "Cho cham")
                nx = f" | Nhan xet: {m['nhan_xet']}" if m["nhan_xet"] else ""
                print(f"       - {m['giai_doan']:<30}{trang_thai}{nx}")
