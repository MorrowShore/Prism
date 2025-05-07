# NOW WITH SECURITY FEATURE

## NOW WITH CUSTOM DESTINATIONS

## Introduction

Would you like to stream to Twitch, Youtube, Kick, Trovo, Facebook, Instagram, and etc at once, but don't have the upload capacity to do it from your own computer?

You can host Prism on a server to act as a prism for your streamed content!

You can then simply stream to your Prism, and it will send your stream to all the platforms you'd like.


---

## Prequisites

You'd need a VPS server for this, but fret not, its specification or power does not matter!

You can get very cheap (1~5 USD) Linux VPS from providers such as OVH, Hetzner, Netcup, Linode, IONOS, Digital Ocean, etc.



---
---
## How To Set up

* 1- SSH into your VPS server,
```
ssh  ssh://root@<server IP address>
```

---
* 2- Enter the password (it will be hidden).<br>
If you haven't set a password before, use what your VPS provider gave you.

---
* 3- Install docker.
```
sudo apt update && sudo apt upgrade -y && sudo apt install -y docker.io docker-compose
```

---
* 4- Build our image:
```
docker build -t prism github.com/MorrowShore/Prism
```
---
* 5- Verify it has been built: (you should see "prism" in the list)
```bash
docker images
```

---
* 6- Now edit the following command with your own key, then copy it all, then paste it in your server's terminal and run it:
```
docker run -d -p 1935:1935 --name prism \
  -e YOUTUBE_KEY="your-youtube-key" \
  -e FACEBOOK_KEY="your-facebook-key" \
  -e INSTAGRAM_KEY="your-instagram-key" \
  -e TWITCH_URL="your-twitch-server" \
  -e TWITCH_KEY="your-twitch-key" \
  -e TROVO_KEY="your-trovo-key" \
  -e KICK_KEY="your-kick-key" \
  -e RTMP1_URL="custom-rtmp1-server" \
  -e RTMP1_KEY="custom-rtmp1-key" \
  -e RTMP2_URL="custom-rtmp2-server" \
  -e RTMP2_KEY="custom-rtmp2-key" \
  -e RTMP3_URL="custom-rtmp3-server" \
  -e RTMP3_KEY="custom-rtmp3-key" \
  prism && sleep 1 && docker logs prism | grep -A5 "# "
```
Each line starting with -e signals a destination. **Remove all the destination lines that don't concern you.**<br>
In order words, if you're not going to stream to a specific platform, simply remove the entire line concerning it from the command above.


---
After running it, you will see a report, such as 
```
======================================
Your Stream Destination: rtmp://123.123.123.123/eeKZWH4iDPyo
======================================
Your Stream Key Does Not Matter
======================================
```
**This gives you your stream destination and your stream key.**


Note: RTMP1, RTMP2, and RTMP3 refer to custom destinations. <br>You can fill in the details of custom destinations or platforms by filling in the RTMP variables with their server URL and the stream key.

---
* 7- In OBS' stream options, enter your stream destination in the Server field. For a made-up example:
```
rtmp://123.123.123.123/eeKZWH4iDPyo
```

As for the Prism stream key in OBS settings, you can put anything.

---
* 8- Begin streaming!

We advise you test it with two platforms first.



## How To Manage

* To STOP the docker, (multistreaming server) run:

```
docker stop prism
```

---

* To START the docker, run:

```
docker start prism
```

---

* To EDIT the destinations,

Remove the container:

```
docker rm prism
```

and then run an edited prompt at step #6

---

* To UNINSTALL the entire project, run:

```
docker rm prism
```
Then,

```
docker images
```
Copy the image ID and then run:

```
docker rmi <IMAGE_ID>
```

---

* To ADD CloudFlare & Instagram support: 

Add the following to the prompt #6
```
-e CLOUDFLARE_KEY="<key>"
```
```
-e INSTAGRAM_KEY="<key>"
```

## Debugging

If something is not working you can check the logs of the container with:

```bash
docker logs prism
```


## Support

Need help with anything, or have thought of an upgrade?

Find us at our Discord server: https://discord.gg/2sbnwze753


