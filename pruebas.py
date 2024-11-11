import os

pth = 'C:/camilo/trabajo_de_grado/pcs/image_datasets/monumento_summarized_3/'

imgs = os.listdir(pth)
"""
# Para borrar
delete = False
for img in imgs:
    path_img = pth+img
    
    if delete == True:
        os.remove(path_img)
        delete = False
    elif delete == False:
        delete = True
"""


#Para renombrar
for index, img in enumerate(imgs):
    path_img    = pth+img
    rename      = f'{index}.jpg'
    path_rename = pth+rename
    os.rename(path_img , path_rename)



