import json
from openpyxl import Workbook

# Load forms
with open("data/forms.json", "r", encoding="utf-8") as f:
    forms = json.load(f)

wb = Workbook()
ws = wb.active
ws.title = "Form Status"

ws.append([
    "Page URL",
    "Form ID",
    "Form Name",
    "Action",
    "Method",
    "Input Fields",
    "Submit Button",
    "Status",
    "Remarks"
])

for form in forms:

    action = form.get("action", "")
    method = form.get("method", "")
    fields = form.get("fields", [])

    input_count = 0
    submit_button = False
    remarks = []

    for field in fields:

        if field["tag"] in ["input", "textarea", "select"]:
            input_count += 1

        if field["tag"] == "button":
            if field.get("type") == "submit":
                submit_button = True

        if field["tag"] == "input":
            if field.get("type") == "submit":
                submit_button = True

    if not action:
        remarks.append("Missing action")

    if not method:
        remarks.append("Missing method")

    if input_count == 0:
        remarks.append("No input fields")

    if not submit_button:
        remarks.append("No submit button")

    if len(remarks) == 0:
        status = "Working"
        remarks_text = "Looks OK"
    else:
        status = "Needs Review"
        remarks_text = ", ".join(remarks)

    ws.append([
        form.get("page_url"),
        form.get("id"),
        form.get("name"),
        action,
        method,
        input_count,
        "Yes" if submit_button else "No",
        status,
        remarks_text
    ])

wb.save("data/form_status.xlsx")

print("Saved report to data/form_status.xlsx")