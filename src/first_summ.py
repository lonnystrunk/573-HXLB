import sys
import os
import re

from d4 import d4 as summarize


if __name__ == '__main__':
    xml_files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if re.match(r'.+\.xml', f)]
    conductor = summarize.Conductor(xml_files)
    weights = [0.75, 0.8, 0.85, 0.90, 0.95, 0.99, 0.999, 1.001, 1.01, 1.05, 1.1, 1.15, 1.2, 1.25]
    f = open("outputs/D4/first_percent", 'w')
    for weight in weights:
        c = 0
        t = 0
        for summ in conductor.summarizers:
            count, total = summ.test_firsts(conductor.lexrank_obj, weight)
            c+=count
            t+=total
        f.write("{}/{} of selected sentences for weight {} are firsts.\n".format(c,t,weights))
    f.close()