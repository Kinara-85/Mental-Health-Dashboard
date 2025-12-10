import pandas as pd
import numpy as np

def clean_data(df):
    df = df.copy()  
    df = clean_timestamp(df)
    df = clean_age(df)
    df = clean_gender(df)
    df = clean_country(df)
    df = clean_self_employed(df)
    df = clean_family_history(df)
    df = clean_treatment(df)
    df = clean_work_interfere(df)
    df = clean_no_employees(df)
    df = clean_remote_work(df)
    df = clean_tech_company(df)
    df = clean_benefits(df)
    df = clean_care_options(df)
    df = clean_wellness_program(df)
    df = clean_seek_help(df)
    df = clean_anonymity(df)
    df = clean_leave(df)
    df = clean_mental_health_consequence(df)
    df = clean_phys_health_consequence(df)
    df = clean_coworkers(df)
    df = clean_supervisor(df)
    df = clean_mental_health_interview(df)
    df = clean_phys_health_interview(df)
    df = clean_mental_vs_physical(df)
    df = clean_obs_consequence(df)
    df = handle_missing_values(df)
    df = convert_data_types(df)   
    return df

def clean_timestamp(df):
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.year
    return df

def clean_age(df):
    if 'Age' in df.columns:
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df.loc[(df['Age'] < 18) | (df['Age'] > 72), 'Age'] = np.nan
    return df

def clean_gender(df):
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].astype(str).str.lower()    
        naccept_male = ['m', 'male-ish', 'maile', 'something kinda male?', 'male', 'cis male',
                       'mal', 'male ', ' male', 'male (cis)', 'make', 'guy (-ish) ^_^',
                       'male leaning androgynous', 'man', 'mail', 'malr', 'cis man',
                       'ostensibly male, unsure what that really means'] 
        naccept_female = ['female', 'cis female', 'f', 'woman', 'femake', 'cis-female/femme',
                         'female (cis)', 'femail', 'female ', ' female']
        naccept_non_binary = ['trans-female', 'queer/she/they', 'non-binary', 'genderqueer',
                             'androgyne', 'agender', 'trans woman', 'neuter', 'female (trans)', 'queer']
        df['Gender'] = df['Gender'].replace(naccept_male, 'Male')
        df['Gender'] = df['Gender'].replace(naccept_female, 'Female')
        df['Gender'] = df['Gender'].replace(naccept_non_binary, 'Non-Binary') 
        accept_values = ['Male', 'Female', 'Non-Binary']
        for row in df['Gender'].unique():
            if row not in accept_values and pd.notna(row):
                df.loc[df['Gender'] == row, 'Gender'] = np.nan
    return df

def clean_country(df):
    if 'Country' in df.columns:
        df['Country'] = df['Country'].replace('USA', 'United States')
        df['Country'] = df['Country'].replace('germant', 'Germany')
        df['Country'] = df['Country'].replace(['russiaaaaa', 'Russiaaaaa'], 'Russia')
        df['Country'] = df['Country'].replace('Bahamas, The', 'Bahamas')
        df['Country'] = df['Country'].replace('bulgarria', 'Bulgaria')
        canada_variations = ['canada', 'Canada ']
        df['Country'] = df['Country'].replace(canada_variations, 'Canada')
        uk_variations = ['UK', 'United Kingdom ', 'uk']
        df['Country'] = df['Country'].replace(uk_variations, 'United Kingdom')
    return df

def clean_self_employed(df):
    if 'self_employed' in df.columns:
        yes_values = ['YES', 'Y', 'y']
        no_values = ['NO', 'N', 'n']
        df['self_employed'] = df['self_employed'].replace(yes_values, 'Yes')
        df['self_employed'] = df['self_employed'].replace(no_values, 'No')
    return df

def clean_family_history(df):
    if 'family_history' in df.columns:
        yes_values = ['YES', 'Y', 'y', 'yyy']
        no_values = ['NO', 'nnnn', 'n', 'N']
        df['family_history'] = df['family_history'].replace(yes_values, 'Yes')
        df['family_history'] = df['family_history'].replace(no_values, 'No')
    return df

