import torch
import torch.nn as nn
import torch.nn.functional as F

class TorchDNN(nn.Module):
    """
    DNN to extract posteriors for HMM decoding.

    Parameters:
        input_dim (int): Input feature dimension
        output_dim (int): Number of output classes
        num_layers (int): Number of hidden layers
        batch_norm (bool): Whether to use BatchNorm1d after hidden layers
        hidden_dim (int): Number of neurons per hidden layer
        dropout_p (float): Dropout probability for regularization
    """
    def __init__(
        self, input_dim, output_dim, num_layers=2, batch_norm=True, hidden_dim=256, dropout_p=0.2
    ):
        super(TorchDNN, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.batch_norm = batch_norm
        self.hidden_dim = hidden_dim
        self.dropout_p = dropout_p

        layers = []


        layers.append(nn.Linear(input_dim, hidden_dim))
        if batch_norm:
            layers.append(nn.BatchNorm1d(hidden_dim))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_p))


        for _ in range(num_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            if batch_norm:
                layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_p))

        layers.append(nn.Linear(hidden_dim, output_dim))
        #layers.append(nn.LogSoftmax(dim=-1))  

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)
