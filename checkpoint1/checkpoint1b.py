"""
Checkpoint 1b

*First complete the steps in checkpoint1a.pdf

Here you will create a script to preprocess the data given in starbucks.csv. You may want to use
a jupyter notebook or python terminal to develop your code and test each function as you go... 
you can import this file and its functions directly:

    - jupyter notebook: include the lines `%autoreload 2` and `import preprocess`
                        then just call preprocess.remove_percents(df) to test
                        
    - python terminal: run `from importlib import reload` and `import preprocess`
                       each time you modify this file, run `reload(preprocess)`

Once you are finished with this program, you should run `python preprocess.py` from the terminal.
This should load the data, perform preprocessing, and save the output to the data folder.

"""
import pandas as pd
import numpy as np

def remove_percents(df, col):
    if pd.api.types.is_string_dtype(df[col]):
        df[col] = df[col].str.slice(stop=-1).astype(float)
    return df

def fill_zero_iron(df):
    df['Iron (% DV)'] = df['Iron (% DV)'].fillna(0)
    return df
    
def fix_caffeine(df):
    df['Caffeine (mg)'] = df['Caffeine (mg)'].replace("varies", np.NaN)
    df['Caffeine (mg)'] = df['Caffeine (mg)'].replace("Varies", np.NaN)
    df['Caffeine (mg)'] = df['Caffeine (mg)'].astype(float)
    df['Caffeine (mg)'] = df['Caffeine (mg)'].fillna(df['Caffeine (mg)'].mean())
    return df

def standardize_names(df):
    for i in range(len(df.columns.values)):
        pos = df.columns.values[i].find('(')
        if pos != -1:
            df.columns.values[i] = df.columns.values[i][:pos - 1]
        df.columns.values[i] = df.columns.values[i].lower()
    return df


def fix_strings(df, col):
    for i in range(len(df[col])):
        chars = [char.lower() for char in df[col][i] if char.isalpha()]
        df[col][i] = "".join(chars)
    return df


def main():
    
    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')
    
    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)
    
    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)

    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)
    
    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)
    
    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)
    
    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    df.to_csv('../data/starbucks_clean.csv')
    

if __name__ == "__main__":
    main()
