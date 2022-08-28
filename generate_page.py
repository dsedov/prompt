from PIL import Image 
import artists, settings, os
from yattag import Doc
doc, tag, text = Doc().tagtext()

root_folder = settings.root_folder()
dist_folder = settings.dist_folder()
dist_image_storage = os.path.join(dist_folder, 'images')
dist_html = os.path.join(dist_folder, 'images.html')

os.makedirs(dist_image_storage, exist_ok=True)
names = artists.names()

with tag('html'):
    with tag('head'):
        with tag('style', type='text/css'):
            text('* {box-sizing: border-box;}')
            text('body {padding: 30px;}')
            text('img {width:100%; padding:20px;}')
            text('h2 {margin-left:30px;margin-bottom:0px;padding-bottom:0px;}')
            text('h4 {margin-left:30px;margin-top:0px;}')
            text('.image_container {background-color:#ffffff; width:50%; float:left;}')
            text('.unfiled {background-color:#ff4444; width:50%; float:left;}')
            text('.bad {opacity: 0.5;background-color:#444444; width:50%; float:left;}')
            text('.bad:* {opacity: 0.5}')
    with tag('body'):
        total_artists = 0
        described_artists = 0
        for artist in names:
            artist_name = artist["name"]
            total_artists += 1

            artist_file = artists.get_filename(artist_name, root_folder)
            try:
                img = Image.open(os.path.join(root_folder, artist_file))
                dist_file_name = f"{artists.sanitize_for_filename(artist_name)}.jpg"
                img.save(os.path.join(dist_image_storage, dist_file_name), quality=90)
                print(artist_file)

                with tag('div', klass='image_container'):
                    if 'unknown' in artist["tags"]:
                        doc.attr(klass = "image_container, unfiled")
                        described_artists += 1
                    if 'bad' in artist["tags"]:
                        doc.attr(klass = "bad")
                    with tag('h2'):
                        text(artists.keep_only_ascii(artist_name))
                    with tag('h4'):
                        text(' '.join(artist["tags"]))
                    doc.stag('img', src=f"images/{dist_file_name}")
            except:
                print(f"ERROR: {artist_name} ") 
        text(f"Artists with description {total_artists-described_artists}/{total_artists}")
result = doc.getvalue()
with open( dist_html, "w") as file:
    file.write(result)