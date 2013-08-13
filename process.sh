#!/bin/bash

TARGET=content/$1
STATIC=static/$1
mkdir -p $TARGET
mkdir -p $STATIC


for article in originals/$1/*; do
	# TODO: comments.json
	cp $article/*.{jpg,jpeg,png} $STATIC/
	(
		echo ---
		cat $article/metadata.yaml
		echo ---
		 
		sed -f images.sed $article/post.html | pandoc -t markdown_strict -f html -
	) > $TARGET/$(basename $article).md;
done