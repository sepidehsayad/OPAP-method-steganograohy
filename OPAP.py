from PIL import Image

host_image = Image.open('baboon512.bmp','r') #open image 

file = open('secretdata.txt','r') #file of scret data


pixel_value_hostimage = list(host_image.getdata()) #we have pixels in this list



width, height =host_image.size #size of pic


def pixel_value(list_of_values): #RGB(R,G,B) in gray scale = RGB(X,X,X) so one of them is enough
    pixel_val=[]
    for i in list_of_values:
        pixel_val+=[i[0]]
    return pixel_val




def size_of_file(file):#size of secret data 
    characters = 0
    for line in file:
        characters = characters + len(line)
    return characters



def cal_of_k(size_of_file):
    pixels=host_image.size[0]*host_image.size[1]
    return int(pixels/size_of_file) #calculate K-LSB (number of pixeles/size_of_file)



def convert_pixelvalue_to_binary(pixel_val):
    binary_of_pixel_value=[]
    for i in pixel_val:
        binary_of_pixel_value+=['{0:08b}'.format(i)]

    return binary_of_pixel_value



def list_of_secret_data_k(file):#all the scret data in of string 
        with open("secretdata.txt", "r") as ins:
            array = []
            for line in ins:
                array.append(line.rstrip('\n'))
        my_lst_str = ''.join(map(str,array))
        return my_lst_str



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



#def show_new_picture(dec_pixels):
#    img = Image.new('L', (512, 512))
#    img.putdata(dec_pixels)
#    img.save("new_img.bmp")
#    img.show()


def calculate_OPAP(binary_pixel_value,lsb_pixels,k_lsb):
    new_pixels=[]
    for i in range(len(binary_pixel_value)):
        d=lsb_pixels[i]-binary_pixel_value[i]
        if -2**k_lsb < d <2**k_lsb :
            if 2**(k_lsb-1)<d<2**k_lsb and lsb_pixels[i] >= 2**k_lsb :
                new_pixels +=[lsb_pixels[i]-2**k_lsb]
            if -2**k_lsb < d <-(2**k_lsb) and lsb_pixels[i] <= (255-2**k_lsb):
                new_pixels += [lsb_pixels[i]+2**k_lsb]
            else :
                new_pixels +=[lsb_pixels[i]]
    return new_pixels



def show_new_picture(dec_pixels):
    img = Image.new('RGB',(517,517))
    img.putdata(dec_pixels)
    img.save("new_img.bmp")
    img.show()

        

pixel_val =[]
pixel_val = pixel_value(pixel_value_hostimage)
print("pixel host val",pixel_val[0:30])
char =size_of_file(file)
binary_pixel_values=[]
binary_pixel_values=convert_pixelvalue_to_binary(pixel_val)#####binary e host image
#print("\n pixel value host binary :\n",binary_pixel_values[0:30])#bayad bashe baraye di 
string_scret_data= []
string_scret_data=list_of_secret_data_k(file)
k_lsb=cal_of_k(char)
#k_slicee_k_slicee_scret_data =[]
k_slicee_k_slicee_scret_data =spilit_value_with_k(string_scret_data,k_lsb)
#print("len:",len(k_slicee_k_slicee_scret_data))
#print("\n secret data slice: \n",k_slicee_k_slicee_scret_data[0:30])
lsb_pixels =LSB(k_slicee_k_slicee_scret_data,binary_pixel_values,k_lsb)
#print("\n k-lsb pixel binary :\n",lsb_pixels[0:30])
dec_lsb_pixels=conver_bin_to_decimal(lsb_pixels)
print("\n lsb pixel decimal : \n" ,dec_lsb_pixels[0:30])
#print(dec_lsb_pixels)

#show_new_picture(dec_lsb_pixels)

opap_pixels=[]
opap_pixels=calculate_OPAP(pixel_val,dec_lsb_pixels,k_lsb)
#print(opap_pixels[0:30])
print("len",len(opap_pixels))
show_new_picture(opap_pixels)
