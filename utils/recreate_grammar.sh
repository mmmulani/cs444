#!/bin/sh
python check_symbols.py
python create_cfg.py > test.cfg && java jlalr.Jlalr1 < test.cfg > joos.lr1 && python build_shift_reduce_maps.py joos.lr1 joos_reduce.txt joos_shift.txt
