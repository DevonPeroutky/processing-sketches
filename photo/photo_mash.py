from math import sqrt

image_names = ["../images/IMG_0903.jpeg", "../images/IMG_0645.jpeg", "../images/IMG_2200.jpeg", "../images/starry_night_full.jpeg", "../images/working-mount-tam.jpeg"]
# image_names = ["../images/IMG_0903.jpeg", "../images/IMG_0645.jpeg", "../images/IMG_2200.jpeg", "../images/working-mount-tam.jpeg"]
# image_names = ["../images/IMG_0903.jpeg", "../images/IMG_0645.jpeg"]
# image_names = ["../images/starry_night_full.jpeg", "../images/working-mount-tam.jpeg", "../images/IMG_2200.jpeg"]
images = None

def setup():
    global images
    size(1000, 1000)
    print(image_names)
    images = [loadImage(image) for image in image_names]
    for image in images:
        image.loadPixels()
    noLoop()

def draw():
    global images
    # 1. Initialize a grid of squares
    # 2. For initial square --> Chose random photo
    # 3. Set pixels of square to be the chosen photo
    # 4. for each nearby squre --> Set the square's pixels to be the pixels of the photo whose corresponding square is more similar in color
    reference_pixel = color(random(256), random(256), random(256))
    print("REFERENCE COLOR ({}, {}, {})".format(red(reference_pixel), green(reference_pixel), blue(reference_pixel)))
    border_thickness = 20

    loadPixels()
    for x in range(width):
        for y in range(height):
            index = y * width + x
            #r if x < border_thickness or y < border_thickness or x > width - border_thickness or y > height - border_thickness:
            #     pixels[index] = reference_pixel
            # else:
            selected_pixel = select_random_pixel(x, y)
            # selected_pixel = select_most_similar_pixel(x, y, reference_pixel)
            # reference_pixel = selected_pixel
            pixels[index] = selected_pixel
    updatePixels()
    print("DONE!")


def select_random_pixel(x, y):
    global images

    # Select Image
    rand = int(random(len(images)))
    # rand = 0
    random_image = images[rand]

    image_index = y * random_image.width + x
    return random_image.pixels[image_index]

def select_most_similar_pixel(x, y, reference_pixel):
    global images
    candidate_pixels = [select_pixel_from_image(img, x, y) for img in images]
    pixel_distances = [calc_pixel_distance(image_pixel, reference_pixel) for image_pixel in candidate_pixels]
    most_similar_pixel_index = pixel_distances.index(min(pixel_distances))
    return candidate_pixels[most_similar_pixel_index]

def select_pixel_from_image(image, x, y):
    image_index = y * image.width + x
    return image.pixels[image_index]

def calc_pixel_distance(pixelA, pixelB):
    labcolorA = rgb2lab((red(pixelA), green(pixelA), blue(pixelA)))
    labcolorB = rgb2lab((red(pixelB), green(pixelB), blue(pixelB)))
    return cie94(labcolorA, labcolorB)

# Blindly coppied from https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python
# ...which blindly copied from https://web.archive.org/web/20120502065620/http://cookbooks.adobe.com/post_Useful_color_equations__RGB_to_LAB_converter-14227.html
def rgb2lab_old(inputColor):
   num = 0
   rgb = [0, 0, 0]

   for value in inputColor:
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       rgb[num] = value * 100
       num = num + 1

   xyz = [0, 0, 0,]

   x = rgb [0] * 0.4124 + rgb [1] * 0.3576 + rgb [2] * 0.1805
   y = rgb [0] * 0.2126 + rgb [1] * 0.7152 + rgb [2] * 0.0722
   z = rgb [0] * 0.0193 + rgb [1] * 0.1192 + rgb [2] * 0.9505
   xyz[0] = round(x,4)
   xyz[1] = round(y,4)
   xyz[2] = round(z,4)

   xyz[0] = float(xyz[0]) / 95.047         # ref_x =  95.047   Observer= 2°, Illuminant= D65
   xyz[1] = float(xyz[1]) / 100.0          # ref_y = 100.000
   xyz[2] = float(xyz[2]) / 108.883        # ref_z = 108.883

   num = 0
   for value in xyz :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       xyz[num] = value
       num = num + 1

   lab = [0, 0, 0]

   l = (116 * xyz[ 1 ]) - 16
   a = 500 * ( xyz[0] - xyz[1] )
   b = 200 * ( xyz[1] - xyz[2] )

   lab[0] = round(l,4)
   lab[1] = round(a,4)
   lab[2] = round(b,4)

   return lab









# Blindly copied from https://gist.github.com/fikr4n/368f2f2070e0f9a15fb4
def rgb(x):
    """Convert #[AA]RRGGBB color in integer or string to (r,g,b) tuple
    
    Alpha (AA) component is simply ignored.
    
    rgb(0xff0000ff)
    >>> (0, 0, 255)
    rgb('#ff0000')
    >>> (255, 0, 0)
    """
    
    if isinstance(x, str) and x[0] == '#':
        x = int(x[1:], 16)
    return ((x >> 16) & 0xff, (x >> 8) & 0xff, (x) & 0xff)