def clean_treatment(df):
    if 'treatment' in df.columns:
        acceptable_values = ['Yes', 'No']
        df.loc[~df['treatment'].isin(acceptable_values), 'treatment'] = np.nan
    return df

def clean_work_interfere(df):
    if 'work_interfere' in df.columns:
        df['work_interfere'] = df['work_interfere'].replace('rarely', 'Rarely')
        df['work_interfere'] = df['work_interfere'].replace('oftem', 'Often')
        df['work_interfere'] = df['work_interfere'].replace('sometimem', 'Sometimes')
        df.loc[df['work_interfere'] == 'c', 'work_interfere'] = np.nan
    return df

def clean_no_employees(df):
    if 'no_employees' in df.columns:
        df['no_employees'] = (
            df['no_employees'].astype(str).str.strip().str.lower().str.replace(r'\s+', '', regex=True).replace({'25-jun': '6-25','05-jan': '5-1','5-jan': '5-1','morethan1000': '1000+'}))
    return df

def clean_remote_work(df):
    if 'remote_work' in df.columns:
        yes_values = ['YES', 'Y', 'y']
        no_values = ['NO', 'N', 'n'] 
        df['remote_work'] = df['remote_work'].replace(yes_values, 'Yes')
        df['remote_work'] = df['remote_work'].replace(no_values, 'No')
    return df

def clean_tech_company(df):
    if 'tech_company' in df.columns:
        df['tech_company'] = df['tech_company'].replace('Y', 'Yes')
        df['tech_company'] = df['tech_company'].replace('y', 'Yes')
    return df


def clean_benefits(df):
    if 'benefits' in df.columns:
        no_values = ['no', 'n', 'N']
        yes_values = ['yes', 'Y'] 
        df['benefits'] = df['benefits'].replace(no_values, 'No')
        df['benefits'] = df['benefits'].replace(yes_values, 'Yes')
        acceptable_values = ['No', 'Yes']
        df.loc[~df['benefits'].isin(acceptable_values), 'benefits'] = np.nan
    return df

def clean_care_options(df):
    if 'care_options' in df.columns:
        yes_values = ['y', 'yess', 'yesss', 'Yesss', 'Y', 'Yess']
        no_values = ['nop', 'nos', 'n', 'Nop', 'Nos', 'N', 'Not']
        df['care_options'] = df['care_options'].replace(yes_values, 'Yes')
        df['care_options'] = df['care_options'].replace(no_values, 'No')
        df['care_options'] = df['care_options'].replace(['Ns', 'Not sure'], 'Not Sure')
    return df

def clean_wellness_program(df):
    if 'wellness_program' in df.columns:
        df['wellness_program'] = df['wellness_program'].replace('Yess', 'Yes')
        df['wellness_program'] = df['wellness_program'].replace(['N', 'no'], 'No')
        invalid_values = ["'''", "'''''", '###', '####', '##3', '0', '?']
        df['wellness_program'] = df['wellness_program'].replace(invalid_values, np.nan)
    return df

def clean_seek_help(df):
    if 'seek_help' in df.columns:
        no_values = ['No.', 'NoS', 'Nop', 'Nowise', 'Nos']
        df['seek_help'] = df['seek_help'].replace(no_values, 'No')
    return df

def clean_anonymity(df):
    if 'anonymity' in df.columns:
        invalid_values = ['jnows', '###', '-']
        df['anonymity'] = df['anonymity'].replace(invalid_values, np.nan)
    return df

def clean_leave(df):
    if 'leave' in df.columns:
        invalid_values = ['//c difficult', 'option c', 'option c difficult', '// easy','//c', '#NOT EASY']
        df['leave'] = df['leave'].replace(invalid_values, np.nan)
        df['leave'] = df['leave'].replace("Don't know~", "Don't know")
        df['leave'] = df['leave'].replace('Somewhat difficultN', 'Somewhat difficult')
        df['leave'] = df['leave'].replace(['Very_easy', '#Very easy'], 'Very easy')
    return df

def clean_mental_health_consequence(df):
    if 'mental_health_consequence' in df.columns:
        df['mental_health_consequence'] = df['mental_health_consequence'].replace('?', np.nan)
    return df


