
# Python code to read image
import cv2
import glob
from scipy.cluster import hierarchy
from skycolors import rgb_colors
import math
import pandas as pd

def main():
    folders = glob.glob("images/*")
    imageFolders = []
    vectors = []

    for folder in folders:
        print(folder)
        
        newDir = folder + "/*"
        folderImages = glob.glob(newDir)

        files = []
        for nextFile in folderImages:
            print("\t", nextFile)
            files.append(nextFile)
            vectors.append(vecFromFilename(nextFile))
        
        imageFolders.append(files)

    data  = mergeVectors(vectors)
    outfileName = "colordata_1.csv"#input("enter output file name: ")
    data.to_csv(outfileName)


def mergeVectors(vectors):
    data_dict = {}
    data_dict["filename"] = []
    data_dict["category"] = []

    for c in rgb_colors:
        data_dict[c] = []

    for vec in vectors:
        for key in vec:
            data_dict[key].append(vec[key])

    
    data = pd.DataFrame(data_dict)
    print(data)
    return data



def vecFromFilename(filename):
    colorVec = {}
    colorVec["filename"] = filename
    if "daytime" in filename:
        colorVec["category"] = "daytime"
    elif "sunset" in filename:
        colorVec["category"] = "sunset"
    elif "night" in filename:
        colorVec["category"] = "night"
    else:
        print("color category::Something has gone wrong")

    for c in rgb_colors:
        colorVec[c] = 0

    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    #print(img[0][0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(img[0][0])
    # print(RGB_dist( img[0][0]),rgb_colors["DARK_BLUE"])
    img_width = 720
    img = image_resize(img,width=img_width)
    # Cropping an image
    #img = img[0:img_width, 0:img_width]
    
    for region in img:
        sumDist = 0
        for pixel in region:
            sumDist += (RGB_dist( pixel,rgb_colors["ORANGE"]))
            matchColor = closestColor(pixel,rgb_colors)
            colorVec[matchColor] += 1

        #print("sumDist:",(sumDist/len(region)))

    # df = pd.DataFrame(data=colorVec)
    print(colorVec)
    return colorVec


def closestColor(target, dict):
    minDist = -1
    matchColor = ""

    for color in dict:
        dist = RGB_dist(target,dict[color])
        if (minDist == -1) or (dist < minDist):
            minDist = dist
            matchColor = color

    return matchColor



def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized



def HSV_dist(color1, color2, hue_max=180):
    degreeToRad = (2 * math.pi) / hue_max
    hue1 = color1[0] * degreeToRad
    hue2 = color2[0] * degreeToRad


def RGB_dist(color1, color2=[0,0,0]):
    channels = zip(color1, color2)
    sum_distance_squared = 0
    for c1, c2 in channels:
        sum_distance_squared += (c1 - c2) ** 2
    return math.sqrt(sum_distance_squared) 

main()