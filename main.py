import cv2
import numpy as np 

def change_brightness( img, value=0):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor( final_hsv, cv2.COLOR_HSV2BGR)
    return img

def change_contrast( img, contrast=0):
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        img = cv2.addWeighted( img, alpha_c, img, 0, gamma_c)

    return img

def change_size(img,scale_x = 1.5,scale_y=1.5):
    img = cv2.resize( img, None, fx = scale_x, fy = scale_y, interpolation = cv2.INTER_LINEAR)
    return img

def change_angle_of_inclination( img, angle, scale_w = 1.0, scale_h = 1.0):

    (h, w) = img.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D( center, angle, 1.0)
  
    img = cv2.warpAffine( img, rotation_matrix, (int(scale_w*w), int(scale_h*h)))
    return img 

def create_variants( filename, img, func, step = 1, min_dif = -100, max_dif = 100):
    for i in range(min_dif,max_dif + 1,step):
        if i == 0:
            continue

        result = func(img,i)
        path = f"{filename}/{func.__name__}/{filename}_{func.__name__}_{i}.jpg"
        cv2.imwrite(path, result)

def create_size_variants( filename, img, step = 1, min_dif = 1, max_dif = 200):
   for i in range( min_dif, max_dif + 1, step):
        for j in range( min_dif, max_dif + 1, step):
            scale_w = i/100
            scale_h = j/100

            result = change_size( img, scale_w, scale_h)
            if i == 100:
                path = f"{filename}/change_size/scale-w/{filename}_scale_w-{i}_h-{j}.jpg"
                cv2.imwrite( path, result)
            elif j == 100:
                path = f"{filename}/change_size/scale-h/{filename}_scale_w-{i}_h-{j}.jpg"
                cv2.imwrite( path, result)
            elif i > j:
                path = f"{filename}/change_size/scale-w-h/{filename}_scale_w-{i}_h-{j}.jpg"
                cv2.imwrite( path, result)
            elif j > i:
                path = f"{filename}/change_size/scale-h-w/{filename}_scale_w-{i}_h-{j}.jpg"
                cv2.imwrite( path, result)

if __name__ == "__main__": 

    print("Program: Start")

    with open('conf.txt','r') as filenames:
        filenames = filenames.readlines()

    for i in range(len(filenames)):
        filenames[i] = filenames[i].strip()

    for filename in filenames:

        imagename = f"{filename}/{filename}.jpg"
        img = cv2.imread(imagename)

        create_variants(filename,img,change_brightness,step=10,min_dif=100,max_dif=100)

        create_variants(filename,img,change_contrast,step=10,min_dif=100,max_dif=100)

        create_variants(filename,img,change_angle_of_inclination,step=5,min_dif=180,max_dif=180)
        
        create_size_variants(filename,img,step=10,min_dif=50,max_dif=150)
        
    print("Program: End") 
    
        
