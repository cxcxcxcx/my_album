import json
import os
import sys
from bottle import Bottle, run, static_file
from bottle import SimpleTemplate

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

JB_PATH = os.path.join(CURRENT_PATH, 'static/')
#JB_PATH = CURRENT_PATH
PHOTO_PATH = None

app = Bottle()

albums = None


@app.get('/static/jbcore/<filepath:path>')
def jbcore_static_files(filepath):
    return static_file(filepath, JB_PATH + 'jbcore/')


@app.get('/photo/<filepath:path>')
def photo_files(filepath):
    return static_file(filepath, PHOTO_PATH)


@app.get('/album/<album>/')
def static_index(album):
    return static_file('index.html', JB_PATH)


class Photo(object):
    pass


@app.get('/albums/')
def all_albums():
    template = SimpleTemplate("""
        <html>
            <ul>
            % for album in albums:
              <li><a href="/album/{{album}}/">
                <img src="/photo/thumbnail/picasa/{{album}}/__album.jpg" />
                {{album}}
              </a></li>
            % end
            </ul>
        </html>""")
    return template.render(albums=albums.keys())


@app.get('/album/<album>/config.xml')
def list_album(album):
    album_dict = albums[album]
    photos = []
    for i in album_dict['photos']:
        photo = Photo()
        photo_path = '/picasa/%s/%s.jpg' % (album, i['name'])
        photo.image_url = '/photo/%s' % photo_path
        photo.thumb_url = '/photo/thumbnail/' + photo_path
        photo.title = ''
        photo.caption = i.get("summary", "")
        photos.append(photo)

    template = SimpleTemplate(source=open('xml_template.xml', 'r').read())
    return template.render(album_title=album, photos=photos)


if __name__ == '__main__':
    PHOTO_PATH = sys.argv[1]
    albums = json.load(open('%s/data.json' % PHOTO_PATH, 'r'))
    run(app, port=8000)