def clean_phys_health_consequence(df):
    if 'phys_health_consequence' in df.columns:
        df['phys_health_consequence'] = df['phys_health_consequence'].replace(['?', ' '], np.nan)
        df['phys_health_consequence'] = df['phys_health_consequence'].replace('Not', 'No')
        df['phys_health_consequence'] = df['phys_health_consequence'].replace('Maybee', 'Maybe')
    return df

def clean_coworkers(df):
    if 'coworkers' in df.columns:
        df['coworkers'] = df['coworkers'].replace(['@', 'C'], np.nan)
        df['coworkers'] = df['coworkers'].replace('Yess', 'Yes')
        df['coworkers'] = df['coworkers'].replace(['Some of them ', 'Sot'], 'Some of them')
    return df

def clean_supervisor(df):
    if 'supervisor' in df.columns:
        no_values = ['N0', 'No.', 'n', '/n', 'NO']
        df['supervisor'] = df['supervisor'].replace(no_values, 'No')
        df['supervisor'] = df['supervisor'].replace('/y', 'Yes')
        df['supervisor'] = df['supervisor'].replace('////', np.nan)
    return df

def clean_mental_health_interview(df):
    if 'mental_health_interview' in df.columns:
        no_values = ['Nope', 'Nat', 'Nnn', 'N', 'No-no', 'Nn', 'N0', 'Not']
        df['mental_health_interview'] = df['mental_health_interview'].replace(no_values, 'No')  
        invalid_values = ['0', '=', 'Oo', 'O']
        df['mental_health_interview'] = df['mental_health_interview'].replace(invalid_values, np.nan)
    return df

def clean_phys_health_interview(df):
    if 'phys_health_interview' in df.columns:
        yes_values = ['Ys', 'yS']
        no_values = ['nop', 'nos', 'n', 'Nop', 'Nos', 'N', 'Not', 'N0', 'No-N', 'NAT']
        invalid_values = ['vvvvv', '^^6', '^^^', '^^^6', 'TT']   
        df['phys_health_interview'] = df['phys_health_interview'].replace(invalid_values, np.nan)
        df['phys_health_interview'] = df['phys_health_interview'].replace(yes_values, 'Yes')
        df['phys_health_interview'] = df['phys_health_interview'].replace(no_values, 'No')
        df['phys_health_interview'] = df['phys_health_interview'].replace(['May be', 'Maybe?'], 'Maybe')
    return df

def clean_mental_vs_physical(df):
    if 'mental_vs_physical' in df.columns:
        invalid_values = ['Nil', '!!!!!', 'T know', '!!!!']
        df['mental_vs_physical'] = df['mental_vs_physical'].replace(invalid_values, np.nan)   
        dont_know_values = ["Don't know!", "Don't", 'T know', "Don't "]
        df['mental_vs_physical'] = df['mental_vs_physical'].replace(dont_know_values, "Don't know")  
        no_values = ['Nat', 'No.', 'Noz', 'Not']
        df['mental_vs_physical'] = df['mental_vs_physical'].replace(no_values, 'No')
    return df

def clean_obs_consequence(df):
    if 'obs_consequence' in df.columns:
        df['obs_consequence'] = df['obs_consequence'].replace('TT', np.nan)  
    return df

def handle_missing_values(df):
    if 'Age' in df.columns:
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    return df

def convert_data_types(df):
    if 'Timestamp' in df.columns:
        df['Timestamp'] = df['Timestamp'].astype('int32')
    if 'Age' in df.columns:
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce').astype('Int64')
    categorical_cols = [
        'Gender', 'Country', 'self_employed', 'family_history', 'treatment',
        'work_interfere', 'no_employees', 'remote_work', 'tech_company', 'benefits',
        'care_options', 'wellness_program', 'seek_help', 'anonymity', 'leave',
        'mental_health_consequence', 'phys_health_consequence', 'coworkers',
        'supervisor', 'mental_health_interview', 'phys_health_interview',
        'mental_vs_physical', 'obs_consequence'] 
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    numeric_cols = ['Years_in_Tech', 'Years_in_Current_Role', 'Sick_Leave_Days', 'Average_Weekly_Hours']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('int64')
    return df