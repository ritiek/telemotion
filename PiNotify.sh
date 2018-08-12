#!/bin/bash

if [ $# -le 1 ]; then
    echo 'Usage: bash PiNotify.sh type data'
    echo 'type = ["text", "photo", "file"]'
    exit
fi

TOKEN=
CHAT_ID=

if [ $1 == 'text' ]; then
    TEXT="$(printf "$2")"
    curl -s -X POST https://api.telegram.org/bot$TOKEN/sendMessage -F text="$TEXT" -F chat_id=$CHAT_ID > /dev/null
elif [ $1 == 'photo' ]; then
    curl -s -X POST https://api.telegram.org/bot$TOKEN/sendPhoto -F photo="@$2" -F caption="${2##*/}" -F chat_id=$CHAT_ID > /dev/null
elif [ $1 == 'file' ]; then
    curl -s -X POST https://api.telegram.org/bot$TOKEN/sendDocument -F document="@$2" -F caption="${2##*/}" -F chat_id=$CHAT_ID > /dev/null
fi
