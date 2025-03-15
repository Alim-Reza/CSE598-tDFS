import numpy as np

class CustomTensor:
    def __init__(self, data, dtype=None, device='cpu'):
        if isinstance(data, (list, tuple, np.ndarray)):
            self.data = np.array(data, dtype=dtype)
        else:
            self.data = np.array([data], dtype=dtype)
        self.device = device
        self.requires_grad = False
        self.grad = None
        self._shape = self.data.shape
        self._dtype = self.data.dtype

    @property
    def shape(self):
        return self._shape

    @property
    def dtype(self):
        return self._dtype

    def to(self, device):
        self.device = device
        return self

    def numpy(self):
        return self.data

    def backward(self, gradient=None):
        if not self.requires_grad:
            raise RuntimeError("Can't call backward on a tensor that doesn't require gradients")
        if gradient is None:
            gradient = np.ones_like(self.data)
        self.grad = gradient

    def __add__(self, other):
        if isinstance(other, CustomTensor):
            return CustomTensor(self.data + other.data)
        return CustomTensor(self.data + other)

    def __mul__(self, other):
        if isinstance(other, CustomTensor):
            return CustomTensor(self.data * other.data)
        return CustomTensor(self.data * other)

    def __getitem__(self, idx):
        return CustomTensor(self.data[idx])

    def __repr__(self):
        return f"CustomTensor({self.data}, device='{self.device}')"

    def reshape(self, *shape):
        return CustomTensor(self.data.reshape(shape))

    def squeeze(self, dim=None):
        if dim is None:
            return CustomTensor(self.data.squeeze())
        return CustomTensor(self.data.squeeze(axis=dim))

    def unsqueeze(self, dim):
        return CustomTensor(np.expand_dims(self.data, axis=dim))

    def mean(self, dim=None):
        if dim is None:
            return CustomTensor(self.data.mean())
        return CustomTensor(self.data.mean(axis=dim))

    def sum(self, dim=None):
        if dim is None:
            return CustomTensor(self.data.sum())
        return CustomTensor(self.data.sum(axis=dim))

    def detach(self):
        return CustomTensor(self.data.copy())

    @staticmethod
    def zeros(*size):
        return CustomTensor(np.zeros(size))

    @staticmethod
    def ones(*size):
        return CustomTensor(np.ones(size))

    @staticmethod
    def randn(*size):
        return CustomTensor(np.random.randn(*size))