from boto.s3.connection import S3Connection

LI_API_KEY = 'AKIAJP3GTHGNEXGI3TZQ'
LI_SECRET_KEY = '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'

conn = S3Connection(LI_API_KEY, LI_SECRET_KEY)
bucket = conn.create_bucket('lialerts')  # creates or retrieves "lialerts" bucket

from boto.s3.key import Key

k = Key(bucket)

import glob
for xml in glob.glob("xml/update_*.xml"):
    print xml
    k.key = xml
    k.set_contents_from_filename(xml)
    raw_input()
