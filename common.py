
def writeToFile(filename, content):
    with open(filename, "w", encoding="utf-8") as fo:
        fo.write(content)
