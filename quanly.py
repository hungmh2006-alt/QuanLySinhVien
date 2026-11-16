"""Module xử lý nghiệp vụ quản lý sinh viên."""

danh_sach = []  # Mỗi sinh viên: {"ma": str, "ten": str, "diem": float}


def _nhap_diem(thong_bao="Nhập điểm trung bình (0-10): "):
    while True:
        try:
            diem = float(input(thong_bao))
            if 0 <= diem <= 10:
                return diem
            print("Điểm phải nằm trong khoảng 0 - 10.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")


def _tim_theo_ma(ma):
    for sv in danh_sach:
        if sv["ma"] == ma:
            return sv
    return None


def _in_sinh_vien(sv):
    print(f"Mã: {sv['ma']:<10} | Tên: {sv['ten']:<25} | Điểm TB: {sv['diem']:.2f}")


def them_sinh_vien():
    """Thêm sinh viên vào danh sách."""
    ma = input("Nhập mã sinh viên: ").strip()
    if not ma:
        print("Mã không được để trống.")
        return
    if _tim_theo_ma(ma):
        print("Mã sinh viên đã tồn tại.")
        return
    ten = input("Nhập tên sinh viên: ").strip()
    diem = _nhap_diem()
    danh_sach.append({"ma": ma, "ten": ten, "diem": diem})
    print("Đã thêm sinh viên.")


def hien_thi_sinh_vien():
    """Hiển thị toàn bộ sinh viên."""
    if not danh_sach:
        print("Danh sách trống.")
        return
    for sv in danh_sach:
        _in_sinh_vien(sv)


def tim_sinh_vien():
    """Tìm sinh viên theo mã."""
    ma = input("Nhập mã sinh viên cần tìm: ").strip()
    sv = _tim_theo_ma(ma)
    if sv:
        _in_sinh_vien(sv)
    else:
        print("Sinh viên không tồn tại.")


def xoa_sinh_vien():
    """Xóa sinh viên theo mã."""
    ma = input("Nhập mã sinh viên cần xóa: ").strip()
    sv = _tim_theo_ma(ma)
    if sv:
        danh_sach.remove(sv)
        print("Đã xóa sinh viên.")
    else:
        print("Sinh viên không tồn tại.")


def sua_sinh_vien():
    """Sửa thông tin sinh viên (Enter để giữ nguyên tên)."""
    ma = input("Nhập mã sinh viên cần sửa: ").strip()
    sv = _tim_theo_ma(ma)
    if not sv:
        print("Sinh viên không tồn tại.")
        return
    ten_moi = input(f"Tên mới (hiện tại: {sv['ten']}, Enter để giữ nguyên): ").strip()
    if ten_moi:
        sv["ten"] = ten_moi
    sv["diem"] = _nhap_diem("Điểm trung bình mới (0-10): ")
    print("Đã cập nhật thông tin.")


def sap_xep_sinh_vien():
    """Sắp xếp giảm dần theo điểm trung bình."""
    if not danh_sach:
        print("Danh sách trống.")
        return
    danh_sach.sort(key=lambda sv: sv["diem"], reverse=True)
    print("Đã sắp xếp theo điểm trung bình (giảm dần):")
    hien_thi_sinh_vien()


def thong_ke_sinh_vien():
    """Thống kê số lượng sinh viên."""
    print(f"Tổng số sinh viên: {len(danh_sach)}")


def tim_diem_cao_nhat():
    """Tìm sinh viên có điểm cao nhất."""
    if not danh_sach:
        print("Danh sách trống.")
        return
    cao_nhat = max(sv["diem"] for sv in danh_sach)
    print(f"Sinh viên có điểm cao nhất ({cao_nhat:.2f}):")
    for sv in danh_sach:
        if sv["diem"] == cao_nhat:
            _in_sinh_vien(sv)


def tim_diem_thap_nhat():
    """Tìm sinh viên có điểm thấp nhất."""
    if not danh_sach:
        print("Danh sách trống.")
        return
    thap_nhat = min(sv["diem"] for sv in danh_sach)
    print(f"Sinh viên có điểm thấp nhất ({thap_nhat:.2f}):")
    for sv in danh_sach:
        if sv["diem"] == thap_nhat:
            _in_sinh_vien(sv)
