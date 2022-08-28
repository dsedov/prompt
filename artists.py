import os, csv

def load_list(artist_list_file = "artist_list.txt", rel_path=True):

    artists = []

    if rel_path : file_path = os.path.join(os.path.dirname(__file__), artist_list_file)
    else : file_path = artist_list_file

    print(f"Loading {file_path}")
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            artist = {}
            artist["name"] = row[0].strip()
            artists.append(artist)
    return artists 
def sanitize_for_filename(name):
    return keep_only_ascii(name).replace(' ', '_').replace('.','_').replace(',','_')
def keep_only_ascii(string):
    return string.replace('á', 'a').replace('ü', 'u').replace('é', 'e').replace('ö', 'o').replace('è', 'e').replace('í', 'i').replace('ä','a').replace('ã','a').replace('ó','o')
def check_image_existance(artist_name, folder):
    files = os.listdir(folder)
    for f in files:
        if keep_only_ascii(f).startswith(sanitize_for_filename(artist_name)):
            return True
    return False 
def get_filename(artist_name, folder):
    files = os.listdir(folder)
    for f in files:
        if keep_only_ascii(f).startswith(sanitize_for_filename(artist_name)):
            return f
    return None 
def names(filter = None):
    names = []
    all_artists = load_list()
    for artist in all_artists:
        if callable(filter):
            if filter(artist):
                names.append(artist["name"])
        else : names.append(artist["name"])

    return names 