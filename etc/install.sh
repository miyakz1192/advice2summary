set -x

cd /etc/systemd/system 
sudo rm advice2summary.service
sudo ln -s ~/advice2summary/etc/advice2summary.service advice2summary.service

sudo systemctl enable advice2summary.service

