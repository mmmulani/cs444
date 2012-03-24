#!/bin/bash

# Assembles and links all assembly files found in the "output" directory,
# and creates an executable called main

# Assemble all .s files found in the output directory:
for f in output/*.s
do
  echo "Assembling $f ..."
  /u/cs444/bin/nasm -O0 -f elf -g -F dwarf $f
done

# Link all .o files found in the output directory, and runtime.o:
echo "Linking..."
ld -melf_i386 -o main output/*.o stdlib/5.0/runtime.o
