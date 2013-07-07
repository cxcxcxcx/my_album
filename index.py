#!/usr/bin/python2
import json
import os
import sys
from bottle import Bottle, run, static_file
from bottle import SimpleTemplate
import bottle

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

JB_PATH = os.path.join(CURRENT_PATH, 'static/')
TEMPLATE_PATH = os.path.join(CURRENT_PATH, 'template/')
#JB_PATH = CURRENT_PATH
PHOTO_PATH = None

app = Bottle()

albums = None


def _get_template(file_name):
    return open(os.path.join(TEMPLATE_PATH, file_name), 'r').read()


@app.get('/static/jbcore/<filepath:path>')
def jbcore_static_files(filepath):
    return static_file(filepath, JB_PATH + 'jbcore/')


@app.get('/photo/<filepath:path>')
def photo_files(filepath):
    return static_file(filepath, PHOTO_PATH)


@app.get('/album/<album:path>/')
def static_index(album):
    template = SimpleTemplate(source=_get_template('index.html'))
    return template.render(title=album)


class Photo(object):
    pass


@app.get('/')
def all_albums():
    sorted_albums = sorted(
        albums.keys(),
        key=lambda x: albums[x]['published'],
        reverse=True)
    template = SimpleTemplate(source=_get_template('list.html'))
    return template.render(albums=sorted_albums)


@app.get('/album/<album:path>/config.xml')
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

    template = SimpleTemplate(source=_get_template('xml_template.xml'))
    return template.render(album_title=album, photos=photos)


if __name__ == '__main__':
    PHOTO_PATH = sys.argv[1]
    albums = json.load(open('%s/data.json' % PHOTO_PATH, 'r'))
    if len(sys.argv) > 2:
        from flup.server.fcgi import WSGIServer
        WSGIServer(app).run()
    else:
        run(app, host='0.0.0.0', port=8000)
