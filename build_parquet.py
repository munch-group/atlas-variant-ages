import sys
import pandas as pd
from pd_lfs import read_parquet, write_parquet

df_list = []
for n in range(1, 23):
    print(f"Chromosome {n}", file=sys.stderr)
    chrom = f'chr{n}'
    file_name = f'./steps/atlas.chr{n}.csv'
    df = pd.read_csv(file_name, sep=r'\s*,\s*', skiprows=3, engine='python')
    df['chrom'] = f'chr{n}'
    df['pos'] = df['Position']
    df.drop(columns=['Chromosome', 'Position'])
    df_list.append(df)
df = pd.concat(df_list)    

column_subset = ['VariantID', 'Chromosome', 'Position', 'AlleleRef', 'AlleleAlt', 'AlleleAnc', 'AgeMode_Mut', 'AgeMean_Mut', 'AgeMedian_Mut', 'AgeCI95Lower_Mut', 'AgeCI95Upper_Mut']

write_parquet(df[column_subset], "results/atlas_variant_age.parquet", group="chrom", 
              compression='gzip' # better but slower compression than zstd
              )
