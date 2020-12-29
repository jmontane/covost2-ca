#!/usr/bin/env python3

import zipfile
import wget
import re

# CoVoST2 translations file
covost2_url = 'https://dl.fbaipublicfiles.com/covost/covost2.zip'

# File with CommonVoice English sentences translated to Catalan by humans
covost2_source_file = 'validated.en_ca.en'

# Output file
covost2_target_file = 'covost2-ca.txt'

# Discarted sentences
discarted_file = 'covost2-ca-discarted.txt'

# char replacements table
source_chars = '´‘’“”«»'
target_chars ='\'\'\'""""'
translation = str.maketrans(source_chars, target_chars)


def normalize_line(line):

    line = line.translate(translation)
    return(line)

def validate_line(line):

    if (re.match("^[a-zA-ZçÇáàèéíïòóóúüÁÀÈÉÍÏÒÓÚÜ·¡¿!\? ,;:.\"'\.\(\)/–-]+\n$", line)):
        return True
    return False

# Download CoVoST2 translations
wget.download(covost2_url)

# Get English to Catalan translated sentences
with zipfile.ZipFile('covost2.zip','r') as zip_ref:
    zip_ref.extract('covost2/' + covost2_source_file)

# Parse translations

# Store lines already seen
lines_seen = set() 

with open(covost2_target_file, 'w') as output_file, open(discarted_file, 'w') as removed_file:
    for line in open('covost2/' + covost2_source_file, 'r'):
        # Normalize line
        line = normalize_line(line)
        # Check if line is duplicated
        if line not in lines_seen:
            # Store line as seen
            lines_seen.add(line)
            # If it's a valid sentece, write it
            if validate_line(line):
                 output_file.write(line)
            else:
                 removed_file.write(line)

