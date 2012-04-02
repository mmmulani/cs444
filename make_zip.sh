#!/bin/bash
files_to_zip=(\
  ax-test \
  code_gen \
  compiler.py \
  exec_tests.py \
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
