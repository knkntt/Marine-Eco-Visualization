import pandas as pd
import numpy as np

def mask_marine_data(input_file, output_file):

    df = pd.read_csv(input_file)
    
    keep_columns = [
        'id', 
        'decimalLongitude', 
        'decimalLatitude', 
        'date_start', 
        'scientificName',
        'depth'
    ]
    
    clean_df = df[keep_columns].copy()
    
    
    clean_df['id'] = clean_df['id'].apply(lambda x: hash(str(x)) % 10**8)

    clean_df['date_start'] = pd.to_datetime(clean_df['date_start'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')
  
    clean_df.to_csv(output_file, index=False)
    print(f"脱敏完成！处理后的字段数量从 {len(df.columns)} 减少到 {len(clean_df.columns)}")
    print(f"数据已保存至: {output_file}")

mask_marine_data('001.part', 'github_demo_data.csv')