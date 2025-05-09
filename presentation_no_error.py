from modules.graphs import graph_de_prof_td_10
from modules.open_digraph import *
from modules.bool_circ import *
import inspect
from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")


bit1, bit2, bit3, bit4 = '0', '1', '0', '1'
res = bit1+bit2+bit3+bit4
enc_g = bool_circ.generate_4bit_encoder(bit1, bit2, bit3, bit4)
#enc_g.display('encoder')
dec_g = bool_circ.generate_4bit_decoder('', '', '', '', '', '', '')
#dec_g.display('decoder')

comp = dec_g.compose(enc_g)
comp = bool_circ(comp)
comp.display('comp')

comp.evaluate()
comp.display('encoder_decoder_compose')