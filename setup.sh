#!/bin/bash

set -e
set -x

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing system dependencies..."
sudo apt install --no-install-recommends \
    xserver-xorg xinit x11-xserver-utils unclutter python3-pip python3-dev git -y

echo "🐍 Installing Python packages: pygame, numpy..."
pip3 install pygame numpy

echo "📁 Cloning FreshLux repo..."
cd ~
if [ ! -d "freshlux" ]; then
  git clone https://github.com/procoder26/freshlux.git
else
  echo "FreshLux repo already cloned."
fi

echo "🧠 Creating .xinitrc to launch ad viewer..."
cat <<EOF > ~/.xinitrc
#!/bin/bash
unclutter -idle 0 &
python3 ~/freshlux/main.py
EOF
chmod +x ~/.xinitrc

echo "🚀 Setting autostart for tty1 login..."
grep -qxF 'if [ -z "\$DISPLAY" ] && [ \$(tty) = /dev/tty1 ]; then startx; fi' ~/.bash_profile || \
echo 'if [ -z "\$DISPLAY" ] && [ \$(tty) = /dev/tty1 ]; then startx; fi' >> ~/.bash_profile

echo "🎨 Installing Plymouth for boot splash..."
sudo apt install plymouth plymouth-themes -y

echo "🎯 Setting spinner theme..."
sudo plymouth-set-default-theme spinner

echo "🖼️ Adding FreshLux logo to spinner theme..."
sudo cp ~/freshlux/freshlux.png /usr/share/plymouth/themes/spinner/freshlux.png

echo "🧾 Updating spinner script..."
sudo bash -c 'cat > /usr/share/plymouth/themes/spinner/spinner.script' <<'EOF'
theme.image_path = "/usr/share/plymouth/themes/spinner";
freshlux_logo = Image("freshlux.png");
freshlux_logo:SetZ(10);
freshlux_logo:MoveTo((Window.GetWidth() - freshlux_logo:GetWidth()) / 2, Window.GetHeight() * 0.35);
Window.SetBackgroundTopColor(0, 0, 0);
Window.SetBackgroundBottomColor(0, 0, 0);
spinner = Sprite();
spinner:SetPosition(Window.GetWidth() / 2, Window.GetHeight() * 0.65);
spinner:SetZ(100);
spinner:SetAnimation("spinner", 30);
EOF

echo "📝 Editing plymouth config..."
sudo sed -i 's/ImageDir=.*/ImageDir=\/usr\/share\/plymouth\/themes\/spinner/' /usr/share/plymouth/themes/spinner/spinner.plymouth
sudo sed -i 's/ScriptFile=.*/ScriptFile=\/usr\/share\/plymouth\/themes\/spinner\/spinner.script/' /usr/share/plymouth/themes/spinner/spinner.plymouth

echo "🔧 Updating bootloader config..."
if ! grep -q "quiet splash logo.nologo" /boot/boot.cmdline; then
  sudo sed -i 's/$/ quiet splash logo.nologo/' /boot/boot.cmdline
fi

echo "🔁 Regenerating initramfs..."
sudo update-initramfs -u

echo "✅ Setup complete. Rebooting in 5 seconds..."
sleep 5
sudo reboot
