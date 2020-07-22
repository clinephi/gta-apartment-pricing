import pandas as pd
import training_functions as train_funcs  #custom built train(), get_accuracy() etc.
import models as arch
import data_processing as data_funcs

# IMPORT OUR DATA, PREPROCESS, TRAIN :
# test = pd.read_csv ( "test.txt", sep='\t' )
# print ( test.drop_duplicates(subset = ["test_col", "test_val"], keep = 'first' ) )
test = "2,000"
print(
    test.replace(",",""),
)