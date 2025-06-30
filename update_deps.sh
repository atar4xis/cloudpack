#!/bin/bash

if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found!"
  exit 1
fi

# format dependencies into TOML array lines
deps=$(sed '/^\s*$/d;/^\s*#/d;s/.*/    "&",/' requirements.txt)

# create new dependencies block content
{
  echo "dependencies = ["
  echo "$deps"
  echo "]"
} >deps_block.tmp

# replace the dependencies block in pyproject.toml with the new block
# create a temp output file
awk '
  BEGIN { in_deps=0 }
  /^dependencies = \[/ {
    if (in_deps == 0) {
      in_deps=1
      system("cat deps_block.tmp")
    }
    next
  }
  in_deps && /^\]/ {
    in_deps=0
    next
  }
  in_deps { next }
  { print }
' pyproject.toml >pyproject.toml.tmp

mv pyproject.toml.tmp pyproject.toml
rm deps_block.tmp

echo "pyproject.toml dependencies updated."
