#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Step 1: Load the Dataset

# In[10]:


file_path = r"C:\Users\owner\Downloads\Onyx Data - DataDNA Dataset Challenge - Washington Crimes Dataset - March 2025\Onyx Data -DataDNA Dataset Challenge - Washington Crimes Dataset - March 2025.xlsx"

df = pd.read_excel(file_path, parse_dates=['START_DATE', 'END_DATE'])

print(df.head())


# ##### Why?
# We import pandas for data manipulation and matplotlib/seaborn for visualization.
# parse_dates=['START_DATE', 'END_DATE'] ensures date columns are correctly interpreted as datetime instead of strings, making it easier to work with time-based analysis.

# In[14]:


df.head()


# ### Step 2: Standardize Column Names

# In[27]:


# Strip column names of any spaces
df.columns = df.columns.str.strip()


# ### Why?
# df.columns.str.strip() removes any extra spaces that might cause errors when accessing columns.
# df.rename(columns={'sector': 'SECTOR'}) corrects case inconsistencies to ensure uniformity.

# In[26]:


# Display missing values before cleaning
print("Missing values before cleaning:\n", df.isnull().sum())


# Why?
# It's important to identify missing values before applying any cleaning methods to understand the extent of the issue.
# 

# In[18]:


df.columns = df.columns.str.strip()  


# In[20]:


df.rename(columns={'sector': 'SECTOR'}, inplace=True)  


# ### Step 4: Filling Missing Values
# A. Categorical Columns
# 
# These columns represent categories (e.g., sectors, districts), and missing values are best filled with the most frequent value (mode()).Using mode()[0] ensures we pick the most common category.
# 

# In[32]:


# Fill 'SECTOR', 'PSA', 'BID', 'DISTRICT' with the most common value (mode)
for col in ['SECTOR', 'PSA', 'BID', 'DISTRICT']:
    df[col] = df[col].fillna(df[col].mode()[0])


# ### Handling Missing IDs
# 
# OCTO_RECORD_ID is likely a unique identifier, and filling it with a mode or median doesn’t make sense.
# "Unknown" ensures that we recognize these records as missing.
# 

# In[31]:


# Fill 'OCTO_RECORD_ID' and 'DICTIONARY' with 'Unknown' or 0 if numeric
df['OCTO_RECORD_ID'] = df['OCTO_RECORD_ID'].fillna('Unknown')


# ### Missing Dates
#  
# Dates should follow a logical order.
# If a date is missing, we assume it happened at the earliest recorded time rather than inserting an arbitrary date.

# In[35]:


# Fill missing 'START_DATE' and 'END_DATE' with the earliest date available
df['START_DATE'] = df['START_DATE'].fillna(df['START_DATE'].min())
df['END_DATE'] = df['END_DATE'].fillna(df['END_DATE'].min())


# ### Verify Missing Values After Cleaning

# In[34]:


# Display missing values after cleaning
print("\nMissing values after cleaning:\n", df.isnull().sum())


# In[38]:


if df['BLOCK_GROUP'].isnull().sum() > 0:
    df['BLOCK_GROUP'] = df.groupby('CENSUS_TRACT')['BLOCK_GROUP'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Unknown'))
    
    # If there are still missing values, fill with mode
    df['BLOCK_GROUP'] = df['BLOCK_GROUP'].fillna(df['BLOCK_GROUP'].mode()[0])

print("✅ Missing BLOCK_GROUP values handled.")


# In[39]:


# Display missing values after cleaning
print("\nMissing values after cleaning:\n", df.isnull().sum())


# In[40]:


if df['CENSUS_TRACT'].isnull().sum() > 0:
    df['CENSUS_TRACT'] = df.groupby(['WARD', 'NEIGHBORHOOD_CLUSTER'])['CENSUS_TRACT'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Unknown'))
    
    # If still missing, use mode
    df['CENSUS_TRACT'].fillna(df['CENSUS_TRACT'].mode()[0], inplace=True)

print("✅ Missing CENSUS_TRACT values handled.")


# In[41]:


# Display missing values after cleaning
print("\nMissing values after cleaning:\n", df.isnull().sum())


# In[43]:


# Save as Excel file
output_file = "cleaned_washington_crime_data.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Cleaned data saved to {output_file}")


# In[44]:


import os

output_file = "cleaned_washington_crime_data.xlsx"
file_path = os.path.abspath(output_file)

print(f"✅ Cleaned data saved at: {file_path}")


# In[ ]:




