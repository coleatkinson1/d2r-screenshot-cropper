# Image control library
from PIL import Image
import time
import glob
import re

adj_thresh = 10 # Amount of adjacent pixels to check
border_color = (68,68,68) # The border color

'''
D2:Resurrected Screenshot Item cropper v0.19
Written by Cole Atkinson (framedump/filogy)
Concept by Daniel Whyte (Zim)

Description:
Determine the bounds for the grey border of item descriptions on hover (excludes equipped items), 
and crop the image around this.

-The program will monitor the current folder for any new image files that are added. (i.e New screenshots that are created)
-The search function will iterate over pixels until it finds the border color. 
-A quick check will be performed to confirm.
-This will define the start of the box.
-Then we will determine the height and width of the box
-Crop the image and save.
'''

# Checks for matching color on adjacent (right) pixels
def check_adj(im, x,y):
    for i in range(adj_thresh):
        col = im.getpixel( (x+i,y) )
        if col != border_color:
            return False
    return True

# Get the height and width of the box starting from 'start' (x,y)
def get_bounds(im, start):
    width = 0
    height = 0
    # Determine width
    for x in range(im.width):
        col = im.getpixel( (start[0]+x,start[1]) )
        if col != border_color:
            width = x
            break
    # Determine height
    for y in range(im.height):
        col = im.getpixel( (start[0],start[1]+y) )
        if col != border_color:
            height = y
            break
    return (width, height)

# Look for the Item Info Box and process the image if found
def search_img(filename):
    im = Image.open(filename)
    top_left = (0,0)
    bounds = (0,0)
    for x in range(im.width):
        for y in range(im.height):
            col = im.getpixel( (x,y) )
            if col == border_color:
                if check_adj(im, x,y):
                    top_left = (x,y)
                    bounds = get_bounds(im, top_left)
                    #print("Found box at position: {},{} with dimensions of {},{}".format(top_left[0],top_left[1],bounds[0],bounds[1]))
                    im1 = im.crop((top_left[0], top_left[1], top_left[0]+bounds[0], top_left[1]+bounds[1]))
                    n_fname = "crp_"+filename # new filename
                    im1.save(n_fname)
                    print("New image saved to: "+n_fname)
                    return
    print("Could not find Item Info Box")


# Monitors for new screenshots, and processes them
def monitor_folder():
    i_files = glob.glob("./*.png") # Initial images in folder
    while True:
        n_files = glob.glob("./*.png") # Current images in folder
        file_diff = list( set(n_files).symmetric_difference(set(i_files)) ) # See if we have any new files
        for file in file_diff:
            if "crp_" in file: # Ignore files that we created
                continue
            print("New file found: "+file)
            filename = re.sub(r'.\\','',file)
            time.sleep(2) # Wait a bit
            search_img(filename)
        i_files = n_files
        time.sleep(5)

# Start this beeeesh
monitor_folder()
