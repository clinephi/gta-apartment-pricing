import pandas as pd
import training_functions as train_funcs  #custom built train(), get_accuracy() etc.
import ann as arch
import data_processing as data_funcs

# IMPORT OUR DATA, PREPROCESS, TRAIN :
ads = pd.read_csv ( "scraped_ads.csv" )

# Gather some statistics about our dataset.
# print ( ads['bedrooms'] )
print( ads.groupby(["bedrooms"]).count() )

print ( "min price per month:", ads["price"].min() )

"""
train_loader = data_funcs.preprocess_data( ads, batch_size= 1 )
model = arch.ANN()
train_funcs.train( model, train_loader, num_epochs=500)

# See our output:
for i, batch in enumerate(train_loader):
    data, label = batch
    print ( data )
    print ( model( data ))

"""