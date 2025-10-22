import csv

def export_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["Place", "Name", "Time", "Heat", "DQ"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result.as_dict())
