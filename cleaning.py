import re
import argparse
import zipfile
import spacy
from os import listdir, path, mkdir
from os.path import isfile, join
from tqdm.auto import tqdm

nlp = spacy.load('en_core_web_sm')

def get_sents(file):
    sents = []
    sent = []
    t_id = {}
    s = 0
    for i in range(len(file)):
        word = file[i].replace('\n', '').split('\t')[1]
        if word in ['.', '!', '?']:
            sent.append(word)
            sents.append(sent)
            text_id = file[i].replace('\n', '').split('\t')[0]
            t_id[s] = text_id
            s += 1
            sent = []
        else:
            word = re.sub(r'[^\w\s]', '', word)
            if word.isalpha():
                sent.append(word)

    return [' '.join(i) for i in sents], t_id

def process_text(name, sents, t_id):
    '''
    Tags and lemmatises a cleaned text

    name: name of the file to be processed
    returns: a file with the following format:
    word \t lemma \t pos \t text_id
    '''

    if not path.exists('cleaned_tagged'):
        mkdir('cleaned_tagged')

    s_c = 0

    with open(f'cleaned_tagged/{name}', 'a') as f:
        for sent in nlp.pipe(sents,
                            n_process=-1):  
            for s in [[token.text, token.lemma_, token.pos_] for token in sent]:
                f.write('\t'.join(s) + '\t' + t_id[s_c] + '\n')

            s_c += 1

def unzip_files(dir, unzip):
    # get a list of files in the directory 

    if not path.exists(unzip):            

        files = [f for f in listdir(dir) if isfile(join(dir, f))]

        for file in tqdm(files, 
                bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}',
                position=0, 
                leave=True):
            if '.zip' in file:
                with zipfile.ZipFile(f'{dir}/{file}', 'r') as zip_ref:
                    zip_ref.extractall(unzip) 

if __name__ == '__main__':

    unzip = 'tagged-txt'
    dir = 'tagged'
    print('...Unzipping files...')
    unzip_files(dir, unzip)
    files = [f for f in listdir(unzip) if isfile(join(unzip, f))]
    print('...Cleaning and tagging files...')
    for file in tqdm(files, 
                bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}',
                position=0, 
                leave=True):
        # print(file)
        with open(f'{unzip}/{file}', 'r', encoding='unicode_escape') as f:
            # if file already in directory, skip it
            if path.exists(f'cleaned_tagged/{file}'):
                continue
            else:
                sents, t_id = get_sents(f.readlines())
                # # correct the sentences
                # sents = checker.correct_strings(sents)
                # process the sentences
                process_text(file, sents, t_id)
