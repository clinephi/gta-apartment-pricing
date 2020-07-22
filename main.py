import pandas as pd
import training_functions as train_funcs  #custom built train(), get_accuracy() etc.
import models as arch
import data_processing as data_funcs
from data_analytics import create_imageset

# IMPORT OUR DATA, PREPROCESS, TRAIN :
clean_ads = pd.read_csv( "ads_cleaned.csv" )
"""
ads = pd.read_csv ( "consolidated_raw_ads.csv" )
ads_dups_removed = ads.drop_duplicates( ["title", "address", "unit_type", "Bedrooms", "Bathrooms", "Lat", "Lon", "SQFT", "Price" ], keep= "first")
"""
# Gather some statistics about our dataset.
"""
print ("Duplicates removed:", len(ads.index ) - len( ads_dups_removed.index) )
print ("Entries remaining:", len(ads_dups_removed.index))
"""

#print ( ads['bedrooms'] )
"""
print( ads.groupby(["Bedrooms"]).count() )
print ( "min price per month:", ads["Price"].min() )
ads_dups_removed.to_csv( "ads_cleaned.csv", index = False )
lookup = ads.loc[ ads["Price"] == 111.0 ]
print ( lookup["title"].values[0].replace(" ", "") )
"""

# Try to train our autoencoder on images
imgs = create_imageset( clean_ads )
for i, img in enumerate(imgs):
    if i>4:
        break
    else:
        print (img)