from openpyxl import Workbook

wb = Workbook()
ws = wb.active
results = []

ws.append([
    "URL",
    "Status Code",
    "Working",
    "Response Time",
    "Remark"
])

for row in results:
    ws.append(row)

wb.save("data/link_status.xlsx")