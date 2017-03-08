# -*- mode: ruby -*-
# vi: set ft=ruby :
# vagrant box add wheezy32 https://dl.dropboxusercontent.com/u/78793012/vagrantup/wheezy32.box

$provisioner = <<SCRIPT
echo "#!/bin/bash
function InstallPip {
  if [ '$(which pip)' ]; then
    echo '-- Already installed.'
    return
  fi
  apt-get install python-dev python-setuptools -y -qq
  curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py
  rm get-pip.py
}
echo 'Installing Pip...'; InstallPip
echo 'Installing Flask...'; pip install flask
exit 0" | /bin/bash
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "wheezy32"
  config.vm.provision :shell, :inline => $provisioner # runs as root
  config.vm.network :forwarded_port, guest: 5000, host: 5000
end
