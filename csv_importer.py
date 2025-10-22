import csv
from core.data_models import Entry

def import_entries_from_csv(filename):
    entries = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = Entry(
                entry_id=row.get('ID', ''),
                name=row.get('Name', ''),
                heat=row.get('Heat', ''),
                lane=row.get('Lane', ''),
                status=row.get('Status', 'OK')
            )
            entries.append(entry)
    return entries

def export_entries_to_csv(entries, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["ID", "Name", "Heat", "Lane", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.as_dict())
