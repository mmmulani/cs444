#!/bin/bash
files_to_zip=(\
  compiler.py \
  joosc \
  Makefile \
  name_resolution \
  parser \
  scanner \
  utils \
  weeder \
  )
zip -r ~/upload_me_to_marmoset.zip ${files_to_zip[@]}
