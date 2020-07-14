import sys
import re

oneline_comment = re.compile(r'//.*', re.MULTILINE|re.DOTALL)
oneline_comment = re.compile(r'//[^\n]*\n|/\*(.*?)\*/', re.MULTILINE|re.DOTALL)

def main(fn):
    with open(fn, 'r') as f:
        for line in f.readlines:
            l = line.strip()


if __name__ == '__main__':
    fn = sys.argv[1]
    main(fn)
