#!/bin/bash
TITLE="$1"
BODY="$2"

git add .

if [[ -n "$BODY" ]]; then
    git commit -m "$TITLE" -m "$BODY"
else
    git commit -m "$TITLE"
fi

git push
