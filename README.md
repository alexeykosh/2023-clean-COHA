# 2023-clean-COHA

A collection of scripts used to run different NLP and cleaning pipelines on the COHA corpus. 

### Installing the dependencies 

This script uses spaCy and tqdm, to install these packages run the following command: 

```bash
pip install -r requirements.txt
```

### Cleaning the files and adding POS-tags and lemmas 

_src/clean.py_ is the script used to clean, lemmatize and add POS-tags to the COHA corpus. The lemmatization and POS-taggind is done using the spaCy python library. To run the script, paste the following command in the command line: 

```bash
python process_text.py --unzip <path_to_zipped_files> --clean_tag <path_to_where_to_store_the_output>
```

### Combining the files

_src/combine.py_ is script for combining files in a directory into one file per year. To use the script, you need to provide two arguments: _folder_ and _folder_combined_. _folder_ is the directory where the cleaned and tagged files are located, while _folder_combined_ is the directory where the combined files will be stored. The script will take the list of files in _folder_, extract the year from each file name, and group the files by year. Finally, it will combine the files in each year into a single file and save it in the folder_combined directory. To run the script, you can use the following command line example: 

```bash
python filename.py --folder <path_to_folder> --folder_combined <path_to_folder_combined>
```
