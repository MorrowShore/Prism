#!/bin/bash

set -e

NGINX_TEMPLATE=/etc/nginx/nginx.conf.template
NGINX_CONF=/etc/nginx/nginx.conf
ENV_OK=0

if [ -n "${YOUTUBE_KEY}" ]; then
	echo "Youtube activate."
	sed -i 's|#youtube|push '"$YOUTUBE_URL"'${YOUTUBE_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#youtube| |g' $NGINX_TEMPLATE
fi

if [ -n "${FACEBOOK_KEY}" ]; then
	echo "Facebook activate."
	sed -i 's|#facebook|push '"$FACEBOOK_URL"'${FACEBOOK_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#facebook| |g' $NGINX_TEMPLATE
fi

if [ -n "${INSTAGRAM_KEY}" ]; then
	echo "Instagram activate."
	sed -i 's|#instagram|push '"$INSTAGRAM_URL"'${INSTAGRAM_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#instagram| |g' $NGINX_TEMPLATE
fi

if [ -n "${CLOUDFLARE_KEY}" ]; then
	echo "Cloudflare activate."
	sed -i 's|#cloudflare|push '"$CLOUDFLARE_URL"'${CLOUDFLARE_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#cloudflare| |g' $NGINX_TEMPLATE
fi

if [ -n "${TWITCH_KEY}" ]; then
	echo "Twitch activate."
	sed -i 's|#twitch|push '"$TWITCH_URL"'${TWITCH_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#twitch| |g' $NGINX_TEMPLATE
fi

if [ -n "${TROVO_KEY}" ]; then
	echo "Trovo activate."
	sed -i 's|#trovo|push '"$TROVO_URL"'${TROVO_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#trovo| |g' $NGINX_TEMPLATE
fi

if [ -n "${KICK_KEY}" ]; then
	echo "Kick activate."
	sed -i 's|#kick|push '"$KICK_URL"'${KICK_KEY};|g' $NGINX_TEMPLATE
	ENV_OK=1
else
	sed -i 's|#kick| |g' $NGINX_TEMPLATE
fi

if [ $ENV_OK -eq 1 ]; then
    envsubst < $NGINX_TEMPLATE > $NGINX_CONF
else
	echo "Start local server."
fi

if [ -n "${DEBUG}" ]; then
	echo $NGINX_CONF
	cat $NGINX_CONF
fi

stunnel4

exec "$@"
