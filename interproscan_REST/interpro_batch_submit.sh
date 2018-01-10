#!/bin/bash
i=1
waitevery=30

mkdir -p out

for j in $(find `pwd` -type f -name "*.fa")
do
    echo "Iteration: $i; File: $j"
    filename=$(basename "$j")
    python3 iprscan5_urllib3.py \
        --goterms \
        --pathways \
        --email=<INSERT_EMAIL_HERE> \
        --outfile=out/${filename} \
        --outformat=xml \
        $j & (( i++%waitevery==0 )) && wait
done
