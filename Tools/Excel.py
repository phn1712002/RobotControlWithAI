import openpyxl, os

def writeExcel(path, data):
    if os.path.exists(path):
        try:
            # Mở tệp Excel
            workbook = openpyxl.load_workbook(path)
            # Chọn một trang bất kỳ trong tệp
            sheet = workbook.active

            # Đặt dữ liệu mới vào tệp Excel
            sheet.append(data)

            # Lưu tệp
            workbook.save(path)
            return "Dữ liệu đã được thêm vào tệp Excel thành công."
        except Exception as e:
            return f"Lỗi: {str(e)}"