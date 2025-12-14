import pandas as pd

# Load 2024 ANES dataset
ANES_URL = 'https://raw.githubusercontent.com/datamisc/ts-2024/main/data.csv'
N_THRESHOLD = 30
VARS = {
    "V243001": 'state',  # state
    "V241551": 'gender',  # gender
    # "V241003",  # sex (only 20 % of the sample)
    # 'V241610',  # e.g., political knowledge catch
    "V241612": 'polk_years',  # e.g., "How many years in full term for US Senator"
    "V241613": 'polk_spend',  # e.g., "Federal gov spending least"
    "V241614": 'polk_house',  # party with most members in House
    "V241615": 'polk_senat',   # party with most members in Senate
}

def main():
    df = pd.read_csv(ANES_URL, compression='gzip')
    df = df[VARS.keys()].rename(columns=VARS)

    # Keep male/female
    df = df[df['gender'].between(1,2)]
    df['male']   = (df['gender'] == 1).astype(int)
    df['female'] = (df['gender'] == 2).astype(int)

    # Keep states where n>=30
    mask = df['state'].value_counts() >= N_THRESHOLD
    mask = (df['state'].value_counts())[mask].index
    df = df[df['state'].isin(mask)]


    pol_knowledge_vars = df.columns[df.columns.str.contains('polk')]
    print(df[pol_knowledge_vars].describe())

    def clean_knowledge_variable(series, correct_values):
        # Replace invalid codes with NaN
        series_cleaned = series.replace([-9, -7, -6, -5, -4, -1], pd.NA)
        # Recode correct answers as 1, others as 0
        series_cleaned = series_cleaned.isin(
            correct_values
        ).astype(int)
        return series_cleaned


    df["polk_years"] = clean_knowledge_variable(
        df["polk_years"], [6]
    )
    df["polk_spend"] = clean_knowledge_variable(
        df["polk_spend"], [4]
    )
    df["polk_house"] = clean_knowledge_variable(
        df["polk_house"], [2]
    )
    df["polk_senat"] = clean_knowledge_variable(
        df["polk_senat"], [1]
    )
    df['polk_score'] = df[pol_knowledge_vars].sum(axis=1, skipna=True)/4


    grouped = df.groupby(['state', 'gender'])['polk_score'].agg(['mean','count','std'])

    return grouped['mean'].unstack().assign(gender_gap=lambda x: x[1] - x[2]).sort_values('gender_gap', ascending=False)

if __name__ == "__main__":
    main()

"""
In Massachusetts, the gender gap in political knowledge is 18.7 percentage points, with men answering, on average, 
nearly one-fifth more of the political knowledge items correctly than women. 
This represents one of the largest gender differences in political knowledge observed across states in 2024.
"""

