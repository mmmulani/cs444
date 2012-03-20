#!/bin/bash
files_to_zip=(\
  ax-test \
  compiler.py \
  joosc \
  Makefile \
  name_resolution \
  parser \
  scanner \
  static_analysis \
  utils \
  weeder \
  )

rm ~/upload_me_to_marmoset.zip
zip -r ~/upload_me_to_marmoset.zip ${files_to_zip[@]}
