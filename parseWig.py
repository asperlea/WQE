__author__ = 'adriana'
import gzip

def main():
    if len(sys.argv) < 2:
        print "Usage: python parseWig.py <file1>"
        exit(1)
    wigFile = sys.argv[1]
    f = gzip.open(wigFile, 'rb')
    file_content = f.read()
    for line in file_content:
        print line
    f.close()

main()