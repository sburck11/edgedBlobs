from PIL import Image, ImageFilter
import matplotlib as mpl
import matplotlib.cm as cm


img=Image.new('RGB', (256, 16), 'white')
toSave=img.load()


# norm = mpl.colors.Normalize(vmin=0, vmax=255)
# cmap = cm.coolwarm
# m = cm.ScalarMappable(norm=norm, cmap=cmap)


for i in range(256):
	for j in range(16):
		norm_tup = cm.coolwarm(i)#m.to_rgba(i)#/255.0)
		reg = (int(norm_tup[0]*255), int(norm_tup[1]*255), int(norm_tup[2]*255))
		print reg
		toSave[i, j] = reg

img.save("/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1/shadeTest.png")

# red = 
# green = -6.0e-6*x^6 + 0.0006 * x^5 - 0.0216 * x^4 
# blue = -3.0e-5*x^5 + 0.0031*x^4 - 0.0906 * x^3 + 0.2982 * x^2 + 10.678 * x + 181.92

# http://www.kennethmoreland.com/color-maps/
# mat plot lib diverging coolwarm colormap
# http://www.kennethmoreland.com/color-maps/ColorMapsExpanded.pdf
