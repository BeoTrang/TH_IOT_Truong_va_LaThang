import subprocess


def write_to_plc_via_usb(gxw_path, com_port):
    """
    Tự động nạp chương trình vào PLC Mitsubishi FX3U qua cáp nạp (USB hoặc RS232).
    :param gxw_path: Đường dẫn đầy đủ đến file chương trình (.gxw)
    :param com_port: Cổng COM của cáp nạp (ví dụ: COM3)
    """
    # Đường dẫn đến GX Works2 hoặc GX Developer (cần điều chỉnh theo cài đặt của bạn)
    gx_works2_exe = r"D:\th plc tren truong\GPPW2\GD2.exe"

    # Lệnh dòng để nạp chương trình
    command = [
        gx_works2_exe,  # Đường dẫn tới GX Works2 hoặc GX Developer
        "/write",  # Tham số nạp chương trình
        f"/path:{gxw_path}",  # Đường dẫn file chương trình
        f"/com:{com_port}"  # Cổng COM của cáp nạp
    ]

    try:
        # Thực thi lệnh và chờ hoàn tất
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ Nạp chương trình thành công!")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ Không tìm thấy ứng dụng GX Works2 hoặc GX Developer.")
        print("Vui lòng kiểm tra đường dẫn tới phần mềm và chỉnh sửa trong script.")
    except subprocess.CalledProcessError as e:
        print("❌ Lỗi khi nạp chương trình:")
        if "COM" in e.stderr:
            print(f"Không thể kết nối với PLC qua cổng {com_port}. Kiểm tra cáp nạp và cổng COM.")
        elif "file" in e.stderr.lower():
            print(f"File chương trình {gxw_path} không hợp lệ hoặc không tồn tại.")
        else:
            print(e.stderr)
    except Exception as e:
        print(f"❌ Có lỗi không xác định xảy ra: {e}")


# Ví dụ sử dụng
if __name__ == "__main__":
    # Đường dẫn file chương trình .gxw
    gxw_file_path = r"D:\PLC\MISTU\testnap.gxw"

    # Cổng COM của cáp nạp (kiểm tra trong Device Manager)
    com_port = "COM3"

    # Kiểm tra điều kiện cơ bản trước khi thực hiện
    if not gxw_file_path.endswith(".gxw"):
        print("❌ Lỗi: Đường dẫn file không đúng định dạng (.gxw). Vui lòng kiểm tra!")
    elif not com_port.startswith("COM"):
        print("❌ Lỗi: Cổng COM không hợp lệ. Vui lòng kiểm tra!")
    else:
        # Gọi hàm nạp chương trình
        write_to_plc_via_usb(gxw_path=gxw_file_path, com_port=com_port)
