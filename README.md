## Introduction

Would you like to stream to Twitch, Youtube, Kick, Trovo, Facebook, Instagram, and etc at once, but don't have the upload capacity to do it from your own computer?

You can host Prism on a server to act as a prism for your streamed content!

You can then simply stream to your Prism, and it will send your stream to all the platforms you'd like.


## Prequisites

You'd need a VPS server for this, but fret not, its specification or power does not matter!

You can get very cheap (1~5 USD) Linux VPS from providers such as Linode, Ionos, Digital Ocean, etc.


## How To Use

* 1- SSH into your VPS server,
```
ssh  ssh://root@<server IP address>
```

* 2- Enter the password (it will be hidden).


* 3- Install docker.


* 4- Build our image:
```
docker build -t prism github.com/MorrowShore/Prism
```

* 5- Verify it has been built:
```bash
docker images
```

* 6- Now edit the following prompt with your own key, and then run it:

```
docker run -it -p 1935:1935 --name Prism -e TWITCH_URL="<twitch server>" -e TWITCH_KEY="<twitch key>" -e FACEBOOK_KEY="<facebook key>" -e YOUTUBE_KEY="<youtube key>" -e TROVO_KEY="<trovo key>" -e KICK_KEY="<kick key>" Prism
```

If you're not going to stream to a specific platform, simply remove it from the prompt.

* 7- In OBS' stream options, enter the following in the Server field:
```
rtmp://<server IP address>/live
```

As for the stream key, you can put anything.

* 8- Begin streaming!

We advise you test it with two platforPrism first.


* To STOP the docker, (multistreaming server) run:

```
docker stop Prism
```

* To START the docker, run:

```
docker start Prism
```

* To DELETE the docker, run:

```bash
docker rm Prism
```
Then,

```bash
docker images
```
Copy the image ID and then run:

```bash
docker rmi <IMAGE_ID>
```


You can also add CloudFlare & Instagram support by adding the following to the prompt #6: 

```
-e CLOUDFLARE_KEY="<key>"
```
```bash
-e INSTAGRAM_KEY="<key>"
```

## Debugging

If something is not working you can check the logs of the container with:

```bash
docker logs Prism
```
