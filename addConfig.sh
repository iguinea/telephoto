#!/bin/bash

CONFIG_FILE=/opt/telePhoto/config.yaml
if [ $# -ne 2 ]; then
    echo "Usage: $0 <TOKEN> <CHANNEL_ID>"
    exit 1
fi

if [ -f $CONFIG_FILE ]; then
    echo "Config file already exists"
    chmod 600 $CONFIG_FILE
fi

sed \
    -e "s/TOKEN: '1234123412:XXXXXXXXXXXX.....XXXXX'/TOKEN: '$1'/g" \
    -e "s/CHANNEL_ID: '@yourchannel'/CHANNEL_ID: '$2'/g" \
    config.yaml.template > $CONFIG_FILE

chmod 400 $CONFIG_FILE
