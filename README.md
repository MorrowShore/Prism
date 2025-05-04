## NOW WITH CUSTOM DESTINATIONS & RTMP STATS

## Introduction

Would you like to stream to Twitch, Youtube, Kick, Trovo, Facebook, Instagram, X (Twitter), Cloudflare, and custom RTMP destinations at once, but don't have the upload capacity to do it from your own computer?

You can host Prism on a server to act as a prism for your streamed content!

You can then simply stream **one** high-quality feed to your Prism server, and it will securely and efficiently relay your stream to all the platforms you configure.

## Prequisites

You'd need a VPS server for this. While powerful hardware isn't strictly necessary for basic relaying, **network performance (bandwidth, low latency, stable routing) between your VPS and your chosen streaming platforms is crucial**, especially for high-bitrate streams (like 1080p 60fps).

Cheap VPS options ($5-10 USD range) often work well. Providers like Linode, Digital Ocean, Vultr, Hetzner Cloud, etc., are popular choices. Choose a location geographically close to you or with good known peering to your primary streaming destinations.

## How To Set up

*   1- SSH into your VPS server:
    ```bash
    ssh root@<server_ip_address>
    ```

*   2- Enter the password (it will likely be hidden).

*   3- Install Docker: Follow the official Docker installation guide for your VPS's Linux distribution (e.g., Debian, Ubuntu).
    *   Example for Debian/Ubuntu:
        ```bash
        apt update && apt install -y docker.io
        systemctl start docker
        systemctl enable docker
        ```

*   4- Build the PrismRTMPS image:
    ```bash
    docker build -t prism https://github.com/waefrebeorn/PrismRTMPS.git
    ```
    *(Note: Building directly from GitHub requires Git to be installed on the VPS: `apt install -y git`)*
    *Alternatively, clone the repo first (`git clone https://github.com/waefrebeorn/PrismRTMPS.git`) and then build from the local directory (`cd PrismRTMPS && docker build -t prism .`)*

*   5- Verify the image has been built:
    ```bash
    docker images
    ```
    *(You should see `prism` listed)*

*   6- **Run the Prism Container:**
    *   Provide the specific stream keys for **each destination platform** you want to stream *to*.
    *   **IMPORTANT:** The key you use in OBS (Step 7) **must** be one of the keys you provide here using the `-e PLATFORM_KEY="..."` arguments. Any non-empty key provided here will grant access to the relay if used in OBS.
    *   Remove the `-e PLATFORM_KEY="..."` lines for platforms you *don't* want to use.

    **Example `docker run` command:**
    ```bash
    docker run -d --name prism \
      -p 1935:1935 \
      -p 8081:8081 `# Expose port for RTMP stats page` \
      --restart unless-stopped `# Optional: auto-restart container` \
      # --- Provide keys for destinations you want to use ---
      -e YOUTUBE_KEY="your-youtube-stream-key" `# You could use this key in OBS` \
      -e TWITCH_URL="rtmp://live-iad.twitch.tv/app/" `# Important: Find your nearest Twitch ingest server!` \
      -e TWITCH_KEY="your_twitch_stream_key" `# Or you could use this key in OBS` \
      -e KICK_KEY="sk_us-west-1_xxxxxxxxxxxxxx" `# Or this one...` \
      -e FACEBOOK_KEY="your-facebook-stream-key" \
      -e X_KEY="your_x_twitter_stream_key" \
      # -e INSTAGRAM_KEY="your-ig-key" ` # Uncomment if using Instagram ` \
      # -e CLOUDFLARE_KEY="your-cf-key" ` # Uncomment if using Cloudflare ` \
      # -e TROVO_KEY="your-trovo-key" `   # Uncomment if using Trovo ` \
      # -e RTMP1_URL="rtmp://custom.server.com/live" ` # Uncomment for Custom Dest 1 ` \
      # -e RTMP1_KEY="custom-key-1" `                  # Uncomment for Custom Dest 1 ` \
      prism
    ```
    *   Replace placeholder values (`your-key-here`, URLs) with your actual keys and preferred ingest URLs.
    *   The `-d` runs the container in detached mode (in the background).
    *   `--restart unless-stopped` makes Docker automatically restart the container if it crashes or the VPS reboots.

*   7- **Configure OBS (or other streaming software):**
    *   Service: `Custom...`
    *   Server: `rtmp://<your_vps_ip_address>:1935/live`
    *   Stream Key: **Use ONE of the actual stream keys you configured in the `docker run` command** (e.g., paste your `YOUTUBE_KEY` value here, or your `TWITCH_KEY` value, etc.).

*   8- Begin streaming from OBS! Your stream goes to Prism, which then relays it to YouTube, Twitch, Kick, etc.

*   9- **(Optional) View Stream Statistics:** Open `http://<your_vps_ip_address>:8081/stat` in your web browser to see details about active connections, bitrates, etc.

We advise testing with just one or two destinations first to ensure the setup is correct before enabling all platforms.

## How To Manage

*   **STOP** the container:
    ```bash
    docker stop prism
    ```

*   **START** the container (if stopped):
    ```bash
    docker start prism
    ```

*   **VIEW LOGS** (essential for troubleshooting):
    ```bash
    docker logs prism
    ```
    *   To follow logs in real-time:
        ```bash
        docker logs -f prism
        ```

*   **EDIT Destinations / Keys:**
    1.  Stop the current container: `docker stop prism`
    2.  Remove the current container: `docker rm prism`
    3.  Run a new container using the `docker run` command (from Step 6) with your updated `-e` variables.

*   **UNINSTALL** the entire project:
    1.  Stop the container: `docker stop prism`
    2.  Remove the container: `docker rm prism`
    3.  List images: `docker images`
    4.  Find the IMAGE ID for `prism`.
    5.  Remove the image: `docker rmi <IMAGE_ID>`
    6.  (Optional) Remove Docker itself if no longer needed.

## Troubleshooting Common Issues

*   **Lag / Falling Behind Stream:** This is almost always caused by a **slow connection between your VPS and *one* of the destination platforms**.
    *   **Diagnosis:** Stop the container, remove it, and run tests pushing to *only one destination at a time* (modify the `docker run` command). Identify which specific platform causes the lag when streamed to alone.
    *   Check network path quality from VPS to the slow destination using `mtr <destination_hostname>` (install `mtr` on VPS: `apt update && apt install mtr -y`). Look for packet loss or high latency hops.
    *   **Solutions:** Try a different ingest server for that platform, change VPS provider/location for better routing, or reduce your stream bitrate in OBS.
*   **Stream Rejects / "Invalid Key":**
    *   Ensure the key you put in OBS *exactly* matches **one** of the non-empty keys (`YOUTUBE_KEY`, `TWITCH_KEY`, etc.) you set in the `docker run` command.
    *   Make sure you actually provided at least one `-e PLATFORM_KEY=...` in your `docker run` command.
    *   Check the validator logs: `docker exec prism tail /tmp/validator.log` or `docker logs prism` for validator startup messages and specific rejection reasons.
*   **One Destination Not Working:**
    *   Double-check the URL and Key for that specific platform in your `docker run` command.
    *   Check Nginx and Stunnel logs: `docker logs prism`. Look for connection errors related to that destination's port or hostname.
    *   Ensure the destination platform's stream is correctly set up (e.g., "Go Live" clicked on YouTube/Facebook).

## Support

Need help with anything, or have thought of an upgrade?

Find us at our Discord server: https://discord.gg/2sbnwze753
