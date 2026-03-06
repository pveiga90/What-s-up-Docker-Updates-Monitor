
# What's up Docker Updates Monitor

## About

This integration grabs info from a What's up Docker instance using the Rest API, creating a sensor per container indicating if there are updates available.
It will also assign all sensors from the same instance to the a device, making it easier to manage if you have multiple instances of What's up Docker

## Installation

Installation is done like any other Home Assistant HACS integration.

### Requirements

[](https://github.com/meichthys/uptime_kuma/blob/main/README.md#requirements)

In order to setup this integration you will need:

-   A Home Assistant instance with [HACS](https://hacs.xyz/) installed.
-   An instance of [What's up Docker](https://github.com/fmartinou/whats-up-docker)

### HACS Installation

Search for "What's up Docker Updates Monitor" in the HACS store. If you don't see it there, you can [add this repository url as a HACS custom repository](https://hacs.xyz/docs/faq/custom_repositories).

[![hacs_badge](https://camo.githubusercontent.com/e983f5420af8b0d8284a16e6127d04146f0a19aa559a11698056dbd42c4de1af/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f484143532d437573746f6d2d3431424446352e7376673f7374796c653d666f722d7468652d6261646765)](https://github.com/pveiga90/What-s-up-Docker-Updates-Monitor)

## Home Assistant Integration

After installation, setup the integration via the web UI like any other integration. When prompted, provide the following:

-   **Host:** *Your What's up Docker IP Address or hostname. You may also include `http://` or `https://`; if no protocol is specified the integration will assume `http`.*
-   **Port:** *the port for the Web UI of What's up Docker (optional). Defaults to port 80 for http, 443 for https.*
-   **Instance_Name:** *This will be the "device" all sensors get associated to*


### Troubleshooting

If you are having issues connecting, make sure you can successfully connect to `<protocol>://<wud_host>[:<port>]/api/containers` (e.g. `http://10.0.0.5:3000/api/containers`). This should retrieve a JSON with all your monitored containers info.

## Contributions

Contributions are welcome!
