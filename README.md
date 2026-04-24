
Download the publicly available csv files from https://human.genome.dating/download/index and build parquet data set with only the main columns (renamed to shorter lower case names):

    ./download.sh && srun --mem-per-cpu=36g --time=03:00:00 --account=xy-drive --pty pixi run python build_parquet.py

 