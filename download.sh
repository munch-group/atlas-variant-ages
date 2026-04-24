#!/usr/bin/env bash

mkdir -p ./steps

for N in {1..22}; do
    echo "Chromosome $N"
    curl https://human.genome.dating/bulk/atlas.chr${N}.csv.gz | gzip -d > ./steps/atlas.chr${N}.csv
done

