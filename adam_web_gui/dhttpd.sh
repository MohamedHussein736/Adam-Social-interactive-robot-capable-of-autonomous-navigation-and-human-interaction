#!/bin/sh 

# Run the dhttpd webserver on the defined port and set the root directory to
# the adam_web_gui directory

PORT=8181

echo 'Launching dhttpd on port' $PORT

if [ ! `pidof dhttpd` ]; then
	dhttpd -p $PORT -r `rospack find adam_web_gui`
fi
