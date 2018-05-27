import sys
import os
import re

from d4 import d4 as summarize


if __name__ == '__main__':
    # TODO: iterate over all xml files
    test_files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if re.match(r'.+\.xml', f)]
    if len(sys.argv > 2):
        training_files = [os.path.join(sys.argv[i], f) for i in range(2,len(sys.argv)) for f in os.listdir(sys.argv[i]) if re.match(r'.+\.xml', f)]
    else:
        training_files = None

    conductor = summarize.Conductor(test_files, training_files)
    #print(len(conductor.summarizers))
    for summ in conductor.summarizers:
        #summ.easy_summarize(conductor.lexrank_obj)
        summ.ordered_summarize(conductor.lexrank_obj)
