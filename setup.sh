#!/bin/bash

echo "🔄 Updating packages..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing X11, Python, and pygame dependencies..."
sudo apt install --no-install-recommends \
    xserver-xorg xinit x11-xserver-utils \
    python3-pip python3-dev git unclutter -y

echo "🐍 Installing pygame..."
pip3 install pygame

echo "📁 Cloning the FreshLux repo..."
cd /home/$(whoami)
git clone https://github.com/procoder26/freshlux.git

echo "🧠 Creating X11 launcher script..."
cat <<EOF > /home/$(whoami)/.xinitrc
#!/bin/bash
unclutter -idle 0 &
python3 /home/$(whoami)/freshlux/main.py
EOF
chmod +x /home/$(whoami)/.xinitrc

echo "🚀 Auto-starting startx on login..."
echo "if [ -z \"\$DISPLAY\" ] && [ \$(tty) = /dev/tty1 ]; then startx; fi" >> /home/$(whoami)/.bash_profile

echo "🖼️ Setting custom splash screen..."
sudo apt install plymouth plymouth-themes -y

# For ROC, the splash path may not be 'pix', use default if available
sudo cp /home/$(whoami)/freshlux/freshlux.png /usr/share/plymouth/themes/pix/splash.png || sudo cp /home/$(whoami)/freshlux/freshlux.png /usr/share/plymouth/themes/text/splash.png

# Use ROC-specific cmdline path
sudo sed -i 's/$/ quiet splash logo.nologo/' /boot/boot.cmdline
sudo update-initramfs -u

echo "✅ Setup complete. Rebooting..."
sleep 3
sudo reboot
