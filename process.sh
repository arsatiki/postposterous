#!/bin/bash

TARGET=hugotest/content/$1

for article in $1/*; do
	(
		echo ---
		cat $article/metadata.yml
		echo ---
		pandoc -t markdown_strict $article/post.html
	) > $target/$(basename $article).md;
done