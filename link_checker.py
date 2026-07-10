import csv
import requests
import time

input_file = "data/urls.csv"
output_file = "data/link_status.csv"

results = []

with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        if not row:
            continue

        url = row[0]

        try:
            start = time.time()

            response = requests.get(
                url,
                timeout=10,
                allow_redirects=True
            )

            elapsed = round(time.time() - start, 2)

            status = response.status_code

            working = "Yes" if status < 400 else "No"

            if status == 200:
                remark = "OK"
            elif status == 404:
                remark = "Page Not Found"
            elif status == 403:
                remark = "Forbidden"
            elif status == 500:
                remark = "Server Error"
            else:
                remark = response.reason

        except requests.exceptions.Timeout:
            status = "Timeout"
            elapsed = "-"
            working = "No"
            remark = "Timed Out"

        except Exception as e:
            status = "Error"
            elapsed = "-"
            working = "No"
            remark = str(e)

        results.append([
            url,
            status,
            working,
            elapsed,
            remark
        ])

        print(f"{url} -> {working}")

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "URL",
        "Status Code",
        "Working",
        "Response Time (s)",
        "Remark"
    ])

    writer.writerows(results)

print(f"\nSaved report to {output_file}")