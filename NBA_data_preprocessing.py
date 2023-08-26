import pandas as pd
import os
import requests
import regex as re
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


'''In this project I was preparing raw NBA data for the future ML analysis'''


# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"


def clean_data(data_path):

    # editing the values columns
    df = pd.read_csv(data_path)
    df['b_day'] = pd.to_datetime(df['b_day'])
    df['draft_year'] = pd.to_datetime(df['draft_year'], format="%Y")
    df['team'].fillna("No Team", inplace=True)
    df['height'] = df['height'].apply(lambda x: float(x.split()[-1]))
    df['weight'] = df['weight'].apply(lambda x: float(x.split()[-2]))
    df['salary'] = df['salary'].apply(lambda x: float(x[1:]))

    # breaking countries into "USA" and "not-USA" for simplicity
    def replace_usa(x):
        if x == 'USA':
            country = 'USA'
        else:
            country = 'Not-USA'
        return country

    df['country'] = df['country'].apply(replace_usa)

    df['draft_round'].replace('Undrafted', '0', inplace=True)
    return df


def feature_data(df):

    # calculating data from existing column (age, bmi, experience) and removing high cardinality features
    df['version'] = df['version'].str.replace('NBA2k', '20')
    df['version'] = pd.to_datetime(df['version'], format="%Y")
    df['age'] = df['version'].dt.year - df['b_day'].dt.year
    df['experience'] = df['version'].dt.year - df['draft_year'].dt.year
    df['bmi'] = df['weight'] / pow(df['height'], 2)
    df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height'], inplace=True)
    high_cardinality = [column for column in df.columns if df[column].dtype == object and df[column].nunique() > 50]
    df.drop(columns=high_cardinality, inplace=True)
    return df


def multicol_data(feature):

    # dropping multicollinear features + checking correlation on the plot
    feature.drop('age', axis=1, inplace=True)
    numeric_feature = feature.select_dtypes(include=['number'])
    correlation = numeric_feature.corr()
    print(correlation)
    plt.imshow(correlation, cmap='coolwarm')
    plt.colorbar()
    return feature


def transform_data(z):

    # Using StandardScaler to transform numerical features in the DataFrame
    # Transforming nominal categorical variables in the DataFrame using OneHotEncoder;
    # Concatenating the transformed numerical and categorical features
    y = z['salary']
    num_feat_df = z.select_dtypes('number')
    num_feat_df = num_feat_df.drop('salary', axis=1)
    cat_feat_df = z.select_dtypes('object')
    # num_feat_df.describe()
    # cat_feat_df.describe()
    scaler_std = StandardScaler()
    df_standard = scaler_std.fit_transform(num_feat_df)
    df_standard = pd.DataFrame(df_standard, columns=num_feat_df.columns)

    one_hot = OneHotEncoder()
    df_one_hot = one_hot.fit_transform(cat_feat_df)
    cat_feat_names = one_hot.get_feature_names_out(cat_feat_df.columns)
    cat_feat_names_cleaned = [name.split('_')[-1] for name in cat_feat_names]

    df_one_hot = pd.DataFrame(df_one_hot.toarray(), columns=cat_feat_names_cleaned)

    final_df = pd.concat([df_standard, df_one_hot], axis=1)

    return final_df, y


path = "../Data/nba2k-full.csv"
df_cleaned = clean_data(path)
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
X, y = transform_data(df)


print(X.head(), y)
