import openpyxl, os

def writeExcel(path, data):
    # Check path have file exist
    if os.path.exists(path):
        try:
            # Open Excel
            workbook = openpyxl.load_workbook(path)
            # Select sheet any
            sheet = workbook.active

            # Write data in sheet
            sheet.append(data)

            # Save file
            workbook.save(path)
            return "Save data in file success"
        except Exception as e:
            return f"Error: {str(e)}"