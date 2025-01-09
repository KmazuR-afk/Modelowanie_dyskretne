import inspect

from lab_1.main import binarize
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def on_key(event):
    if event.key == 'escape':  # Check if the Esc key is pressed
        plt.close()
def dilate(img,r,disp=True):
    height, width = img.shape
    dilated=img.copy()
    if disp:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event',on_key)

    for i in range(height):
        for j in range(width):
            if (img[i, j] == 0):
                if i in [r,height-r-1]:
                    if j in [r,width-r-1]:
                        dilated[i-r:i+r+1,j-r:j+r+1]=0
                    else:
                        dilated[i-r:i+r+1,j-r:j+r+1]=0
                else:
                    if j in [r,width-r-1]:
                        dilated[i-r:i+r+1,j-r:j+r+1]=0
                    else:
                        dilated[i-r:i+r+1,j:j+r+1]=0
            else:
                if dilated[i,j] ==255:
                    dilated[i,j]=img[i,j]
        if disp:
            ax.clear()
            ax.imshow(dilated, cmap='gray')
            ax.axis('off')
            plt.pause(1e-10)
            ax.clear()

    if inspect.stack()[1].function=='main':
        if disp:
            ax.imshow(dilated, cmap='gray')
            ax.axis('off')
            plt.show()
            while plt.fignum_exists(fig.number):
                plt.pause(0.000000000001)

        dilated=Image.fromarray(dilated)
        dilated.save('dilated.bmp')
    return np.array(dilated)
def erode(img,r,disp=True):
    height, width = img.shape
    eroded = img.copy()
    if disp==True:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', on_key)
    for i in range(height):
        for j in range(width):
            if (img[i, j] == 255):
                if i in [r, height - (r+1)]:
                    if j in [r, width - (r+1)]:
                        eroded[i - r:i + (r+1), j - r:j + (r+1)] = 255
                    else:
                        eroded[i - r:i + (r+1), j-r:j + (r+1)] = 255
                else:
                    if j in [r, width - (r+1)]:
                        eroded[i-r:i + (r+1), j - r:j + (r+1)] = 255
                    else:
                        eroded[i-r:i + r+1, j-r:j + r+1] = 255
            else:
                if eroded[i, j] == 0:
                    eroded[i, j] = img[i, j]
        if disp==True:
            ax.clear()  # Clear the previous image
            ax.imshow(eroded, cmap='gray')  # Show the updated image
            ax.axis('off')  # Turn off axis
            plt.pause(1e-10)
    if inspect.stack()[1].function == 'main':
        if disp == True:
            ax.imshow(eroded, cmap='gray')
            ax.axis('off')
            plt.show()
            while plt.fignum_exists(fig.number):
                plt.pause(0.000000000001)

        eroded = Image.fromarray(eroded)
        eroded.save('eroded.bmp')
    return np.array(eroded)

def opening(img,r,disp=True):
    open = erode(img,r,False)
    open = dilate(open,r,False)
    if disp==True:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', on_key)
        ax.imshow(open, cmap='gray')
        ax.axis('off')
        plt.show()
        while plt.fignum_exists(fig.number):
            plt.pause(0.000000000001)

    open = Image.fromarray(open)
    open.save('open.bmp')
    return np.array(open)

def closing(img,r,disp=True):
    close = dilate(img, r,False)
    close = erode(close, r,False)
    if disp == True:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', on_key)
        ax.imshow(close, cmap='gray')
        ax.axis('off')
        plt.show()
        while plt.fignum_exists(fig.number):
            plt.pause(0.000000000001)

    close = Image.fromarray(close)
    close.save('close.bmp')
    return np.array(close)


def G_M(radius, sigma):
    size = 2 * radius + 1  # Zmienna 'size' określa rozmiar maski
    kernel = np.zeros((size, size), np.float64)  # Tworzymy pustą maskę o rozmiarze size x size
    norm_factor = 1 / (2 * np.pi * sigma ** 2)  # Współczynnik normalizacyjny

    # Wypełniamy maskę Gaussa
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            kernel[i + radius, j + radius] = norm_factor * np.exp(-(i ** 2 + j ** 2) / (2 * sigma ** 2))

    # Normalizacja maski, aby suma elementów wynosiła 1
    kernel /= np.sum(kernel)
    return kernel


def c_convovle(img,mask,disp=True):
    h,w=img.shape
    k_size=mask.shape[0]
    pad_s=k_size//2
    pad_img=np.pad(img,pad_s, mode='constant', constant_values=0)
    ret=img.copy()
    if disp:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', on_key)
    for i in range(h):
        for j in range(w):
            region=pad_img[i:i+k_size,j:j+k_size].copy()
            ret[i,j]=np.sum(region*mask)
        if (disp == True):
            ax.clear()
            ax.imshow(ret, cmap='gray')
            ax.axis('off')
            plt.pause(1e-100)
            ax.clear()

    if disp:
        ax.imshow(ret, cmap='gray')
        ax.axis('off')
        plt.show()
        while plt.fignum_exists(fig.number):
            plt.pause(0.000000000001)

    sploted = Image.fromarray(ret)
    sploted.save('sploted.bmp')

    return ret

def splot(img,mask=None,disp=True):
    if mask is None:
        size=int(input("Podaj promień maski: "))
        mask=G_M(size,1.0)
    else:
        size=mask.shape[0]
    c_img=c_convovle(img,mask,disp)
    return c_img

def main():
    img=np.array(Image.open("./zdj.bmp"))
    img=np.array(binarize(5,img))
    rad=int(input("Podaj promień sąsiedztwa operacji morfologicznych: "))
    #dilate(img,rad,True)
    #erode(img,rad,True)
    mask=np.loadtxt('./gor_5x5',delimiter=' ')
    #opening(img,rad)
    #closing(img,rad)
    splot(img)

main()