import yaml
import os
import subprocess
import hashlib
import binascii
import getpass
import time


class Config:
    def __init__(self, config_file):
        self.config = yaml.safe_load(open(config_file))

    def get_filesystem_info(self):
        return self.config["fs"]

    def get_network_info(self):
        return self.config["network"]

    def get_image_info(self):
        return self.config["image"]


def rewrite_image(config):
    image_info = config.get_image_info()
    imager_dir = image_info["dir"]
    image = image_info["os_image"]
    image_path = os.path.join(imager_dir, image)

    fs_info= config.get_filesystem_info()
    device_path = fs_info["device"]

    rpi_image_cmd = ["rpi-imager", "--cli", "--disable-verify", image_path, device_path]

    subprocess.run(rpi_image_cmd)

    print("image written")

# create ssh file to enable ssh
def create_ssh_file(config):
    fs_info = config.get_filesystem_info()
    device_path = fs_info["mount"]
    boot_dir = fs_info["boot"]
    ssh_file_path = os.path.join(device_path, boot_dir, "ssh")

    open(ssh_file_path, "w")


# create wpa_supplicate conf file to auto connect to wifi
def create_wpa_supplicate_file(config):
    fs_info = config.get_filesystem_info()
    device_path = fs_info["mount"]
    boot_dir = fs_info["boot"]
    wpa_conf_file_path = os.path.join(device_path, boot_dir, "wpa_supplicant.conf")

    ssid = input("WiFi SSID: ")
    pass_hash = wpa_psk(ssid)
    file_contents = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=US
update_config=1
network={{
    ssid="{ssid}"
    psk={pass_hash}
}}"""

    wpa_conf_file = open(wpa_conf_file_path, "w")
    wpa_conf_file.write(file_contents)
    wpa_conf_file.close()


def wpa_psk(ssid):
    ssid_pass = getpass.getpass(f"{ssid} password: ")
    dk = hashlib.pbkdf2_hmac('sha1', str.encode(ssid_pass), str.encode(ssid), 4096, 32)

    return binascii.hexlify(dk).decode("utf-8")


# give static IP
def modify_dhcpcd(config):
    fs_info = config.get_filesystem_info()
    network_info = config.get_network_info()
    device_path = fs_info["mount"]
    root_dir = fs_info["root"]
    dhcpcd_rel_path = network_info["dhcpcd"]
    dhcpcd_path = os.path.join(device_path, root_dir, dhcpcd_rel_path)
    ip_address = input("IP address: ")
    router = input("Router: ")

    dhcpcd_file = open(dhcpcd_path, "a")
    dhcpcd_file.write(f"static ip_address={ip_address}/24\n")
    dhcpcd_file.write(f"static routers={router}\n")
    dhcpcd_file.close()


def modify_shadow(config):
    fs_info = config.get_filesystem_info()
    device_path = fs_info["mount"]
    root_dir = fs_info["root"]
    shadow_rel_path = fs_info["shadow"]
    shadow_path = os.path.join(device_path, root_dir, shadow_rel_path)

    pass_hash = create_pass_hash()
    shadow_contents = open(shadow_path).readlines()

    with open(shadow_path, "w") as new_shadow_file:
        for line in shadow_contents:
            if line.startswith("pi:"):
                tokens = line.split(":")
                tokens[1] = pass_hash
                new_line = ":".join(tokens)
            else:
                new_line = line
            new_shadow_file.write(new_line)

def create_pass_hash():
    openssl_cmd = ["openssl", "passwd", "-6"]
    pass_hash = subprocess.run(openssl_cmd, stdout=subprocess.PIPE)
    return pass_hash.stdout.decode("utf-8").strip()

def un_eject(config):
    eject(config)

    fs_info = config.get_filesystem_info()
    device_path = fs_info["device"]
    un_eject_cmd = ["eject", "-t", device_path]

    subprocess.run(un_eject_cmd)

    # wait for SD card to be reinserted
    time.sleep(10)

def eject(config):
    fs_info = config.get_filesystem_info()
    device_path = fs_info["device"]
    eject_cmd = ["eject", device_path]

    subprocess.run(eject_cmd)

    # wait
    time.sleep(10)

if __name__ == '__main__':
    c = Config("config.yml")

    rewrite_image(c)
    un_eject(c)

    create_ssh_file(c)
    create_wpa_supplicate_file(c)
    modify_dhcpcd(c)
    modify_shadow(c)

    eject(c)