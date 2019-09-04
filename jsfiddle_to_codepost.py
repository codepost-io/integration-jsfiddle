# =============================================================================
# codePost – JSFiddle Utility
#
# Takes a list of JSFiddle URLs and downloads them into a file structure
# that codePost will recognize.
#
# =============================================================================

# Python stdlib imports
import requests
import re
import os
import shutil
import csv
import argparse

# Other imports
# pip install bs4
from bs4 import BeautifulSoup

# =============================================================================

parser = argparse.ArgumentParser(description='JSFiddle to codePost!')
parser.add_argument(
    'fiddles', help='A text file with the JSFiddle urls, one per line')
parser.add_argument(
    'roster', help='The course roster of students that includes JSFiddle id and email')
parser.add_argument(
    'assignment_name', help='The name for the jsfiddle submissions. Ex.: assignment1.js')
args = parser.parse_args()

# =============================================================================
#

FIDDLES = args.fiddles
ROSTER = args.roster
ASSIGNMENT_NAME = args.assignment_name

OUTPUT_DIRECTORY = 'codepost_upload'
ERROR_DIRECTORY = 'errors'

DEBUG = True

# =============================================================================

_cwd = os.getcwd()
_upload_dir = os.path.join(_cwd, OUTPUT_DIRECTORY)
_error_dir = os.path.join(_cwd, ERROR_DIRECTORY)


def parse_jsfiddle(url, id_to_email):
  match = re.match(r"^https://jsfiddle.net/(.*?)/", url)
  if match != None:
    username = match.group(1)

  response = requests.get(url)
  parsed_html = BeautifulSoup(response.content, features="html.parser")
  scripts = parsed_html.head.findAll('script')

  for script in scripts:
    if 'EditorConfig' in script.text:
      # Extract object from EditorConfig
      objs = re.findall(r"{.*}", script.text.strip(), re.MULTILINE | re.DOTALL)
      if len(objs) == 1:
        # Extract js from EditorConfig object
        submission_escaped = re.findall(
            r"js:\s*\"(.*)\"", objs[0], re.MULTILINE)

        # Remove escaped single and double quotes
        submission_string = re.compile(
            r"\\(\'|\")").sub(r'\1', submission_escaped[0])

        # Split the single-line string to newlines
        submission_lines = submission_string.split('\\n')

        if username != None and normalize(username) in id_to_email:
          dirname = id_to_email[normalize(username)]

          student_dir = os.path.join(_upload_dir, dirname)
          os.makedirs(student_dir)

          with open(os.path.join(student_dir, ASSIGNMENT_NAME), 'w') as f:
            for l in submission_lines:
              f.write(l + '\n')
        else:
          with open(os.path.join(_error_dir, url.split('/')[-2]), 'w') as f:
            for l in submission_lines:
              f.write(l + '\n')

        print('#', end="")


def delete_directory(path):
  if os.path.exists(path):
    shutil.rmtree(path)


def normalize(string):
  return string.lower().strip()


def validate_csv(row):
  for key in row.keys():
    if 'jsfiddle' in normalize(key):
      jsfiddle = key
    elif 'email' in normalize(key):
      email = key

  if jsfiddle == None or email == None:
    if first == None:
      print("Missing header: jsfiddle_id")
    if email == None:
      print("Missing header: email")

    raise RuntimeError(
        "Malformatted roster. Please fix the headers and try again.")

    return (jsfiddle, email)
  else:
    return (jsfiddle, email)


def id_to_email(roster):
  with open(roster, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    jsfiddle, email = (None, None)
    id_to_email = {}
    for row in csv_reader:
      if line_count == 0:
        (jsfiddle, email) = validate_csv(row)
        line_count += 1

      id_to_email[normalize(row[jsfiddle])] = normalize(row[email])
      line_count += 1
    return id_to_email


# Overwrite the directories if they exist already
delete_directory(_upload_dir)
delete_directory(_error_dir)
os.makedirs(_upload_dir)
os.makedirs(_error_dir)

with open(FIDDLES) as f:
  urls = f.readlines()

urls = [x.strip() for x in urls]

id_to_email = id_to_email(ROSTER)

for url in urls:
  parse_jsfiddle(url, id_to_email)
