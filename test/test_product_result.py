import unittest

from comparator.product_result import (
    ComparatorProductResult
)


class TestComparatorProductResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res = ComparatorProductResult(
            [[
                [
                    {'mean': 5.672800853433379,
                     'power': 1073777814.4721427,
                     'rms': 181.02236972828902},
                    {'mean': 1.4581813835337236,
                     'power': 96652.75406978757,
                     'rms': 1.7174422765616182}
                ],
                [
                    {'mean': 3.233081163629969e-05,
                     'power': 0.0018962821180273776,
                     'rms': 0.00024056171283880768},
                    {'mean': 0.6876932754960305,
                     'power': 19022.5477345008,
                     'rms': 0.7619200001471086}
                ],
                [
                    {'mean': 3.225394250383691e-05,
                     'power': 0.0018600611942844972,
                     'rms': 0.00023825314859169847},
                    {'mean': 0.5847065377784514,
                     'power': 11338.460403136232,
                     'rms': 0.5882366455517107}
                ]
            ], [
                None,
                [
                    {'mean': 6.429213820738072,
                     'power': 1077492853.6685228,
                     'rms': 181.33524847904872},
                    {'mean': -0.3276216890194712,
                     'power': 31461.21411298117,
                     'rms': 0.9798571628560233}
                ],
                [
                    {'mean': 1.701510479829544e-05,
                     'power': 3.18627505789411e-05,
                     'rms': 3.118291166761411e-05},
                    {'mean': 0.2752178239288577,
                     'power': 3578.0854597841885,
                     'rms': 0.3304459147226525}
                ]
            ], [
                None,
                None,
                [
                    {'mean': 6.4142984226025614,
                     'power': 1073151966.3923148,
                     'rms': 180.96960787484412},
                    {'mean': -0.3278972376161442,
                     'power': 31476.472772588157,
                     'rms': 0.9800947489589434}
                ]
            ]]
        )

    def test_contains(self):
        self.assertTrue("mean" in self.res)
        self.assertTrue("foo" not in self.res)
        self.assertFalse("foo" in self.res)

    def test_iter(self):
        val = list(self.res["mean"])
        expected_val = [[
            [
                5.672800853433379,
                1.4581813835337236
            ],
            [
                3.233081163629969e-05,
                0.6876932754960305
            ],
            [
                3.225394250383691e-05,
                0.5847065377784514
            ]
        ], [
            None,
            [
                6.429213820738072,
                -0.3276216890194712
            ],
            [
                1.701510479829544e-05,
                0.2752178239288577
            ]
        ], [
            None,
            None,
            [
                6.4142984226025614,
                -0.3278972376161442
            ]
        ]]
        self.assertEqual(val, expected_val)
        with self.assertRaises(ValueError):
            list(self.res)

    def test_getitem_str(self):
        val = self.res["mean"]._products
        expected_val = [[
            [
                {'mean': 5.672800853433379},
                {'mean': 1.4581813835337236}
            ],
            [
                {'mean': 3.233081163629969e-05},
                {'mean': 0.6876932754960305}
            ],
            [
                {'mean': 3.225394250383691e-05},
                {'mean': 0.5847065377784514}
            ]
        ], [
            None,
            [
                {'mean': 6.429213820738072},
                {'mean': -0.3276216890194712}
            ],
            [
                {'mean': 1.701510479829544e-05},
                {'mean': 0.2752178239288577}
            ]
        ], [
            None,
            None,
            [
                {'mean': 6.4142984226025614},
                {'mean': -0.3278972376161442}
            ]
        ]]
        self.assertTrue(len(val) == 3)
        self.assertTrue(len(val[0]) == 3)
        self.assertTrue(len(val[0][0]) == 2)
        self.assertEqual(val, expected_val)

    def test_getitem_tuple(self):
        val = self.res[0, 0, 0]
        expected_val = {'mean': 5.672800853433379,
                        'power': 1073777814.4721427,
                        'rms': 181.02236972828902}
        self.assertEqual(val, expected_val)

        val = self.res[2, 1]
        self.assertIsNone(val)
        val = self.res[2, 1, 0]
        self.assertIsNone(val)

    def test_getitem_int(self):
        val = self.res[0]
        self.assertEqual(len(val), 3)

    def test_len(self):
        self.assertTrue(len(self.res) == 3)

    # def test_str(self):
    #     pass

    def test_iscomplex(self):
        self.assertTrue(self.res.iscomplex)

    def test_isreal(self):
        self.assertFalse(self.res.isreal)

    def test_complex_dim(self):
        self.assertTrue(self.res.complex_dim == 2)


if __name__ == "__main__":
    unittest.main()
