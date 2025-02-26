# Kanoa Borromeo

# These are the necessary libraries:
# - pandas helps with data manipualtions as well as analysis
# - re supports expression operations which simplify tasks like pattern matching
import pandas as pd
import re

# The two datasets we need:
# - The goal is to load these datasets into a pandas data frame which can allow us to manipulate them 
# ***YOU NEED TO LOAD THE FILES IN FROM YOUR OWN DEVICE
defect_df = pd.read_csv('Insert Defect Write Ups File Here')
ata_dict_df = pd.read_csv('Insert Defect Categories Configuration - Defect Categories File Here')

# This creates a dictionary that maps keywords from the 'key_words' column in 
# 'ata_dict_df' to the corresponding 'category_chapter' ATA codes and be used 
# later to map defect descriptions to their appropriate ATA codes.
ata_dict = pd.Series(ata_dict_df['category_chapter'].values, index=ata_dict_df['key_words'].str.lower()).to_dict()

# This function takes a defect description and checks if any keywords from the ATA mapping dictionary appear
# in the description, and if a keyword is not found, then nothing is returned, but if it is, then it returns 
# the respective ATA code
def map_ata_code(defect_desc):
    """Maps defect descriptions to ATA codes using the dictionary."""
    for keyword, ata_code in ata_dict.items():
        if re.search(keyword, defect_desc.lower()):
            return ata_code
    return None

# This function takes a text input like a defect description, removes any extra spacing and converts it to lowercase
# and then trims the whitespace around the text which creates a standardized text format
def standardize_text(text):
    if pd.isna(text):
        return ''
    return re.sub(r'\s+', ' ', text).strip().lower()

# This section applies the data cleaning and ATA code mapping by standardizing the text in 'defect_description', mapping 
# each defect descrition to a ATA code, and identifying any missing or incomplete entries where no ATA code was mapped
defect_df['Standardized_Description'] = defect_df['defect_description'].apply(standardize_text)
defect_df['Mapped_ATA_Code'] = defect_df['Standardized_Description'].apply(map_ata_code)

# This part saves the cleaned data and the missing entries to seperate CSV files. 
missing_entries = defect_df[defect_df['Mapped_ATA_Code'].isna()]

# Output cleaned results to CSV
defect_df.to_csv('/Users/kanoa/Downloads/cleaned_defect_write_ups.csv', index=False)
missing_entries.to_csv('/Users/kanoa/Downloads/missing_entries.csv', index=False)

# This section provides feedback by printing the number od defect entries that were missing ATA codes
print("Data cleaning and ATA code mapping complete.")
print(f"{len(missing_entries)} entries were missing ATA codes.")
