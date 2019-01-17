# Day02 Data Preprocessing - NumPy & Pandas

#### Installation

pip

```
pip install numpy
pip install pandas
```

conda

```
conda install numpy
conda install pandas
```

#### Import

```python
import pandas as pd
import numpy as np
```

詳細numpy, pandas操作請見Day02.ipynb

### Pandas (分組)

#### GroupBy

#### Pandas.cut( )

等寬劃分(每個 bin 的值的範圍大小都是一樣的)

`pd.cut(df["col"], 4)`

等頻劃分(每個bin的筆數相同)

```python
pd.qcut(ages["age"], 4)`
```

numpy切​

```python
#自 20 到 70 歲，切 11 個點 (得到 10 組)
bin_cut = np.linspace(20, 70, 11)
age_data['YEARS_BINNED'] = pd.cut(age_data['YEARS_BIRTH'], bins = bin_cut)
```
