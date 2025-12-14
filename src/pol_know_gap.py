import pandas as pd

# Load the 2024 ANES dataset
data_url_anes = 'https://raw.githubusercontent.com/datamisc/ts-2024/main/data.csv'
N_THRESHOLD = 60
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

df = pd.read_csv(data_url_anes, compression='gzip')
df = df[VARS.keys()].rename(columns=VARS)

mask = df['V243001'].value_counts() >= N_THRESHOLD
mask = (df['V243001'].value_counts())[mask].index
df['state'] = df['V243001']
df = df[df['state'].isin(mask)]

df = df[df['V241551'].between(1,2)]

df['male']   = (df['V241551'] == 1).astype(int)
df['female'] = (df['V241551'] == 2).astype(int)


# === STEP 2: Select political knowledge items ===
# Replace with actual variable names
pol_knowledge_vars = [
    # 'V241610',  # e.g., political knowledge catch
    'V241612',  # e.g., "How many years in full term for US Senator"
    'V241613',  # e.g., "Federal gov spending least"
    'V241614',  # party with most members in House
    'V241615'   # party with most members in Senate
]
print(df[pol_knowledge_vars].describe())
