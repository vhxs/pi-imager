# pi-imager
Python tool to create microSD cards with OS installed, that are ssh-able, and that auto-connected to a specified access point.

- Depends on `rpi-imager` and `psudo`.
- Must download `.img` file and save to `images/` directory.
- Configure by modifying `config.yml`. Defines the following
  - Location of OS images, and which one to use.
  - Mount points, device name of SD card
  - Location of shadow file on OS, to set the password you want
  - Location of DHCP config file, so you can set whatever static IP address you want
- Run `psudo python main.py` 

# todo
- [ ] configure install script to add ssh public key specified in `config.yml`. This is so we can communicate passwordlessly from an ansible control node
- [ ] k8s-ify the pis?

# related knowledge
- https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server
- https://opensource.com/article/20/6/kubernetes-raspberry-pi
