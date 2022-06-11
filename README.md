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
- [ ] ansibilize the installation/setup of kubernetes
- [ ] k8s-ify the pis?

# k8s notes
- https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server
- https://opensource.com/article/20/6/kubernetes-raspberry-pi
  - on raspbian buster, edit `/boot/cmdline.txt` instead of `/boot/firmware/cmdline.txt` to enable cgroups etc
  - seems that after k8s version 1.24, Docker is no longer supported as a CRI (container runtime engine) `
  - `kubectl` crashloops until it's given a thing to do?
  - using k8s requires that you disable swap, can be done with `sudo swapoff -a`
  - can run Lens IDE on my laptop, entirely outside of the cluster, by pointing to a control node in `kubeconfig`?
