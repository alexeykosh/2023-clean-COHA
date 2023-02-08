import os
import argparse

def get_years(files):
    '''
    Get years and corresponding files

    Parameters
    ----------
    files : list
        The list of files in the folder
    
    Returns
    -------
    years : dict
        The dictionary of years and corresponding files
    '''
    years = {}
    for file in files:
        if file.endswith('.txt'):
            year = file.split('_')[2].split('.')[0]
            if year in years:
                years[year].append(file)
            else:
                years[year] = [file]
    return years

def combine_files(folder, folder_combined, years):
    '''
    Combine the files into one file per year

    Parameters
    ----------
    folder : str
        The directory where the cleaned and tagged files are located
    folder_combined : str
        The directory where the combined files will be stored
    years : dict
        The dictionary of years and corresponding files
    
    Returns
    -------
    None
    '''
    for year in years:
        # create a file to write to
        with open(os.path.join(folder_combined, 
                            'combined_' + year + '.txt'), 'wb') as outfile:
            # write to the file
            for fname in years[year]:
                with open(os.path.join(folder, fname), 'rb') as infile:
                    outfile.write(infile.read())


if __name__ == '__main__':
    # parce the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, 
                        help='The directory where the cleaned and tagged files are located')
    parser.add_argument('--folder_combined', type=str,
                        help='The directory where the combined files will be stored')
    args = parser.parse_args()
    folder = args.folder
    folder_combined = args.folder_combined

    # pefrom the combination
    files = os.listdir(folder)
    combine_files(folder, folder_combined, get_years(files))