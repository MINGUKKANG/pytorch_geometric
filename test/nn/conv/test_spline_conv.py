import torch
from torch_geometric.nn import SplineConv


def test_spline_conv():
    in_channels, out_channels = (16, 32)
    edge_index = torch.tensor([[0, 0, 0, 1, 2, 3], [1, 2, 3, 0, 0, 0]])
    num_nodes = edge_index.max().item() + 1
    x = torch.randn((num_nodes, in_channels))
    pseudo = torch.rand((edge_index.size(1), 3))

    conv = SplineConv(in_channels, out_channels, dim=3, kernel_size=5)
    assert conv.__repr__() == 'SplineConv(16, 32, dim=3)'
    out = conv(x, edge_index, pseudo)
    assert out.size() == (num_nodes, out_channels)

    jit_conv = conv.jittable(x=x, edge_index=edge_index, pseudo=pseudo)
    jit_conv = torch.jit.script(jit_conv)
    assert jit_conv(x, edge_index, pseudo).tolist() == out.tolist()
