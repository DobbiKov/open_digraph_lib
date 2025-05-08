import sys
import os

from modules.bool_circ import bool_circ
root = os.path.normpath(os.path.join(__file__, './../../'))
sys.path.append(root) #allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.open_digraph_mixins.open_digraph_matrix_mixin import *
from modules.node import node
from modules.bool_circ import get_result_of_evaluated_enc_dec

class BoolCircTests(unittest.TestCase):
    def test_encoder_deconder_compose_evaluate_gives_identity(self):
        bit1, bit2, bit3, bit4 = '0', '1', '0', '1'
        res = bit1+bit2+bit3+bit4

        enc_g = bool_circ.generate_4bit_encoder(bit1, bit2, bit3, bit4)
        dec_g = bool_circ.generate_4bit_decoder('', '', '', '', '', '', '')
        comp = dec_g.compose(enc_g)
        comp = bool_circ(comp)
        comp.evaluate()

        self.assertEqual(len(comp.get_nodes_ids()), 4*2) 

        self.assertEqual(get_result_of_evaluated_enc_dec(comp), res)

    def test_encoder_deconder_compose_evaluate_gives_identity_with_changed_bit_1(self):
        bit1, bit2, bit3, bit4 = '0', '1', '0', '1'
        res = bit1+bit2+bit3+bit4

        enc_g = bool_circ.generate_4bit_encoder(bit1, bit2, bit3, bit4)
        dec_g = bool_circ.generate_4bit_decoder('~', '', '', '', '', '', '')
        comp = dec_g.compose(enc_g)
        comp = bool_circ(comp)
        comp.evaluate()

        self.assertEqual(len(comp.get_nodes_ids()), 4*2) 

        self.assertEqual(get_result_of_evaluated_enc_dec(comp), res)

    def test_encoder_deconder_compose_evaluate_gives_identity_with_changed_bit_2(self):
        bit1, bit2, bit3, bit4 = '0', '1', '0', '1'
        res = bit1+bit2+bit3+bit4

        enc_g = bool_circ.generate_4bit_encoder(bit1, bit2, bit3, bit4)
        dec_g = bool_circ.generate_4bit_decoder('', '', '', '~', '', '', '')
        comp = dec_g.compose(enc_g)
        comp = bool_circ(comp)
        comp.evaluate()

        self.assertEqual(len(comp.get_nodes_ids()), 4*2) 

        self.assertEqual(get_result_of_evaluated_enc_dec(comp), res)

    def test_encoder_deconder_compose_evaluate_gives_identity_with_2bits_changed(self):
        bit1, bit2, bit3, bit4 = '0', '1', '0', '1'
        res = bit1+bit2+bit3+bit4

        enc_g = bool_circ.generate_4bit_encoder(bit1, bit2, bit3, bit4)
        dec_g = bool_circ.generate_4bit_decoder('', '', '', '~', '', '', '~')
        comp = dec_g.compose(enc_g)
        comp = bool_circ(comp)
        comp.evaluate()

        self.assertEqual(len(comp.get_nodes_ids()), 4*2) 

        self.assertNotEqual(get_result_of_evaluated_enc_dec(comp), res)

if __name__ == "__main__":
    unittest.main()
