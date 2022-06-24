# Rpi Cluster-er
Originally started as a project to automatically create Rpi OS images that are ssh-able and autoconnect to my home wifi. Let's be more ambitious with this and automate the setup/configuration of a Kubernetes cluster on top of a collection of RPis that I own.

## Burning a new OS image
- Depends on `rpi-imager` and `psudo`.
- Must download `.img` file and save to `images/` directory.
- Configure by modifying `config.yml`. Defines the following
  - Location of OS images, and which one to use.
  - Mount points, device name of SD card
  - Location of shadow file on OS, to set the password you want
  - Location of DHCP config file, so you can set whatever static IP address you want
- Run `psudo python main.py` 

## todo
- [ ] configure install script to add ssh public key specified in `config.yml`. This is so we can communicate passwordlessly from an ansible control node
- [ ] rename the hostname in the install script so they're not all named `raspberrypi` (k8s yells at me for this)
- [ ] ansibilize the installation/setup of kubernetes
- [ ] write script that pings me when RPis with >= 4gb RAM are available in stock? Chip shortage means I can't buy them and can't run real k8s :(

## k8s notes
- https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server
- https://opensource.com/article/20/6/kubernetes-raspberry-pi
  - on raspbian buster, edit `/boot/cmdline.txt` instead of `/boot/firmware/cmdline.txt` to enable cgroups etc
  - seems that after k8s version 1.24, Docker is no longer supported as a CRI (container runtime engine) `
  - `kubelet` crashloops until it's given a thing to do?
  - using k8s requires that you disable swap, can be done with `sudo swapoff -a`
  - can run Lens IDE on my laptop, entirely outside of the cluster, by pointing to a control node in `kubeconfig`?
