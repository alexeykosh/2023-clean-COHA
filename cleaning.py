import re
import argparse
import zipfile
import spacy
from os import listdir, path, mkdir
from os.path import isfile, join
from tqdm.auto import tqdm

nlp = spacy.load('en_core_web_sm')

def get_sents(file):
    '''
    Get the sentences from the text

    Parameters
    ----------
    file : list
        The list of lines from the text file
    
    Returns
    -------
    sents : list
        The list of sentences
    t_id : dict
        The dictionary of text ids
    '''

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
    Extract lemmas and POS tags from the text

    Parameters
    ----------
    name : str
        The name of the file
    sents : list
        The list of sentences
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
    '''
    Function that unzips the COHA files in the directory

    Parameters
    ----------
    dir : str
        The directory where the zip files are located
    unzip : str
        The directory where the text files will be extracted
    '''
    if not path.exists(unzip):            

        files = [f for f in listdir(dir) if isfile(join(dir, f))]

        for file in tqdm(files, 
                bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}',
                position=0, 
                leave=True):
            if '.zip' in file:
                with zipfile.ZipFile(f'{dir}/{file}', 'r') as zip_ref:
                    zip_ref.extractall(unzip) 

def clean_and_tag(unzip, spellcheck=False):
    '''
    Clean and tag the text files

    Parameters
    ----------
    unzip : str
        The directory where the text files are located
    spellcheck : bool, optional
        Whether to spellcheck the text, by default False
    '''
    files = [f for f in listdir(unzip) if isfile(join(unzip, f))]
    for file in tqdm(files, 
                bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}',
                position=0, 
                leave=True):
        with open(f'{unzip}/{file}', 'r', encoding='unicode_escape') as f:
            if path.exists(f'cleaned_tagged/{file}'):
                continue
            else:
                sents, t_id = get_sents(f.readlines())
                if spellcheck:
                    raise NotImplementedError
                    # sents = checker.correct_strings(sents)
                process_text(file, sents, t_id)


if __name__ == '__main__':
    # parce arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--unzip', type=str, default='tagged-txt')
    parser.add_argument('--dir', type=str, default='tagged')
    args = parser.parse_args()
    unzip = args.unzip
    dir = args.dir

    # execute the cleaning process
    print('...Unzipping files...')
    unzip_files(dir, unzip)
    print('...Cleaning and tagging files...')
    clean_and_tag(unzip)
