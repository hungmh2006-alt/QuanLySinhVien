"""Huong 4 - Thuat toan & cau truc du lieu: BST, bang bam, to mau do thi de xep lich thi."""
import math
import random
import time

from dulieu import du_lieu

SUC_CHUA_PHONG = 40   # so thi sinh toi da moi phong thi


class _Nut:
    __slots__ = ("khoa", "gia_tri", "trai", "phai")

    def __init__(self, khoa, gia_tri):
        self.khoa, self.gia_tri, self.trai, self.phai = khoa, gia_tri, None, None


class CayNhiPhan:
    """Cay tim kiem nhi phan (BST): tim kiem trung binh O(log n)."""

    def __init__(self):
        self.goc = None

    def them(self, khoa, gia_tri):
        nut = _Nut(khoa, gia_tri)
        if self.goc is None:
            self.goc = nut
            return
        hien = self.goc
        while True:
            if khoa == hien.khoa:
                hien.gia_tri = gia_tri
                return
            huong = "trai" if khoa < hien.khoa else "phai"
            con = getattr(hien, huong)
            if con is None:
                setattr(hien, huong, nut)
                return
            hien = con

    def tim(self, khoa):
        hien = self.goc
        while hien:
            if khoa == hien.khoa:
                return hien.gia_tri
            hien = hien.trai if khoa < hien.khoa else hien.phai
        return None

    def duyet_trung_to(self):
        """Tra ve cac gia tri theo thu tu khoa tang dan."""
        ket_qua, stack, hien = [], [], self.goc
        while stack or hien:
            while hien:
                stack.append(hien)
                hien = hien.trai
            hien = stack.pop()
            ket_qua.append(hien.gia_tri)
            hien = hien.phai
        return ket_qua


class BangBam:
    """Bang bam xu ly dung do bang chaining: tim kiem trung binh O(1)."""

    def __init__(self, so_xo=1024):
        self.xo = [[] for _ in range(so_xo)]

    def _bam(self, khoa):
        h = 0
        for c in khoa:
            h = (h * 31 + ord(c)) % len(self.xo)
        return h

    def them(self, khoa, gia_tri):
        xo = self.xo[self._bam(khoa)]
        for i, (k, _) in enumerate(xo):
            if k == khoa:
                xo[i] = (khoa, gia_tri)
                return
        xo.append((khoa, gia_tri))

    def tim(self, khoa):
        for k, v in self.xo[self._bam(khoa)]:
            if k == khoa:
                return v
        return None


def tra_cuu_nhanh():
    ds = du_lieu["sinh_vien"]
    if not ds:
        print("Chua co sinh vien.")
        return
    cay, bang = CayNhiPhan(), BangBam(max(16, 2 * len(ds)))
    for sv in ds:
        cay.them(sv["ma_sv"], sv)
        bang.them(sv["ma_sv"], sv)
    ma = input("Nhap ma sinh vien can tra cuu: ").strip()
    print(f"  BST      : {cay.tim(ma) or 'Khong tim thay'}")
    print(f"  Bang bam : {bang.tim(ma) or 'Khong tim thay'}")
    print("Danh sach sap xep theo ma (duyet trung to BST):")
    for sv in cay.duyet_trung_to():
        print(f"  {sv['ma_sv']:<10}{sv['ten']}")


def so_sanh_toc_do(n=20000, so_lan=200):
    """Do thoi gian tim kiem: mang (tuyen tinh) vs BST vs bang bam tren n ban ghi gia lap."""
    khoa = [f"SV{i:06d}" for i in range(n)]
    random.shuffle(khoa)
    ds = [{"ma_sv": k} for k in khoa]
    cay, bang = CayNhiPhan(), BangBam(2 * n)
    for sv in ds:
        cay.them(sv["ma_sv"], sv)
        bang.them(sv["ma_sv"], sv)
    mau = random.sample(khoa, so_lan)

    def tuyen_tinh(k):
        for sv in ds:
            if sv["ma_sv"] == k:
                return sv

    print(f"Tim {so_lan} ma ngau nhien trong {n} sinh vien:")
    for ten, ham, do_phuc_tap in (("Mang (duyet tuyen tinh)", tuyen_tinh, "O(n)"),
                                  ("Cay nhi phan tim kiem", cay.tim, "O(log n)"),
                                  ("Bang bam", bang.tim, "O(1)")):
        t0 = time.perf_counter()
        for k in mau:
            ham(k)
        ms = (time.perf_counter() - t0) * 1000
        print(f"  {ten:<26}{ms:>9.2f} ms   {do_phuc_tap}")


def xep_lich_thi():
    """To mau do thi: moi mon la 1 dinh, 2 mon noi nhau neu co chung sinh vien. Cung mau = cung ca thi."""
    hoc_ky = input("Hoc ky can xep lich thi (vd 2026-1): ").strip()
    sv_theo_mon = {}
    for d in du_lieu["dang_ky"]:
        if d["hoc_ky"] == hoc_ky:
            sv_theo_mon.setdefault(d["ma_mon"], set()).add(d["ma_sv"])
    if not sv_theo_mon:
        print("Khong co du lieu dang ky trong hoc ky nay.")
        return
    mon = list(sv_theo_mon)
    ke = {m: set() for m in mon}
    for i, a in enumerate(mon):
        for b in mon[i + 1:]:
            if sv_theo_mon[a] & sv_theo_mon[b]:
                ke[a].add(b)
                ke[b].add(a)
    mau = {}
    for m in sorted(mon, key=lambda x: len(ke[x]), reverse=True):   # Welsh-Powell: bac cao truoc
        da_dung = {mau[k] for k in ke[m] if k in mau}
        c = 0
        while c in da_dung:
            c += 1
        mau[m] = c
    so_ca = max(mau.values()) + 1
    print(f"Hoc ky {hoc_ky}: {len(mon)} mon thi, can toi thieu {so_ca} ca thi de khong ai bi trung ca.")
    phong_max = 0
    for c in range(so_ca):
        mon_ca = sorted(m for m in mon if mau[m] == c)
        tong = sum(len(sv_theo_mon[m]) for m in mon_ca)
        phong = sum(math.ceil(len(sv_theo_mon[m]) / SUC_CHUA_PHONG) for m in mon_ca)
        phong_max = max(phong_max, phong)
        print(f"  Ca {c + 1}: {', '.join(mon_ca)} | {tong} luot thi | {phong} phong")
    print(f"So phong thi can chuan bi (dung lai giua cac ca): {phong_max}")
