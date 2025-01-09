import inspect
import os
import numpy as np
from PIL import Image

def brighten(percent, bmp,n=0):
    for i in range(bmp.shape[0]):
        for j in range(bmp.shape[1]):
            if 255-(bmp[i , j]+round(bmp[i, j]*percent/100))>0:
                bmp[i, j] += round(bmp[i, j]*percent/100)
            elif bmp[i , j]!=255:
                bmp[i, j] = 255
    if inspect.stack()[1].function=='main':
        print("Do u want to save or display the image?\nY/N\n")
        choice=input()
        if choice=="Y" or choice=="y":
            img=Image.fromarray(bmp)
            print("Do u want to display, save or both?\nD / S / B\n")
            choice = input()
            if choice=="D" or choice=="d":
                img.show()
            else:
                img.save("output-brightening.bmp")
                if choice=="B" or choice=="b":
                    img.show()
    else:
        img = Image.fromarray(bmp)
        name=str(n)+'.bmp'
        img.save(name)


def step_brightening(per,bmp):
    if 10<=per<=20:
        for i in range(3):
            brighten(per, bmp, i)

def binarize(limit,bmp):
    limit = 255 * limit / 100
    bmp = np.where(bmp >= limit, 255, 0).astype(np.uint8)
    img = Image.fromarray(bmp)
    name = 'binarized.bmp'
    img.save(name)

    return img
def main():
    print("Wszystkie naraz (A) tylko 1(1) tylko 2(2) tylko 3(3)\n")
    choice = input()
    path= '../../przyklad_w_paczce/Mapa_MD_no_terrain_low_res_Gray.bmp'
    bmp=np.array(Image.open(os.path.join(path)))
    bmp_backup=bmp

    match choice:
        case "1":
            print("podaj poziom rozjaśnienia pojedyńczego\n")
            per=int(input())
            brighten(per,bmp)
            bmp=bmp_backup
        case "2":
            print("podaj poziom rozjaśnienia 3-krotnego z zakresu 10-20\n")
            per = int(input())
            step_brightening(per, bmp)
            bmp = bmp_backup
        case "3":
            print("podaj poziom binaryzacji\n")
            per = int(input())
            binarize(per, bmp)
        case "a" | "A":
            print("podaj poziom rozjaśnienia pojedyńczego\n")
            per = int(input())
            brighten(per, bmp)
            bmp = bmp_backup
            print("podaj poziom rozjaśnienia 3-krotnego z zakresu 10-20\n")
            per = int(input())
            step_brightening(per, bmp)
            bmp = bmp_backup
            print("podaj poziom binaryzacji\n")
            per = int(input())
            binarize(per, bmp)
    return 0

#main()