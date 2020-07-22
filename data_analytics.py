import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.request import urlopen
from io import BytesIO
from PIL import Image
import numpy as np
from skimage.transform import rescale, resize, downscale_local_mean

# CALCULATE SOME DATA STATISTICS FOR OUR CLEANED ADS
clean_ads = pd.read_csv( "ads_cleaned.csv" )
# print ( clean_ads.head() )
print ( clean_ads.columns )

# Plot a histogram of ppb values
clean_ads["ppb"] = clean_ads["Price"] / clean_ads["Bedrooms"]
ppb_hist = clean_ads.hist( column = ["ppb"], bins = 1000 )
#plt.show()
# From review here, it looks like anything less than $500/bedroom should probably be tossed out.

# Check out correlations for price and variables:
c = clean_ads.corr()
c = pd.DataFrame ([c["Price"]], columns = c.columns )
sns.heatmap(c, annot=True , square=True)
plt.show()

# Loop over image links and show values:
def create_imageset( clean_ads ):
    img_links = clean_ads.loc[:, "img_1":"img_3"]
    imgs = []
    for index, row in img_links.iterrows():
        try:
            print ( index )
            if isinstance(row["img_1"], str) and  isinstance(row["img_2"], str) and isinstance(row["img_3"], str):
                i1 = Image.open(BytesIO(urlopen(row["img_1"]).read()))
                i1 = i1.resize( (250,250) )

                i2 = Image.open(BytesIO(urlopen(row["img_2"]).read()))
                i2 = i2.resize ((250,250))

                i3 = Image.open(BytesIO(urlopen(row["img_3"]).read()))
                i3 = i3.resize ((250,250))

                imgs.append(
                    [i1, i2, i3]
                )
        except:
            pass

    return imgs




