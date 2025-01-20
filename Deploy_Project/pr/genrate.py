import pandas as pd
import os
import random
import string

# Load the sample spam and ham dataset
df = pd.read_csv('random_spam_ham.csv')

# Directory to save the text files
output_dir = 'output_txt_files'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to generate a random filename
def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.txt'

# Iterate through the dataframe and create text files
for index, row in df.iterrows():
    message = row['Message']
    # Generate a random filename
    filename = generate_random_filename()
    file_path = os.path.join(output_dir, filename)
    
    # Write the message to the .txt file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(message)

print(f"Text files have been saved to the '{output_dir}' directory.")
