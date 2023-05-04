#!/bin/bash

FILE="RPC_server/setup.py"

VERSION_TAG="$1"
echo "VERSION_TAG: $VERSION_TAG"

if [[ "$VERSION_TAG" = "0.0.0" ]]
then
    echo "Skipping version number replacement (triggered by VERSION_TAG being '0.0.0')."
    exit 0
fi

# regex for version tag taken from official definition
if ! [[ "$VERSION_TAG" =~ ^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$ ]]
then
    echo "The version tag was not in the pip version format."
    exit 1
fi

PLACEHOLDER="0.0.0"

NUM_VT_STR_BEFORE=$(grep -o "${VERSION_TAG}" $FILE | wc -l)

sed -i "s/version='$PLACEHOLDER'/version='$VERSION_TAG'/" $FILE
echo "This is what the setup.py file looks like now:"
cat $FILE

NUM_VT_STR_AFTER=$(grep -o "${VERSION_TAG}" $FILE | wc -l)
REPLACEMENTS=$(expr $NUM_VT_STR_AFTER - $NUM_VT_STR_BEFORE)
echo "Number of replacements: ${REPLACEMENTS}"

if [[ ${REPLACEMENTS} -ne 1 ]]
then
    echo "The replacement of the version string with the tag did not work!"
    echo "Was the tag not a valid pip version? Or has the placeholder value ('${PLACEHOLDER}') been changed in the setup.py file?"
    exit 1
fi
