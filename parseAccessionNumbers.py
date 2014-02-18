def parseFile(fileLocation):
    fileHandle = open(fileLocation)
    lines = fileHandle.readlines()
    barcodes = []
    for line in lines:
        line = line.strip()
        barcodes.append(line)

    return barcodes
