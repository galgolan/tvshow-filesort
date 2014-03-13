#!/usr/bin/python

import os      
import re
import shutil
import logging

# completed downloads dir
download_dir = '/storage/tvshows'
# sorted tv shows dir
sorted_dir = '/storage/media/Storage/TV Shows'

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',filename='/storage/downloads/filesort.log',level=logging.DEBUG)

extensions = ['3gp', 'avi', 'bdvm', 'flv', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'mts', 'wmv']

errors = False

if not os.path.exists(download_dir):
    logging.error('download_dir doesnt exist')
    errors = True
    
if not os.path.exists(sorted_dir):
    logging.error('sorted_dir doesnt exist')
    errors = True
    
if errors:
    exit(1)
    
logging.info('Searching: ' + download_dir + '...')
fileCounter = 0
for root, dirs, files in os.walk(download_dir):
    for dir in dirs:
        # extract show name and season number
        tv = re.findall(r"""(.*)S(\d{1,2})""", dir, re.IGNORECASE)
        show_name = tv[0][0].replace('.',' ').rstrip()
        season = tv[0][1]        
        logging.info('Processing ' + show_name + ', season: ' + season)
        
        # find or create the target directory
        show_target_dir = os.path.join(sorted_dir, show_name)
        if not os.path.exists(show_target_dir):
            logging.debug('creating directory: ' + show_target_dir)
            os.mkdir(show_target_dir)
            # TODO: place tvshow.nfo file with link to thetvdb.com

        # now move all files in sub directory (which match a filter) to target directory            
        # delete files which are left over
        current = os.path.join(root, dir)
        logging.debug('Processing season dir: ' + dir)
        for root2, dirs2, files2 in os.walk(current):
            for file in files2:
                extension = os.path.splitext(file)[1].replace('.','')
                if extension in extensions:
                    # move the file
                    target_file = os.path.join(show_target_dir, file)
                    source_file = os.path.join(root2, file)
                    logging.debug('Copying ' + source_file + ' to ' + target_file)
                    shutil.copyfile(source_file, target_file)
                    fileCounter += 1
                else:
                    logging.debug('ignored: ' + file)
        
        logging.debug('Removing dir: ' + current)
        shutil.rmtree(current)
    
    
logging.info('Finished processing {} files'.format(fileCounter))
exit(0)