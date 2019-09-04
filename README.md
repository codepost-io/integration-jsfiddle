# Integrating with JSFiddle

This repository contains a short utility script that make it easy to import student submissions from JSFiddle to codePost.

## 0. List all JSFiddle URLs

Create a file called `fiddles.txt` that contains a list of all the JSFiddle files submitted by students, one per line. There is an example `fiddles.txt` file in this repo.

## 1. Create a roster

Since JSFiddle URLS are indexed by JSFiddle ID, we need to map {JSFiddle ID} to {email} in order to upload to codePost.

Create a roster.csv with the following information:

```
jsfiddle_id,email
rfreling,richard@codepost.io
scooper2,sheldon@codepost.io
aturing,alan@codepost.io
```

## 2. Run the script

Clone this repository or copy the python script `jsfiddle_to_codepost.py` to your local machine. Collect this script, `fiddles.txt`, and `roster.csv`into one folder. Then run

`python3 jsfiddle_to_codepost fiddles.txt roster.csv`

You should now see a folder called `codepost_upload`, whose subfolders correspond to students. Any problem files will show up in the `errors` folder.

## 4. Upload to codePost

Navigate to [codepost.io](https://codepost.io), log in, and click `Assignments -> Actions -> Upload Submissions -> Multiple Submissions`. Drag `codepost_upload` into codePost and voila.

If you prefer to have more control over the upload process, check out our [Python SDK](https://github.com/codepost-io/codepost-python).
