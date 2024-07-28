#!/bin/bash

[ -e latest_unverified_url.dat ] || exit 0

S=`cat latest_unverified_url.dat`

echo $S >> verified_urls.dat
rm latest_unverified_url.dat

echo "verified" $S
