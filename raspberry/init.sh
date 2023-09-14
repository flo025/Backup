sudo apt update
sudo apt upgrade
sudo apt install python3-pip
pip3 install -r requirements.txt
sudo apt install python3-opencv -y

pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U

#crontab
crontab -l > mycron
echo "30 8 * * 1-5 python3 /home/pi/2023_iot/send_sensor_data.py >> /home/pi/2023_iot/logs/log-$(date +\%Y-\%m-\%d).log 2>&1" >> mycron
echo "30-59 8 * * 1-5 python3 /home/pi/2023_iot/send_image.py >> /home/pi/2023_iot/logs/log-$(date +\%Y-\%m-\%d).log 2>&1" >> mycron
echo "* 9-17 * * 1-5 python3 /home/pi/2023_iot/send_image.py >> /home/pi/2023_iot/logs/log-$(date +\%Y-\%m-\%d).log 2>&1" >> mycron
echo "0-30 18 * * 1-5 python3 /home/pi/2023_iot/send_image.py >> /home/pi/2023_iot/logs/log-$(date +\%Y-\%m-\%d).log 2>&1" >> mycron
crontab mycron
rm mycron