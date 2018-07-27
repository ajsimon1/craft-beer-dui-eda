## Exploratory Data Analysis Kaggle Craft Beer Dataset

Found an interesting dataset on [craft beer and breweries](https://www.kaggle.com/nickhould/craft-cans).  Initially, I had basic
questions on
- What is the most popular beer style?
- What state has the most breweries?
- The highest avg ABV %?

After these initial questions I decided to explore any relationships between
fatalities from drunk driving as reported by another kaggle dataset on  [DUIs and fatalities](https://www.kaggle.com/bryanmaloney/dui-arrests-and-population-by-state-2015-usa/version/2) by state.

Import necessary packages
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

Begin by importing the csv into dataframes.  The craft beer set included 2
csv files, 1 detailing actual beer and the other breweries.  The third csv is the
DUI and fatalities set.

```python
# ################## load datasets #####################################
df_beers = pd.read_csv('beers.csv', index_col=0)
df_brews = pd.read_csv('breweries.csv', index_col=0)
df_fatal = pd.read_csv('DUI.csv', index_col=0)
```

The beer datasets are combined into a single dataset based on the *brewery_id*
column on the beer side acting as a foreign key to the an id column on the
brewery side.  In order to ensure matching, an *id* column was set in the
brewery dataset as **+1** of the loaded index.  The fatality data is left
out due to avoid listing the summary statistics per state in duplicate for
each beer style; these sets are explored in tandem later on.

```python
# add index as column for easy merging, adding to zero based index to
# match 'brewery_id' column that is one base indexed
df_brews['id'] = df_brews.index + 1
```

Once the *id/brewery_id* columns are in place, the sets are combined using
and *outer* join.  I choose this join to retain non-matching rows in the
final dataset.

```python
# merge datasets on 'brewery_id'/'id'
df_comb = pd.merge(df_beers,
                       df_brews,
                       how='outer',
                       left_on='brewery_id',
                       right_on='id')
```

Cleaning continues:
```python
# ################### clean datasets ###################################
# remove unamed column
df_comb = df_comb.loc[:, ~df_comb.columns.str.contains('^Unnamed')]

# rename columns
col_rename = {'id_x':'beer_id', 'name_x':'beer_name', 'name_y':'brewery'}
df_comb = df_comb.rename(index=str, columns=col_rename)

# remove unecessary id_y column
df_comb = df_comb.drop(labels='id_y', axis=1)
```

Check info() method on combined dataframe for insight on values
 ```python
 df_comb.info()
 ```
 ```
  <class 'pandas.core.frame.DataFrame'>
  Index: 2411 entries, 0 to 2410
  Data columns (total 10 columns):
  abv           2348 non-null float64
  ibu           1405 non-null float64
  beer_id       2410 non-null float64
  beer_name     2410 non-null object
  style         2405 non-null object
  brewery_id    2410 non-null float64
  ounces        2410 non-null float64
  brewery       2405 non-null object
  city          2405 non-null object
  state         2405 non-null object
  dtypes: float64(5), object(5)
  memory usage: 207.2+ KB
```

Need to take care of NaN values for various columns.

For the missing *stle* column, the NaN values are replaced with ***Unknown***
```python
# work on style column NaN first
# remove row at index 2410, values were mostly NaN
df_comb = df_comb.drop(df_comb.index[2410])
# replacing remaining 'style' NaN with 'unknown'
df_comb['style'].fillna('Unknown', inplace=True)
```

Some googling revealed the *brewery*, *city*, *state* missing values were from a single brewery, Northgate Brewing. These values
were also replaced with `fillna()` method.
```python
# work on 'brewery', 'city', 'state' columns
# all NaN in above columns are from Northgate Brewing, googled beer names
df_comb['brewery'].fillna('Northgate Brewing', inplace=True)
df_comb['city'].fillna('Minneapolis', inplace=True)
df_comb['state'].fillna('MN', inplace=True)
```
Finally, the *abv* and *ibu* column NaN values were filled with
the average value of the column.
```python
# work on abv & ibu by setting NaN to average of column
# set mean of the column to a variable
abv_mean = df_comb['abv'].mean(skipna=True).round(2)
ibu_mean = df_comb['ibu'].mean(skipna=True).round(2)
# use mean var to fill NaN of each column
df_comb['abv'].fillna(abv_mean, inplace=True)
df_comb['ibu'].fillna(ibu_mean, inplace=True)
```
A final check with `info()` method to confirm all NaN values NaN values have been replaced.
```
<class 'pandas.core.frame.DataFrame'>
Index: 2410 entries, 0 to 2409
Data columns (total 10 columns):
abv           2410 non-null float64
ibu           2410 non-null float64
beer_id       2410 non-null float64
beer_name     2410 non-null object
style         2410 non-null object
brewery_id    2410 non-null float64
ounces        2410 non-null float64
brewery       2410 non-null object
city          2410 non-null object
state         2410 non-null object
dtypes: float64(5), object(5)
memory usage: 207.1+ KB
```
