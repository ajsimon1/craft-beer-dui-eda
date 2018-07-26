# -*- coding: utf-8 -*-
"""
Created on Thu May  3 20:24:58 2018

@author: Adam

exploration into the craft beer dataset on kaggle
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ################## load datasets #####################################
df_beers = pd.read_csv('beers.csv', index_col=0)
df_brews = pd.read_csv('breweries.csv', index_col=0)
df_fatal = pd.read_csv('DUI.csv', index_col=0)

# ################### clean datasets ###################################
# add index as column for easy merging, adding to zero based index to
# match 'brewery_id' column that is one base indexed
df_brews['id'] = df_brews.index + 1

# merge datasets on 'brewery_id'/'id'
df_comb = pd.merge(df_beers,
                       df_brews,
                       how='outer',
                       left_on='brewery_id',
                       right_on='id')

# remove unamed column
df_comb = df_comb.loc[:, ~df_comb.columns.str.contains('^Unnamed')]

# rename columns
col_rename = {'id_x':'beer_id', 'name_x':'beer_name', 'name_y':'brewery'}
df_comb = df_comb.rename(index=str, columns=col_rename)

# remove unecessary id_y column
df_comb = df_comb.drop(labels='id_y', axis=1)

# TODO clean up data, too many NaN
# TODO convert both df_comb to full name

# questions
# avg abv per beer style
df_comb.groupby(by='style')['abv'].mean()
# total count per beer style
df_comb.groupby(by='style')['abv'].count()
# top 5 produced beer styles
df_comb['style'].value_counts().head()
# most common beer style in each state

# most ounces per state?
df_sum_ounces = df_comb.groupby('state')['ounces'].sum()
df_sum_ounces.sort_values(ascending=False).head()
# most popular style list
df_comb['style'].count
# top 5 states with most variety
df_most_style_state = df_comb.groupby(by='state')['style'].count()
df_most_style_state.sort_values(ascending=False).head()
# top 5 most breweries per state
df_brew_per_state = df_comb.groupby('state')['brewery'].count()
df_brew_per_state.sort_values(ascending=False).head()
# zoom in on NJ
# get lats and longs for cities, plot
# brewery with most styles
df_style_brew_count = df_comb.groupby('brewery')['style'].count()
df_style_brew_count.sort_values(ascending=False)
# city with most breweries
df_brew_per_city = df_comb.groupby('city')['brewery'].count()
df_brew_per_city.sort_values(ascending=False).head()
# most alcohol for all style, uselsess
df_most_bitter_style = df_comb.groupby('style')['abv'].sum()
df_most_bitter_style.sort_values(ascending=False).head()
# avg alcohol per style
df_avg_bitter_style = df_comb.groupby('style')['abv'].mean()
df_avg_bitter_style.sort_values(ascending=False).head()
# map of usa with breweries as volume per state
# what brewery makes highest abv beer
df_high_abv_style = df_comb.groupby('style')['abv'].max()
df_high_abv_style.sort_values(ascending=False).head
df_high_alc_style_state = df_comb.groupby(['state', 'beer_name'])['abv'].max()
df_high_alc_style_state.sort_values(ascending=False)
# count of style by state
df_count_style_state = df_comb.groupby(['state', 'style'])['abv'].count()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
