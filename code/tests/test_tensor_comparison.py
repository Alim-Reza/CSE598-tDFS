import unittest
import torch
import numpy as np
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# sys.path.insert(0, 'e:\\CSE598-tDFS\\code')

from src.pickle_tensor import PickleTensor

class TestTensorComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup test data directory
        cls.directory = os.path.join('data', 'processed', 'video_chunks')
        cls.target_shape = (100, 360, 640, 3)
        
        # Load pickle tensor
        cls.order_func = lambda x: int(x.split('_')[-1].split('.')[0])
        cls.transform_func = lambda x: [frame.astype('float32') / 255.0 for frame in x]
        
        cls.pickle_tensor = PickleTensor.load_from_pickles(
            directory=cls.directory,
            target_shape=cls.target_shape,
            order_by=cls.order_func,
            transform=cls.transform_func
        )
        
        # Convert to PyTorch tensor - access the numpy array directly
        cls.torch_tensor = torch.from_numpy(cls.pickle_tensor.numpy())

    def test_basic_properties(self):
        """Test basic tensor properties"""
        self.assertEqual(self.pickle_tensor.shape, tuple(self.torch_tensor.shape))
        self.assertAlmostEqual(self.pickle_tensor.min().item(), self.torch_tensor.min().item(), places=5)
        self.assertAlmostEqual(self.pickle_tensor.max().item(), self.torch_tensor.max().item(), places=5)
        self.assertAlmostEqual(self.pickle_tensor.mean().item(), self.torch_tensor.mean().item(), places=5)

    def test_all_slicing_types(self):
        """Test all slicing types shown in main.py"""
        
        # Basic indexing
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[0],
            self.torch_tensor[0].numpy()
        )
        
        # Range slicing
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[:5],
            self.torch_tensor[:5].numpy()
        )
        
        # Strided slicing
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[:10:2],
            self.torch_tensor[:10:2].numpy()
        )
        
        # Multi-dimensional slicing (center crop)
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[:, 90:270, 160:480],
            self.torch_tensor[:, 90:270, 160:480].numpy()
        )
        
        # Ellipsis notation (color channel)
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[..., 0],
            self.torch_tensor[..., 0].numpy()
        )
        
        # Step slicing in multiple dimensions
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[10:20, ::2, ::2],
            self.torch_tensor[10:20, ::2, ::2].numpy()
        )
        
        # Boolean indexing
        pickle_mask = self.pickle_tensor > 0.5
        torch_mask = self.torch_tensor > 0.5
        np.testing.assert_array_equal(pickle_mask, torch_mask.numpy())
        
        # Fancy indexing
        indices = [0, 5, 10, 15]
        np.testing.assert_array_almost_equal(
            self.pickle_tensor[indices],
            self.torch_tensor[indices].numpy()
        )

    def test_channel_operations(self):
        """Test channel-specific operations"""
        # Test single channel extraction
        pickle_red = self.pickle_tensor[..., 0]
        torch_red = self.torch_tensor[..., 0]
        np.testing.assert_array_almost_equal(pickle_red, torch_red.numpy())

if __name__ == '__main__':
    unittest.main()