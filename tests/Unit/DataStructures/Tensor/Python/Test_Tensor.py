# Distributed under the MIT License.
# See LICENSE.txt for details.

from spectre.DataStructures import DataVector
from spectre.DataStructures.Tensor import tnsr, Frame, Scalar
import unittest
import numpy as np
import numpy.testing as npt


class TestTensor(unittest.TestCase):
    def test_tensor(self):
        coords = tnsr.I[DataVector, 3, Frame.Inertial](num_points=4, fill=0.)
        self.assertEqual(coords.rank, 1)
        self.assertEqual(coords.size, 3)
        self.assertEqual(len(coords), 3)
        npt.assert_equal(coords[0], np.zeros(4))
        npt.assert_equal(coords[1], np.zeros(4))
        npt.assert_equal(coords[2], np.zeros(4))
        coords[0] = DataVector(4, 1.)
        coords[1] = DataVector(4, 2.)
        coords[2] = DataVector(4, 3.)
        for d, xyz in enumerate(coords):
            npt.assert_equal(xyz, np.ones(4) * (d + 1))
            self.assertEqual(coords.multiplicity(d), 1)
            self.assertEqual(coords.component_suffix(d), ["_x", "_y", "_z"][d])

    def test_construct_from_list(self):
        data = [DataVector(xyz) for xyz in np.random.rand(3, 4)]
        coords = tnsr.I[DataVector, 3, Frame.Inertial](data)
        npt.assert_equal(np.array(coords), data)

    def test_numpy_interoperability(self):
        data = np.random.rand(3, 4)
        for copy in [True, False]:
            coords = tnsr.I[DataVector, 3, Frame.Inertial](data, copy=copy)
            for i, (a, b) in enumerate(zip(coords, data)):
                npt.assert_equal(a, b, f"Mismatch at index {i}")
            npt.assert_equal(np.array(coords), data)

    def test_tensor_double(self):
        coords = tnsr.I[float, 3, Frame.Inertial](fill=0.)
        coords[0] = 1.
        coords[1] = 2.
        coords[2] = 3.
        npt.assert_equal(np.array(coords), [1., 2., 3.])

    def test_scalar(self):
        scalar = Scalar[DataVector](num_points=4, fill=1.)
        npt.assert_equal(np.array(scalar), np.ones((1, 4)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
