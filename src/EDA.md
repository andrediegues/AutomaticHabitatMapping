

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

path = '/home/diegues/Desktop/ProcessedImages/'
labeled_data = pd.read_csv(path + 'labeled_data.csv')
```


```python
folders = []
for folder in [f for f in os.listdir(path) if os.path.isdir(path + f)]:
    if folder[0] in '0123456789':
        folders.append(folder)
folders.sort()
print(folders)        
```

    ['104728_cam-np3', '105317_cam-np3', '113610_cam_survey_1', '125355_forcadinho-np3', '132143_forcadinho-np3']



```python
df0 = pd.DataFrame()
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
df4 = pd.DataFrame()

i = 0

for f in folders:
    datafile = path + f + "/" + f + ".csv"
    if not os.path.exists(datafile):
        print(datafile + "doesn't exist!")
        break
    data = pd.read_csv(datafile, 
                       names=['filename', 'timestamp', 'latitude', 'longitude', 'altitude', 'roll', 'pitch', 'depth', 'entropy', 'date'])[1:]
    data = data.drop(['altitude', 'depth'], axis = 1)
    targetsfile = path + f + "/" + f + "-targets.csv"
    if not os.path.exists(targetsfile):
        print(targetsfile + "doesn't exist!")
        continue
    targets = pd.read_csv(targetsfile,
                          names=['filename', 'date', 'longitude', 'latitude', 'depth', 'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 
                                 'species', 'AphiaID'])[1:]
    targets = targets.drop(['date', 'longitude', 'latitude'], axis=1)
    join_dfs = pd.merge(data, targets, on='filename', how='outer')
    non_empty_targets = join_dfs[join_dfs['EunisCode'].notnull()]
    if i == 0:
        df0 = non_empty_targets
        filenames = df0['filename']
        targets = df0['level3']
        species = pd.get_dummies(df0['species'])
        df0 = df0.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4',
          'level5', 'level6', 'AphiaID', 'EunisName', 'EunisCode', 
          'date', 'timestamp', 'species'], axis = 1)
        df0 = pd.concat([df0, species, targets], axis = 1).groupby('filename').max()
        i += 1
    elif i == 1:
        df1 = non_empty_targets
        filenames = df1['filename']
        targets = df1['level3']
        species = pd.get_dummies(df1['species'])
        df1 = df1.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4',
          'level5', 'level6', 'AphiaID', 'EunisName', 'EunisCode', 
          'date', 'timestamp', 'species'], axis = 1)
        df1 = pd.concat([df1, species, targets], axis = 1).groupby('filename').max()
        i += 1
    elif i == 2:
        df2 = non_empty_targets
        filenames = df2['filename']
        targets = df2['level3']
        species = pd.get_dummies(df2['species'])
        df2 = df2.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4',
          'level5', 'level6', 'AphiaID', 'EunisName', 'EunisCode', 
          'date', 'timestamp', 'species'], axis = 1)
        df2 = pd.concat([df2, species, targets], axis = 1).groupby('filename').max()
        i += 1
    elif i == 3:
        df3 = non_empty_targets
        filenames = df3['filename']
        targets = df3['level3']
        species = pd.get_dummies(df3['species'])
        df3 = df3.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4',
          'level5', 'level6', 'AphiaID', 'EunisName', 'EunisCode', 
          'date', 'timestamp', 'species'], axis = 1)
        df3 = pd.concat([df3, species, targets], axis = 1).groupby('filename').max()
        i += 1
    elif i == 4:
        df4 = non_empty_targets
        filenames = df4['filename']
        targets = df4['level3']
        species = pd.get_dummies(df4['species'])
        df4 = df4.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4',
          'level5', 'level6', 'AphiaID', 'EunisName', 'EunisCode', 
          'date', 'timestamp', 'species'], axis = 1)
        df4 = pd.concat([df4, species, targets], axis = 1).groupby('filename').max()
        i += 1
```


```python
df0.level3.value_counts()
```




    A4.1    22
    Name: level3, dtype: int64




```python
plt.figure(1)

plt.subplot(221)
plt.plot(df1.level3.value_counts())
plt.plot([np.mean(df1.level3.value_counts())]*len(df1.level3.value_counts()), color='red', linestyle = '--')
plt.plot([np.median(df1.level3.value_counts())]*len(df1.level3.value_counts()), color='green')

plt.subplot(222)
plt.plot(df2.level3.value_counts())
plt.plot([np.mean(df2.level3.value_counts())]*len(df2.level3.value_counts()), color='red', linestyle = '--')
plt.plot([np.median(df2.level3.value_counts())]*len(df2.level3.value_counts()), color='green')

plt.subplot(223)
plt.plot(df3.level3.value_counts())
plt.plot([np.mean(df3.level3.value_counts())]*len(df3.level3.value_counts()), color='red', linestyle = '--')
plt.plot([np.median(df3.level3.value_counts())]*len(df3.level3.value_counts()), color='green')

plt.subplot(224)
plt.plot(df4.level3.value_counts())
plt.plot([np.mean(df4.level3.value_counts())]*len(df4.level3.value_counts()), color='red', linestyle = '--')
plt.plot([np.median(df4.level3.value_counts())]*len(df4.level3.value_counts()), color='green')

plt.savefig('classes_per_log.jpg')

