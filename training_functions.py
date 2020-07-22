# util functions:
import torch
import torch.nn as nn
import torch.nn.functional as F

def train(model, train_loader, num_epochs=5, learning_rate=1e-4):
    torch.manual_seed(42)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # train_acc, val_acc = [], []
    # iters, losses = [], []
    for epoch in range(num_epochs):
        for data, labels in train_loader:
            pred = model(data)
            loss = criterion(pred, labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print('epoch {}, loss {}'.format(epoch, loss.item()))
