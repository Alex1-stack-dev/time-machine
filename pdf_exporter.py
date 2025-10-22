from reportlab.pdfgen import canvas

def export_results_to_pdf(results, filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 800, "Race Results")
    y = 780
    for idx, result in enumerate(results, 1):
        c.drawString(100, y, f"{idx}. {result.name}  {result.time}  Heat: {result.heat} {'DQ' if result.dq else ''}")
        y -= 20
    c.save()
