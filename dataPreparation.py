# %%
import pandas as pd

# %% [markdown]
# Create DataFrame from raw csv:

# %%
dataFile = r"data/ZBAA.26.09.2012.30.11.2022.1.0.0.cn.utf8.00000000.csv"
df = pd.read_csv(dataFile, sep=';')
df

# %% [markdown]
# Drop redundant columns in DataFrame:

# %%
df.drop(['stat_pres', 'max_gust_spd', 'special', 'important', 'vis', 'Unnamed: 13'], axis=1, inplace=True)
df
# df.drop(['stat_pres', 'max_gust_spd', 'special', 'important', 'Unnamed: 13'], axis=1)

# %%
import re

# s = r"27.09.2012 \d\d:\d\d"

# df_27092012 = df[df['date_time'].str.contains(s, regex=True)]
# df_27092012

# %%
# print(df_27092012['temp'].mean())
# print(df_27092012['temp'].max())
# print(df_27092012['wd_dir'].mode()[0])
# print(df['wd_dir'].unique())
# print(df['cld_cnt'].unique())
# df_27092012

# %% [markdown]
# Encode wind direction data, convert from string categorical data to integar continuous data. Wind directions such as *northeast-north* (东北偏北) was encoded in their direction components, e.g. *northeast-north* was encoded in *northeast* and *north*:

# %%
def encodeWind(windDirection):
    if windDirection == '风向多变':
        return {'N_wd':1, 'NW_wd':1, 'W_wd':1, 'SW_wd':1,
                'S_wd':1, 'SE_wd':1, 'E_wd':1, 'NE_wd':1}
    elif windDirection == '无风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从北方吹来的风':
        return {'N_wd':1, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西北偏北方向吹来的风':
        return {'N_wd':1, 'NW_wd':1, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西北方吹来的风':
        return {'N_wd':0, 'NW_wd':1, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西北偏西方向吹来的风':
        return {'N_wd':0, 'NW_wd':1, 'W_wd':1, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':1, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西南偏西方向吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':1, 'SW_wd':1,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西南方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':1,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从西南偏南方向吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':1,
                'S_wd':1, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从南方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':1, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从东南偏南方向吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':1, 'SE_wd':1, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从东南方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':1, 'E_wd':0, 'NE_wd':0}
    elif windDirection == '从东南偏东方向吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':1, 'E_wd':1, 'NE_wd':0}
    elif windDirection == '从东方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':1, 'NE_wd':0}
    elif windDirection == '从东北偏东方向吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':1, 'NE_wd':1}
    elif windDirection == '从东北方吹来的风':
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':1}
    elif windDirection == '从东北偏北方向吹来的风':
        return {'N_wd':1, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':1}
    else:
        return {'N_wd':0, 'NW_wd':0, 'W_wd':0, 'SW_wd':0,
                'S_wd':0, 'SE_wd':0, 'E_wd':0, 'NE_wd':0}

# %% [markdown]
# Encode cloud coverage data, convert from string categorical data to integar continuous data. '*垂直能见度...*' are treated as cloudy as it is believed that when vertical visibilities are low, cloud must be very heavy and low; '*垂直发展很旺盛的浓积云*' is treated as '*积雨云*' as it is most likily to develop into one.

# %%
def encodeCldCovery(cloud:str):
    nocld = r'无明显的云'
    little = r'疏云.'
    some = r'少云.'
    much = r'多云'
    cloudy = r'阴天.'
    rain = r'积雨云'
    vert = r'垂直能见度.'
    nj = r'垂直发展.'
    result = {'nocld':0, 'little':0, 'some':0, 'much':0, 'cloudy':0, 'rain':0}
    if re.search(nocld, cloud): result['nocld'] = 1
    if re.search(little, cloud): result['little'] = 1
    if re.search(some, cloud): result['some'] = 1
    if re.search(much, cloud): result['much'] = 1
    if re.search(cloudy, cloud) or re.search(vert, cloud): result['cloudy'] = 1
    if re.search(rain, cloud) or re.search(nj, cloud): result['rain'] = 1
    return result

# %% [markdown]
# Compute each and every useful data's maximum, minimum, mean for the given date, and execute the above encoding for wind direction and cloud coverage.

# %%
def dayAverage(df, date):
    s = "{} \d\d:\d\d".format(date)
    df_date = df[df['date_time'].str.contains(s, regex=True)]
    result = {
        'date': date,
        'mintemp': df_date['temp'].min(),
        'maxtemp': df_date['temp'].max(),
        'meantemp': df_date['temp'].mean(),
        'minpres': df_date['sea_pres'].min(),
        'maxpres': df_date['sea_pres'].max(),
        'meanpres': df_date['sea_pres'].mean(),
        'maxhumi': df_date['humi'].max(),
        'minhumi': df_date['humi'].min(),
        'meanhumi': df_date['humi'].mean(),
        'meanwdspd': df_date['ave_wd_spd'].mean(),
        'maxdewpt': df_date['dewpt_temp'].max(),
        'mindewpt': df_date['dewpt_temp'].min(),
        'meandewpt': df_date['dewpt_temp'].mean()
    }
    result.update(encodeWind(df_date['wd_dir'].mode()[0]))
    result.update(encodeCldCovery(df_date['cld_cnt'].mode()[0]))
    return result

# %% [markdown]
# Execute day average for every day in the dataset, from 2012.9.27 to 2022.11.30, and create a new DataFrame to store the averages.

# %%
import warnings
from tqdm import tqdm

clean_df = pd.DataFrame()

days = 3717

with tqdm(total = days) as pbar:
    for year in range(2012, 2023):
        for month in range(1, 13):
            if ((year == 2012) and (month < 9)) or ((year == 2022) and (month == 12)):
                continue
            max_days = 31
            if month in [4,6,9,11]:
                max_days = 30
            elif month == 2 and year in [2016, 2020]:
                max_days = 29
            elif month == 2:
                max_days = 28
            for day in range(1, max_days+1):
                if (year == 2012) and (month == 9) and (day < 27):
                    continue
                date = "{}.{:0>2d}.{}".format(day, month, year)
                with warnings.catch_warnings():
                    warnings.simplefilter(action='ignore', category=FutureWarning)
                    clean_df = clean_df.append(dayAverage(df, date), ignore_index=True)
                pbar.update(1)

# %% [markdown]
# The data are now clean and ready for building and testing a machine learning model.

# %%
clean_df

# %% [markdown]
# Store the clean data as a csv file for future use(building and testing model).

# %%
cleanFile = r'data/clean_data.csv'

clean_df.to_csv(cleanFile, index=False)


