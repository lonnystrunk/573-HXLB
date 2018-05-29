#!/bin/sh
if [ ! -d "py36" ]
then
    virtualenv py36 -p /opt/python-3.6/bin/python3
fi

if [ ! -L "AQUAINT" ] || [ ! -L "AQUIANT-2" ]
then
    ln -sf /corpora/LDC/LDC02T31/ AQUAINT
    ln -sf /corpora/LDC/LDC11T07/ AQUAINT-2
fi

. py36/bin/activate
pip install -r src/requirements.txt

python src/summarize.py /dropbox/17-18/573/Data/Documents/devtest/ D4_devtest &
python src/summarize.py /dropbox/17-18/573/Data/Documents/evaltest/ D4_evaltest &
wait

python /dropbox/17-18/573/code/ROUGE/run_rouge.py src/rouge_dev.xml > results/D4_devtest_rouge_scores.out &
python /dropbox/17-18/573/code/ROUGE/run_rouge.py src/rouge_eval.xml > results/D4_evaltest_rouge_scores.out &
wait

deactivate
