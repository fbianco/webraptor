#!/bin/sh
echo 'Compressing css'
rm -f compressed.css
for f in blueprint-screen.css MenuMatic.css style.css
do
    /usr/bin/yui-compressor --type css $f >> compressed.css
done
