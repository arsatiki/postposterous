#!/bin/bash

TARGET=hugotest/content/$1
mkdir -p $TARGET

for article in $1/*; do
	(
		echo ---
		cat $article/metadata.yaml
		echo ---
		pandoc -t markdown_strict $article/post.html
	) > $target/$(basename $article).md;
done