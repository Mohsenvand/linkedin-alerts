from lxml import etree
import pylab
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.colors import COLOR_SCHEMES
import time
import datetime
import webbrowser
from prettytable import PrettyTable


def parse_update(xml):
    tree = etree.parse(xml)
    updates = tree.xpath('/updates/update')
    update_fields = []
    headlines = ""
    first = True
    x = PrettyTable(['Name', 'Headline', 'Timestamp', 'Human Readable'])
    x.align["Headline"] = 'l'
    for update in updates:
        u = {}
        u['timestamp'] = update.find('timestamp').text
        u['key'] = update.find('update-key').text
        u['type'] = update.find('update-type').text
        update_content = update.find('update-content')
        try:
            person = update_content.find('person')
            person.text
        except:
            person = update_content.find('company-person-update/person')
        u['person_id'] = person.find('id').text
        if first:
            print person.find('first-name').text, ' ',  person.find('last-name').text
            print person.find('headline').text
            person_url = person.find('site-standard-profile-request/url').text
            print person_url, '\n'
            first = False
        if u['type'] == "CONN":
            conn_person = person.find('connections/person')
            headline = conn_person.find('headline')
            if headline is not None:
                # private names have no headlines
                conn_full_name = conn_person.find('first-name').text + ' '
                conn_full_name += conn_person.find('last-name').text
                x.add_row([conn_full_name,
                           headline.text,
                           u['timestamp'],
                           mod_time(u['timestamp'])])
                headline = headline.text
                u['headline'] = headline
                headlines += " " + headline
        update_fields.append(u)
    print x
    if headlines:
        tag_cloud(headlines)
    if update_fields:
        graph(update_fields)
    print '*' * 50
    return update_fields


def parse_contact(xml):
    tree = etree.parse(xml)
    persons = tree.xpath('/connections/person')
    person_fields = []

    for person in persons:
        p = {}
        p['id'] = person.find('id').text
        p['first-name'] = person.find('first-name').text
        p['last-name'] = person.find('last-name').text
        person_fields.append(p)

    return person_fields


def graph_types(types):
    pylab.figure(1, figsize=(6, 6))

    translated_types = {
        'APPS': 'Application Update',     # Ignore
        'APPM': 'Application Update',     # Ignore
        'CMPY': 'Company Follow Updates', # Ignore
        'CONN': 'New Connection',
        'JGRP': 'Joined a group',
        'JOBS': 'Posted a new job',
        'JOBP': 'Job posting update',
        'MSFC': 'Following new company',
        'NCON': 'New Connection',
        'PICU': 'Picture update',
        'PICT': 'Picture update',
        'PRFU': 'Profile update',
        'PRFX': 'Profile update',
        'PROF': 'Profile update',
        'PREC': 'Recommendation update',
        'SVPR': 'Recommendation update',
        'RECU': 'New recommendation',
        'SHAR': 'Shared an item',
        'STAT': 'Status update',
        'VIRL': 'Commented or liked an update',
    }

    labels = [translated_types[k] for k in types.keys()]
    fracs = types.values()

    pylab.pie(fracs, labels=labels,
        autopct='%1.1f%%', shadow=True)

    pylab.title('What is being updated?', bbox={'facecolor': '0.8', 'pad': 5})
    pylab.show()
    #img = "image/pie_%s.png" % (int(time.time()))
    #pylab.open(img, format='png')
    #webbrowser.open(img)


def mod_time(time):
    """
    Convert LinkedIn's epoch time (in ms) to Python datetime

    str (time in ms) --> str (Python formatted datetime)
    """
    t = int(time)
    t = t / 1000.
    epoch_to_date = datetime.datetime.fromtimestamp(t)
    return epoch_to_date.strftime("%a %b-%d-%Y %I:%m %p")


def graph_delta(updates):
    import numpy as np
    import matplotlib

    type_score = {
        'APPS': 1.01,
        'APPM': 1.02,
        'CMPY': 1.03,
        'CONN': 1.04,
        'JGRP': 1.05,
        'JOBS': 1.06,
        'JOBP': 1.07,
        'MSFC': 1.08,
        'NCON': 1.09,
        'PICU': 1.10,
        'PICT': 1.11,
        'PRFU': 1.12,
        'PRFX': 1.13,
        'PROF': 1.14,
        'PREC': 1.15,
        'SVPR': 1.16,
        'RECU': 1.17,
        'SHAR': 1.18,
        'STAT': 1.19,
        'VIRL': 1.20,
    }
    import matplotlib.pyplot as plt

    timestamps = []
    update_types = []

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)

    locator = matplotlib.dates.AutoDateLocator()

    for u in updates:
        timestamp = u.get('timestamp')
        t = datetime.datetime.fromtimestamp(float(timestamp)/1000.)
        timestamps.append(t)

        update_type = u.get('type')
        u = type_score[update_type]
        update_types.append(u)

        #ax.annotate(update_type, (t, u))

    plt.ylim((0.8, 1.5))
    dates = matplotlib.dates.date2num(timestamps)
    plt.plot_date(dates, update_types, '-')

    plt.show()


def graph(updates):
    types = {}
    for u in updates:
        u_type = u.get('type')
        if u_type is not None:
            num_type = types.get(u['type'], 0) + 1
            types[u['type']] = num_type

    graph_types(types)
    #graph_delta(updates)


def tag_cloud(text):
    tags = make_tags(get_tag_counts(text),
                     minsize=10,
                     maxsize=50,
                     colors=COLOR_SCHEMES['audacity'])
    img = "image/cloud_large_%s.png" % (int(time.time()))
    create_tag_image(tags,
                     img,
                     size=(1280, 800),
                     background=(0, 0, 0, 255),
                     rectangular=True)
    webbrowser.open(img)
    raw_input()


if __name__ == "__main__":
    import glob

    xmls = glob.glob('xml/update_*.xml')
    for x in xmls:
        print x
        #parse_update(x)
