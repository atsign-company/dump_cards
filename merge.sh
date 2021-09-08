#!/bin/bash
#Merge together the last two files, stripping the header line from the second
LATEST_FILES=$(ls -tr | tail -2)
FIRST_FILE=$(echo $LATEST_FILES | sed 's/[^ ]* //')
SECOND_FILE=$(echo $LATEST_FILES | sed 's/ [^ ]*//')
cat "$FIRST_FILE" > "$FIRST_FILE.$SECOND_FILE"
tail -n+2 "$SECOND_FILE" >> "$FIRST_FILE.$SECOND_FILE"
