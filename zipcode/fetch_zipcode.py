import requests
import zipfile
import path
import os
from io import BytesIO
from functools import reduce


def download_file(url: str) -> str:
    fname = url.split('/')[-1]
    epost_req = requests.get(url, stream=True)
    with open(fname, 'wb') as f:
        for chunk in epost_req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return fname


def download_zip_to_memory(url: str) -> zipfile.ZipFile:
    epost_req = requests.get(url)
    z_file = zipfile.ZipFile(BytesIO(epost_req.content))
    return z_file


def extract_file(zip_file: str, file_name: str, dest: str):
    f = open(dest, 'wb')
    f.write(zip_file.read(file_name))
    f.close()


def extract_zip(zip_file: str, data_dir: str):
    for file_name in zip_file.namelist():
        if len(file_name) == 0 or file_name[-1] == '/':
            continue
        bstr = bytes(file_name, 'cp437')
        d_file_name = bstr.decode('cp949')
        data_file_path = d_file_name.split('/')[-1]
        data_path = '{data_dir}/{file_name}'.format(data_dir=data_dir, file_name=data_file_path)
        try:
            extract_file(zip_file, file_name, data_path)
        except IOError:
            dir_path_list = data_path.split('/')[:-1]
            dir_path = reduce(lambda x, y: x+'/'+y, dir_path_list)
            os.makedirs(dir_path)
            extract_file(zip_file, file_name, data_path)
        except zipfile.BadZipFile:
            print('Bad file {bad_file}'.format(d_file_name))


zipfile = download_zip_to_memory(path.EPOST_ALL_URL)
extract_zip(zipfile, path.DATA_PATH)
