import matplotlib.pyplot as plt
from matplotlib import pyplot as mp

def show_image(img, title = "", cmap='gray', file = 'empty'):
    plt.title(title)
    plt.imshow(img, cmap)
    if file not in ['empty']:
        mp.savefig('output_images/' + file + '.jpg', type="jpg", bbox_inches='tight')
    
def show_images(images, columns = 2, colormap='gray', name = 'empty'):
    fig = plt.figure(figsize=(20,10))
    for i, image in enumerate(images):
        subfig = fig.add_subplot(len(images) / columns + 1, columns, i + 1)
        subfig.imshow(image)
    #if name not in ['empty']:
    #     mp.savefig('test_images_output/' + name + '.png', type="png", bbox_inches='tight')

def show_images_side_by_side(image1, image2, title1 ="", title2 = "", cmap='gray', file = 'empty'):
    fig = plt.figure(figsize=(20,10))
    subfig1 = fig.add_subplot(1,2,1)
    subfig1.imshow(image1)
    subfig1.set_title(title1)
    subfig2 = fig.add_subplot(1,2,2)
    subfig2.imshow(image2, cmap)
    subfig2.set_title(title2)
    if file not in ['empty']:
        mp.savefig('output_images/' + file + '.jpg', type="jpg", bbox_inches='tight')
        
def show_images_side_by_side3(image1, image2, image3, title1 ="", title2 = "", title3 = "", cmap='gray'):
    fig = plt.figure(figsize=(20,10))
    subfig1 = fig.add_subplot(1,3,1)
    subfig1.imshow(image1)
    subfig1.set_title(title1)
    subfig2 = fig.add_subplot(1,3,2)
    subfig2.imshow(image2)
    subfig2.set_title(title2)
    subfig3 = fig.add_subplot(1,3,3)
    subfig3.imshow(image3, cmap)
    subfig3.set_title(title3)
    plt.show()