import sys
import pandas as pd
import gc
import logging
from pathlib import Path
from pd_lfs import write_parquet

logging.basicConfig(
    level=logging.DEBUG,
    # format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(Path(__file__).with_suffix('.log'))],
)
logger = logging.getLogger(Path(__file__).stem)
logger.setLevel(logging.DEBUG)

df_list = []
for n in range(1, 23):
    logger.info(f"Reading chrom {n}")
    chrom = f'chr{n}'
    file_name = f'./steps/atlas.chr{n}.csv'
    df = pd.read_csv(file_name, sep=r'\s*,\s*', skiprows=3, engine='python')
    df['chrom'] = f'chr{n}'
    df['pos'] = df['Position']
    df.drop(columns=['Chromosome', 'Position'])
    df_list.append(df)

logger.info(f"Concatenating data frames")

column_subset = ['VariantID', 'Chromosome', 'Position', 'AlleleRef', 'AlleleAlt', 'AlleleAnc', 'AgeMode_Mut', 'AgeMean_Mut', 'AgeMedian_Mut', 'AgeCI95Lower_Mut', 'AgeCI95Upper_Mut']
df = pd.concat(df_list)[column_subset].rename(columns={
    'VariantID': 'variant_id', 'Chromosome': 'chrom', 'Position': 'pos', 
    'AlleleRef': 'ref', 'AlleleAlt': 'alt', 'AlleleAnc': 'anc', 
    'AgeMode_Mut': 'age_mode', 'AgeMean_Mut': 'age_mean', 'AgeMedian_Mut': 'age_median', 
    'AgeCI95Lower_Mut': 'age_lo95ci', 'AgeCI95Upper_Mut': 'age_hi95ci'
})

logger.info(f"Garbage collecting")

del df_list
gc.collect()

logger.info(f"Writing parquet")

write_parquet(df, "results/atlas_variant_age.parquet", group="chrom", 
              compression='gzip' # better but slower compression than zstd
              )
