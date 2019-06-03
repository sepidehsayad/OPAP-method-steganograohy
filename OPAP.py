from PIL import Image


host_image = Image.open('baboon512.bmp','r') #open image 
secret_image = Image.open('boat256.bmp','r') #open image


pixel_value_hostimage = list(host_image.getdata()) #we have pixels in this list


pix_val_secret=list(secret_image.getdata())


width, height =host_image.size #size of pic


def pixel_value(list_of_values): #RGB(R,G,B) in gray scale = RGB(X,X,X) so one of them is enough
    pixel_val=[]
    for i in list_of_values:
        pixel_val+=[i[0]]
    return pixel_val


def cal_of_k(size_of_file):
    pixels=host_image.size[0]*host_image.size[1]
    k = int(size_of_file/pixels)
    if 1<= k <= 4 :
        print("k :",k)
        return k #calculate K-LSB (number of pixeles/size_of_file)
    return "PLZ ENTER ANOTHER FILE"


def convert_pixelvalue_to_binary(pixel_val):
    binary_of_pixel_value=[]
    for i in pixel_val:
        binary_of_pixel_value+=['{0:08b}'.format(i)]

    return binary_of_pixel_value

def spilit_value_with_k(string,k):#convert string(secret data) to k slice k slice
    list_k=[]
    for i in range(0,len(string),k):
        list_k+=[string[i:i+k]]
    
    return list_k

def LSB(list_secret_data,list_binary_hostimage,k):
    new_pixels=[]
    count=len(list_binary_hostimage[0])-k
    for i in range(0,len(list_secret_data)):
            temp =list_binary_hostimage[i][0:count]+list_secret_data[i]
            new_pixels+=[temp]
    for j in range(len(list_secret_data),len(list_binary_hostimage)):
        new_pixels +=[list_binary_hostimage[j]]
    
    return new_pixels



def conver_bin_to_decimal(bin_pixles):
    dec_pixels=[]
    for i in bin_pixles:
        dec_pixels+=[int(i,2)]
    return dec_pixels



def calculate_OPAP(binary_pixel_value,lsb_pixels,k_lsb):
    new_pixels=[]
    for i in range(len(binary_pixel_value)):
        d=lsb_pixels[i]-binary_pixel_value[i]
        if -2**k_lsb < d <2**k_lsb :
            if (2**(k_lsb-1)<d<2**k_lsb) and (lsb_pixels[i] >= 2**k_lsb) :
                new_pixels +=[lsb_pixels[i]-2**k_lsb]
            elif (-2**k_lsb < d <-(2**k_lsb)) and (lsb_pixels[i] <= (255-2**k_lsb)):
                new_pixels += [lsb_pixels[i]+2**k_lsb]
            else :
                new_pixels +=[lsb_pixels[i]]
        else:
            print("cant calculate")
    return new_pixels



def show_new_picture(dec_pixels):
    img = Image.new('L',(512,512))
    img.putdata(dec_pixels)
    img.save("new_img.bmp")
    img.show()


Pixel_val_secret =pixel_value(pix_val_secret)
binary_pixel_values_secret=convert_pixelvalue_to_binary(Pixel_val_secret)
print(binary_pixel_values_secret[0:30])
pixel_val =[]
f_sec_pix='' 
for i in range(len(binary_pixel_values_secret)) :
    f_sec_pix +=binary_pixel_values_secret[i]


pixel_val = pixel_value(pixel_value_hostimage)
binary_pixel_values=convert_pixelvalue_to_binary(pixel_val)
string_scret_data= f_sec_pix

k_lsb=cal_of_k(len(string_scret_data))

k_slicee_k_slicee_scret_data =spilit_value_with_k(string_scret_data,k_lsb)

lsb_pixels =LSB(k_slicee_k_slicee_scret_data,binary_pixel_values,k_lsb)


dec_lsb_pixels=conver_bin_to_decimal(lsb_pixels)

opap_pixels=calculate_OPAP(pixel_val,dec_lsb_pixels,k_lsb)

show_new_picture(opap_pixels)



