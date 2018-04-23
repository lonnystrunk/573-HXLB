#!/bin/sh
if [ ! -d "py36" ]
then
    virtualenv py36 -p /opt/python-3.6/bin/python3
fi

if [ ! -L "AQUAINT" ] || [ ! -L "AQUIANT-2" ]
then
    ln -sf /corpora/LDC/LDC02T31/ AQUAINT
    ln -sf /corpora/LDC/LDC08T25/ AQUAINT-2
fi

. py36/bin/activate
pip install -r src/requirements.txt
python src/d2system.py $@
python /dropbox/17-18/573/code/ROUGE/run_rouge.py src/rouge_run_ex.xml > results/D2_rouge_scores.out
deactivate
