cmd-shift-v to see this doc in MARKDOWN
control-shift-v in linux


Install netatalk
```
sudo apt-get install netatalk
```
Also, netatalk defaults does not allow us to connect to see the drive.
Need to allow the home directory to be shared. or really any directory
https://chicagodist.com/blogs/news/using-netatalk-to-share-files-between-a-raspberry-pi-and-mac
```
sudo nano /etc/netatalk/afp.conf
```
If you take a look at the default install of that file, you will see something like this:
```
	; Netatalk 3.x configuration file
	;
	[Global]
	; Global server settings
	; [Homes]
	; basedir regex = /home
	; [My AFP Volume]
	; path = /home/pi
	; [My Time Machine Volume]
	; path = /path/to/backup
	; time machine = yes
	; log file = /home/pi/afp.log
```
	
Those semi colons indicate almost every line in the above file are commented out.  So, by default, nothing in shared in Netatalk.  From a security standpoint this is nice, but from a usability standpoint it seems a bit overkill.
 
To allow Netatalk to connect to /home/pi, all you have to do is uncomment two lines:
```
	[Homes]
	basedir regex = /home
```
Note: on the basedir line, if you see the following:
```
	basedir regex = /xxxx
```
change it to
```
	basedir regex = /home
```
And then restart Netatalk with:
```
	sudo systemctl restart netatalk
```

Dropbox doesn't run easily on arm so copy the working folder
Really need to get into a good github flow. It's the only way



Install and mount the drive and use it in VSCODE
https://www.raspberrypi.com/news/visual-studio-code-comes-to-raspberry-pi/
```


sudo apt install git
sudo apt install code -y
```

Once VSCode is up and running I need to set up the environment. Since I don't want to use the root env, 
install conda (maybe a better way?)
Currently not using an env but I think it's probably a good idea



Then use remote connect to connect via SSH
https://www.raspberrypi.com/news/coding-on-raspberry-pi-remotely-with-visual-studio-code/
If the device is named the same it'll give a key has changed error. Delete on the connecting device
```
nano ~/.ssh/known_hosts
```
Next you can connect to your Raspberry Pi. Launch the VS Code command palette using Ctrl+Shift+P on Linux or Windows, or Cmd+Shift+P on macOS. Search for and select Remote SSH: Connect current window to host (there’s also a connect to host option that will create a new window).




When VS Code starts I can link it to my personal settings but this fucks up terminal so 
then I need to setup ohmyzsh and power10k
Have to install zsh on the pi
```
sudo apt install zsh

$ zsh --version

$ echo $SHELL
$ chsh -s $(which zsh) 
or 
$ chsh -s /usr/bin/zsh


```
The restart vscode not just the terminal
Choose system admin settings 

Install the fonts
$ mkdir ~/.local/share/fonts
copy fonts there
$ fc-cache -f -v


Then install powerlevel10k
```
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```
1. set ZSH_THEME="powerlevel10k/powerlevel10k" in ~/.zshrc.

Visual Studio Code: Open File → Preferences → Settings (PC) or Code → Preferences → Settings (Mac), enter terminal.integrated.fontFamily in the search box at the top of Settings tab and set the value below to MesloLGS NF.

Upgrade Pygame
```
pip install pygame --upgrade
```

Install Menlo font
```
sudo mkdir /usr/share/fonts/truetype/newfonts
sudo cp ./fonts/*  /usr/share/fonts/truetype/newfonts
fc-cache -f -v
fc-list

#may need to install 
sudo apt install libsdl2-ttf-2.0-0
```