import pandas as pd
from pd_lfs import read_parquet, write_parquet

df_list = []
for n in range(1, 23):
    chrom = f'chr{n}'
    file_name = f'./steps/atlas.chr{n}.csv'
    print(file_name)
    df = pd.read_csv(file_name, sep=r'\s*,\s*', skiprows=3, engine='python')
    print(df.columns)
    assert 0
    df['chrom'] = f'chr{n}'
    df['pos'] = df['Position']
    df.drop(columns=['Chromosome', 'Position'])
    df_list.append(df)
df = pd.concat(df_list)    

write_parquet(df, "results/atlas_variant_age.parquet", group="chrom", 
              compression='gzip' # better but slower compression than zstd
              )

# # HTTPS (after uploading the dir to a static host — GitHub Pages, S3 website, nginx, ...)
# df = read_parquet("https://github.com/munch-group/atlas-variant-age/")

