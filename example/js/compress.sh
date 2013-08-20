#!/bin/sh
echo 'Compressing js'
rm -f compressed.js
for f in mootools.js mootools-more.js menumatic.js effects.js
do
    /usr/bin/yui-compressor --type js $f >> compressed.js
done
