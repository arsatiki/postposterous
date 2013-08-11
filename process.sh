#!/bin/bash

TARGET=content/$1
mkdir -p $TARGET

for article in originals/$1/*; do
	(
		echo ---
		cat $article/metadata.yaml
		echo ---
		pandoc -t markdown_strict $article/post.html
	) > $TARGET/$(basename $article).md;
done