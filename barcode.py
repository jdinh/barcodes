import sys
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from parseAccessionNumbers import parseFile


def main():
    if len(sys.argv) <= 1:
        print "No filepath argument passed."
        return

    c = canvas.Canvas("barcode_example.pdf", pagesize=letter)

    accessionNumberList = parseFile(sys.argv[1])

    # Page specs
    totalHeight = 265 * mm
    xColumnMargin = 70 * mm
    yBarcodeMargin = 20 * mm

    # Specs for lower right status info
    xPageStatus = 165 * mm
    yPageStatus = 17 * mm
    yBarcodeStatus = 12 * mm

    # Initial values
    x = 1 * mm
    y = totalHeight
    x1 = 6.4 * mm

    # Initialize barcode counts and page counts
    currentBarcodeTotalCount = 0
    currentPageCount = 0
    currentPage = 1
    totalPages = int(len(accessionNumberList) / 32)
    if len(accessionNumberList) % 32 > 0:
        totalPages += 1

    for accessionNumber in accessionNumberList:
        if currentBarcodeTotalCount % 32 == 0 and currentBarcodeTotalCount != 0:
            c.drawString(xPageStatus, yPageStatus, "Page " + str(currentPage) + " of " + str(totalPages))
            c.drawString(xPageStatus, yBarcodeStatus, str(currentPageCount) + " barcodes")
            c.showPage()

            # Reset values for a new page
            x = 1 * mm
            y = totalHeight
            x1 = 6.4 * mm
            currentPageCount = 0

            # Increase to next page
            currentPage += 1

        currentBarcodeTotalCount += 1
        currentPageCount += 1

        barcode = code39.Extended39(accessionNumber)

        # Draw the barcode on the canvas
        barcode.drawOn(c, x, y)
        x1 = x + 6.4 * mm
        y -= 5 * mm

        # Draw the actual string
        c.drawString(x1, y, accessionNumber)
        x = x
        y -= yBarcodeMargin

        if int(y) < 20:
            x += xColumnMargin
            y = totalHeight

    c.drawString(xPageStatus, yPageStatus, "Page " + str(currentPage) + " of " + str(totalPages))
    c.drawString(xPageStatus, yBarcodeStatus, str(currentPageCount) + " barcodes")
    c.showPage()
    c.save()
    print "File successfully created"

main()