fig,ax = plt.subplots()
x = labeled_data.level3.value_counts()
y_mean = [np.mean(x)]*len(x)
y_median = [np.median(x)]*len(x)
print(np.mean(x), np.median(x))
ax.plot(x)
ax.plot(y_mean, color='red', linestyle = '--')
ax.plot(y_median, color='green')

plt.savefig('aggregated_data.jpg')
```

    309.85714285714283 178.0



![png](../figures/classes_per_log.jpg)



![png](../figures/aggregated_data.jpg)



```python
df_a41 = labeled_data[labeled_data['level3'] == 'A4.1']
df_a31 = labeled_data[labeled_data['level3'] == 'A3.1']
df_a51 = labeled_data[labeled_data['level3'] == 'A5.1']
df_a47 = labeled_data[labeled_data['level3'] == 'A4.7']
df_a37 = labeled_data[labeled_data['level3'] == 'A3.7']
df_a52 = labeled_data[labeled_data['level3'] == 'A5.2']
df_a54 = labeled_data[labeled_data['level3'] == 'A5.4']

```


```python
median = int(np.median(labeled_data.level3.value_counts()))
print('A4.1:',len(df_a41),'\nA3.1:',len(df_a31),'\nA5.1:',len(df_a51),'\nA4.7:',len(df_a47),'\nA3.7:',len(df_a37),
      '\nA5.2:',len(df_a52),'\nA5.4:', len(df_a54), '\nMedian:',median)

```

    A4.1: 1207 
    A3.1: 388 
    A5.1: 181 
    A4.7: 178 
    A3.7: 96 
    A5.2: 85 
    A5.4: 34 
    Median: 178



```python
sampled_a41 = df_a41.sample(median)
sampled_a31 = df_a31.sample(median)
sampled_a51 = df_a51.sample(median)
sampled_a47 = df_a47.sample(median)
sampled_a37 = df_a37
sampled_a52 = df_a52
sampled_a54 = df_a54
```


```python
sampled_df = pd.concat([sampled_a31,sampled_a37,sampled_a41,sampled_a47,sampled_a51,sampled_a52, sampled_a54])
```


```python
sampled_df[:5]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>filename</th>
      <th>timestamp</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>roll</th>
      <th>pitch</th>
      <th>entropy</th>
      <th>date</th>
      <th>depth</th>
      <th>EunisCode</th>
      <th>EunisName</th>
      <th>level1</th>
      <th>level2</th>
      <th>level3</th>
      <th>level4</th>
      <th>level5</th>
      <th>level6</th>
      <th>species</th>
      <th>AphiaID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2082</th>
      <td>113610_cam_survey_1_frame2013.jpg</td>
      <td>1.525176e+09</td>
      <td>41.53330</td>
      <td>-8.80762</td>
      <td>-1.62</td>
      <td>-19.97</td>
      <td>21.909578</td>
      <td>01/05/18</td>
      <td>9.45</td>
      <td>A3.11</td>
      <td>Kelp with cushion fauna and/or foliose red sea...</td>
      <td>A</td>
      <td>A3</td>
      <td>A3.1</td>
      <td>A3.11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2115</th>
      <td>113610_cam_survey_1_frame2676.jpg</td>
      <td>1.525176e+09</td>
      <td>41.53336</td>
      <td>-8.80589</td>
      <td>-3.10</td>
      <td>-18.89</td>
      <td>21.810189</td>
      <td>01/05/18</td>
      <td>8.09</td>
      <td>A3.11</td>
      <td>Kelp with cushion fauna and/or foliose red sea...</td>
      <td>A</td>
      <td>A3</td>
      <td>A3.1</td>
      <td>A3.11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1934</th>
      <td>113610_cam_survey_1_frame962.jpg</td>
      <td>1.525175e+09</td>
      <td>41.53322</td>
      <td>-8.81097</td>
      <td>-1.48</td>
      <td>-17.99</td>
      <td>21.907689</td>
      <td>01/05/18</td>
      <td>10.21</td>
      <td>A3.1</td>
      <td>Atlantic and Mediterranean high energy infrali...</td>
      <td>A</td>
      <td>A3</td>
      <td>A3.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>245</th>
      <td>132143_forcadinho-np3_frame1283.jpg</td>
      <td>1.525183e+09</td>
      <td>41.53297</td>
      <td>-8.80974</td>
      <td>0.06</td>
      <td>-25.89</td>
      <td>21.897980</td>
      <td>01/05/18</td>
      <td>9.54</td>
      <td>A3.1</td>
      <td>Atlantic and Mediterranean high energy infrali...</td>
      <td>A</td>
      <td>A3</td>
      <td>A3.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1858</th>
      <td>113610_cam_survey_1_frame699.jpg</td>
      <td>1.525175e+09</td>
      <td>41.53322</td>
      <td>-8.81165</td>
      <td>-16.29</td>
      <td>-19.78</td>
      <td>21.914735</td>
      <td>01/05/18</td>
      <td>12.14</td>
      <td>A3.1</td>
      <td>Atlantic and Mediterranean high energy infrali...</td>
      <td>A</td>
      <td>A3</td>
      <td>A3.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.plot(sampled_df.level3.value_counts())
plt.plot([np.mean(sampled_df.level3.value_counts())]*len(sampled_df.level3.value_counts()), color='red', linestyle = '--')
plt.savefig('sampled_data.jpg')
print(np.mean(sampled_df.level3.value_counts()))
```

    132.42857142857142



![png](../figures/sampled_data.jpg)



```python
sampled_df.to_csv('sampled_data.csv', index=False)
```
