def export_results_to_hy3(results, filename):
    """
    Export results to the Hy-Tek .hy3 format (simplified example).
    """
    with open(filename, 'w') as f:
        f.write("HY3 HEADER DATA\n")
        for r in results:
            # Replace with actual HY3 format according to Hy-Tek docs
            f.write(f"{r.place},{r.name},{r.time},{r.heat},{r.dq}\n")
