import sys
import os
import re

from d4 import d4 as summarize

# GLOBAL VARIABLES
ORDERING_METHOD = 2 # 1 - Easy; 2 - Greedy; 3 - Chronological


if __name__ == '__main__':
    # TODO: iterate over all xml files
    xml_files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if re.match(r'.+\.xml', f)]
    conductor = summarize.Conductor(xml_files)
    #print(len(conductor.summarizers))
    for summ in conductor.summarizers:
        if ORDERING_METHOD == 1:
            summ.easy_summarize(conductor.lexrank_obj)
        elif ORDERING_METHOD == 2:
            summ.ordered_summarize(conductor.lexrank_obj)
        elif ORDERING_METHOD == 3:
            summ.chrono_summarize(conductor.lexrank_obj)
