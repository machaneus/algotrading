import os
import zipfile
from subprocess import Popen, PIPE, STDOUT


def unzip(zip_filename, dst_directory):
    try:
        if os.path.isfile(zip_filename):
            zip_ref = zipfile.ZipFile(zip_filename, 'r')
            zip_ref.extractall(dst_directory)
            zip_ref.close()
    except zipfile.BadZipfile:
        pass

def remove_first_line(filenames):
    for filename in filenames:
        sed_command = "sed '1d' " + filename  + " > tmpfile; mv tmpfile " + filename
        sed_command = "sed '1d' {}  > tmpfile; mv tmpfile {}".format(filename, filename)
        os.system(sed_command)

def remove_directory(directory):
    rm_command = 'rm -r {}'.format(directory)
    os.system(rm_command)

def concatenate_files(original_filenames, new_filename, remove_original = False):
    cat_command = 'cat {} > {}'.format(" ".join(original_filenames), new_filename)
    os.system(cat_command)
    if (remove_original):
        rm_command = 'rm {}'.format(" ".join(original_filenames))
        os.system(rm_command)

def extract_and_merge(zip_filenames, new_filename):
    if '/' in new_filename:
        tmp_directory = '{}/temp'.format('/'.join(new_filename.split('/')[:-1]))
    else:
        tmp_directory = 'temp'
    print 'tmp:', tmp_directory
    if (os.path.exists(tmp_directory)):
        remove_directory(tmp_directory)
    os.makedirs(tmp_directory)
    for zip_filename in zip_filenames:
        print 'unzipping {}'.format(zip_filename)
        unzip(zip_filename, tmp_directory)
    extracted_filenames = ['{}/{}'.format(tmp_directory, filename) for filename in sorted(os.listdir(tmp_directory))]
    print 'extracted_filenames', extracted_filenames
    remove_first_line(extracted_filenames[1:])
    concatenate_files(extracted_filenames, new_filename, True)
    #remove_directory(tmp_directory)
    
def download(url, filename, dst_directory = '.'):
    if (dst_directory != '.') and (not os.path.exists(dst_directory)):
        os.makedirs(dst_directory)
    wget = Popen(['/usr/bin/wget', '-O', '{}/{}'.format(dst_directory.rstrip('/'),filename), url], stdout=PIPE, stderr=STDOUT)
    stdout, nothing = wget.communicate()
    if '404' in stdout:
        print 'Got 404 for {}'.format(url)
        rm_command = 'rm {}'.format('{}/{}'.format(dst_directory.rstrip('/'),filename))
        os.system(rm_command)
    
