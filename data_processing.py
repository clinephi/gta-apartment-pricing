import pandas as pd
import numpy as np
from sklearn import preprocessing
import torch
import torch.utils.data

def preprocess_data ( ads, batch_size = 5  ):
    # ads: pd dataframe of scraped ads.

    # Partition into labels and data
    ads_numerical_data = ads.loc[:, 'bedrooms':'bike_score']  # data to learn from
    ads_labels = ads["price"]   # price is our label to learn.

    # Convert to floats
    numerical_data = ads_numerical_data.astype( "float64" )
    labels = ads_labels.astype( "float64" )

    # Normalize data  TODO: clean this up with sklearn.
    numerical_data["bedrooms"] = (numerical_data["bedrooms"] - numerical_data["bedrooms"].min()) / (
    numerical_data["bedrooms"].max() - numerical_data["bedrooms"].min())  # normalize bedrooms
    numerical_data["bathrooms"] = (numerical_data["bathrooms"] - numerical_data["bathrooms"].min()) / (
    numerical_data["bathrooms"].max() - numerical_data["bathrooms"].min())  # normalize bathrooms
    numerical_data["apartment_lat"] = (numerical_data["apartment_lat"]/100)
    numerical_data["apartment_lon"] = (numerical_data["apartment_lon"]/100)
    numerical_data["sqft"] = (numerical_data["sqft"] - numerical_data["sqft"].min()) / (numerical_data["sqft"].max() - numerical_data["sqft"].min())  # normalize sqft
    numerical_data["walk_score"] = (numerical_data["walk_score"] - numerical_data["walk_score"].min()) / (
    numerical_data["walk_score"].max() - numerical_data["walk_score"].min())  # normalize walk_score
    numerical_data["transit_score"] = (numerical_data["transit_score"] - numerical_data["transit_score"].min()) / (
    numerical_data["transit_score"].max() - numerical_data["transit_score"].min())  # normalize transit_score
    numerical_data["bike_score"] = (numerical_data["bike_score"] - numerical_data["bike_score"].min()) / (
    numerical_data["bike_score"].max() - numerical_data["bike_score"].min())  # normalize transit_score

    # Normalize labels TODO: normalize price for faster convergence ?
    #labels= (labels- labels.min()) / (labels.max() - labels.min())

    # Convert to tensors.
    data_tensor = torch.Tensor( numerical_data.values)
    label_tensor = torch.Tensor( labels.values )

    # Create loaders:
    dataset = torch.utils.data.TensorDataset( data_tensor, label_tensor )
    train_loader = torch.utils.data.DataLoader( dataset, batch_size = batch_size, shuffle = True )

    return train_loader
