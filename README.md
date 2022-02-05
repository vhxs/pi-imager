# pi-imager
Python script to make ssh-able SD card images super easy.

- Depends on `rpi-imager` and `psudo`.
- Must download `.img` file and save to `images/` directory.
- Configure by modifying `config.yml`. Defines the following
  - Location of OS images, and which one to use.
  - Mount points, device name of SD card
  - Location of shadow file on OS, to set the password you want
  - Location of DHCP config file, so you can set whatever static IP address you want
- Run `psudo python main.py` 