def cie94(L1_a1_b1, L2_a2_b2):
    """Calculate color difference by using CIE94 formulae
    
    See http://en.wikipedia.org/wiki/Color_difference or
    http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CIE94.html.
    
    cie94(rgb2lab((255, 255, 255)), rgb2lab((0, 0, 0)))
    >>> 58.0
    cie94(rgb2lab(rgb(0xff0000)), rgb2lab(rgb('#ff0000')))
    >>> 0.0
    """
    
    L1, a1, b1 = L1_a1_b1
    L2, a2, b2 = L2_a2_b2

    C1 = sqrt(_square(a1) + _square(b1))
    C2 = sqrt(_square(a2) + _square(b2))
    delta_L = L1 - L2
    delta_C = C1 - C2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_H_square = _square(delta_a) + _square(delta_b) - _square(delta_C)
    return (sqrt(_square(delta_L)
            + _square(delta_C) / _square(1.0 + 0.045 * C1)
            + delta_H_square / _square(1.0 + 0.015 * C1)))


def rgb2lab(R_G_B):
    """Convert RGB colorspace to Lab
    
    Adapted from http://www.easyrgb.com/index.php?X=MATH.
    """
    
    R, G, B = R_G_B
    
    # Convert RGB to XYZ
    
    var_R = ( R / 255.0 )        # R from 0 to 255
    var_G = ( G / 255.0 )        # G from 0 to 255
    var_B = ( B / 255.0 )        # B from 0 to 255

    if ( var_R > 0.04045 ): var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_R = var_R / 12.92
    if ( var_G > 0.04045 ): var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_G = var_G / 12.92
    if ( var_B > 0.04045 ): var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    
    # Convert XYZ to L*a*b*
    
    var_X = X / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    var_Y = Y / 100.000        # ref_Y = 100.000
    var_Z = Z / 108.883        # ref_Z = 108.883

    if ( var_X > 0.008856 ): var_X = var_X ** ( 1.0/3.0 )
    else:                    var_X = ( 7.787 * var_X ) + ( 16.0 / 116.0 )
    if ( var_Y > 0.008856 ): var_Y = var_Y ** ( 1.0/3.0 )
    else:                    var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )
    if ( var_Z > 0.008856 ): var_Z = var_Z ** ( 1.0/3.0 )
    else:                    var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116.0 )

    CIE_L = ( 116.0 * var_Y ) - 16.0
    CIE_a = 500.0 * ( var_X - var_Y )
    CIE_b = 200.0 * ( var_Y - var_Z )
    return (CIE_L, CIE_a, CIE_b)


def _old_rgb2lab(R_G_B):
    """Old implementation of rgb2lab, the result is strange :D
    
    Adapted from http://www.f4.fhtw-berlin.de/~barthel/ImageJ/ColorInspector//HTMLHelp/farbraumJava.htm.
    """
    
    R, G, B = R_G_B

    # http://www.brucelindbloom.com

    # float: r, g, b, X, Y, Z, fx, fy, fz, xr, yr, zr
    # float: Ls, as_, bs
    eps = 216.0/24389.0
    k = 24389.0/27.0

    Xr = 0.964221  # reference white D50
    Yr = 1.0
    Zr = 0.825211

    # RGB to XYZ
    r = R/255.0 #R 0..1
    g = G/255.0 #G 0..1
    b = B/255.0 #B 0..1
    
    if not (0<=r<=1 and 0<=g<=1 and 0<=b<=1):
        raise ValueError('RGB out of 0..255 range')

    # assuming sRGB (D65)
    if r <= 0.04045:
        r = r/12
    else:
        r = ((r+0.055)/1.055) ** 2.4

    if g <= 0.04045:
        g = g/12
    else:
        g = ((g+0.055)/1.055) ** 2.4

    if b <= 0.04045:
        b = b/12
    else:
        b = ((b+0.055)/1.055) ** 2.4

    X =  0.436052025*r     + 0.385081593*g + 0.143087414 *b
    Y =  0.222491598*r     + 0.71688606 *g + 0.060621486 *b
    Z =  0.013929122*r     + 0.097097002*g + 0.71418547  *b

    # XYZ to Lab
    xr = X/Xr
    yr = Y/Yr
    zr = Z/Zr

    if xr > eps:
        fx =  xr ** (1.0/3.0)
    else:
        fx = (k * xr + 16.0) / 116.0

    if yr > eps:
        fy =  yr ** (1.0/3.0)
    else:
        fy = (k * yr + 16.0) / 116.0

    if zr > eps:
        fz =  zr ** (1.0/3.0)
    else:
        fz = (k * zr + 16.0) / 116.0

    Ls = ( 116 * fy ) - 16
    as_ = 500*(fx-fy)
    bs = 200*(fy-fz)

    return (int(2.55*Ls + 0.5), # L
            int(as_ + 0.5),     # a
            int(bs + 0.5))      # b


def _square(x):
    return x * x
