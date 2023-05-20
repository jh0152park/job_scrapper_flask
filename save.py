import csv

def create_csv(term, jobs):
    with open(f"{term}_search_result.csv", "w", encoding="utf-8-sig", newline="") as f:
        agenda = ["company", "title", "locate", "type", "link"]
        writer = csv.writer(f)
        writer.writerow(agenda)
        for job in jobs:
            writer.writerow([job[a] for a in agenda])

