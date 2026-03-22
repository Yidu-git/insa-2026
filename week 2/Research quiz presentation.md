Linux user Management
include : user d/t root , access root user, Superuser DO

package installation on Linux
include apt, pkg, pacman
- script installation
- software installation
- shell
include: types
- or, piping, and d/t

# Linux user management
Linux is a multi user OS system which means it allows for the existence of multiple users who can use the same machine. Linux user management is about managing permissions of users and groups.
### Users and Root
Regular users have limited permissions. They are only allowed access for daily tasks such as document manipulation.
### Creating users
Create user: 
```shell
sudo adduser <user>
```
Delete user:
```shell
sudo deluser <user> 
```
Change user password:
```shell
sudo passwd <user>
```
### Groups
Linux allows certain permissions to apply to groups of users instead of changing permissions to individual users.

Creating groups:
```shell
sudo groupadd <group>
```
Adding users:
```Shell
sudo usermod -aG <group> <user>
```
Removing users:
```Shell
sudo deluser <user> <group>
```

### Where is user data stored?
Important system files:
- *`/etc/passwd`* : user account info
- *`/etc/shadow`* encrypted passwords
- *`/etc/group`* group definitions
### Changing ownership
Change owner:
```Shell
sudo chown <user> file.txt
```
Change group:
```Shell
sudo chgrp developers file.txt
```
Change permission:
```Shell
chmod 775 script.sh
```
### Sudo access
```Shell
sudo usermod -aG sudo yidu
```
# Package installation
Linux has a different software installation process compared to windows. Instead of installing *`.exe`* files through a GUI (while it is possible using wine), Linux uses commands in the terminal with different methods of installing software.
## Package managers
Package managers (like *`apt`*, *`packman`*, *`pkg`*) are used to manage and install packages. Package managers vary from distro to distro.

To install a package the command to install must start with `sudo` to install the package with elevated permissions.,
Example: 
#### **Debian(Ubuntu/Mint)** :
  *`sudo apt install <package_name>`*
#### **Fedora(RHEL/CentOS)** :
  *`sudo apt install <package_name>`*
#### **Arch Linux/Manjaro** :
  *`pacman -S <package_name>`*
## Software managers
Regular users or users who may not want to use the terminal can install software through pre-installed GUIs (like Gnome) which allow for searching and installing applications. This method is often the safest was to install software.
## Snap and Flatpak
Snap and Flatpak are universal formats that work across distributions.
#### Snap
`sudo snap install <package_name>`
#### Flatpak
`sudo flatpak install <package_name>`
## App images
If a users Linux machine does not have access to internet or is an air gaped system, portable *App images* can be run directly since they don't require installation.
## Manual package installation
Packages can also be downloaded and installed directly depending on the Linux distro used. Example :
#### Debian / Ubuntu
```Shell
sudo dpkg -i package.deb
```
#### Fedora / Red Hat
```shell
sudo rpm -i package.rpm
```
# Linux shell
A Linux shell is a **command-line interpreter** that acts as an interface between a user and the Linux operating system's core, known as the kernel.
## Types of shell
### 1) `Bash` (Bourne Again Shell)
- Default on most Operating Systems
- Easy scripting
- Tab completion
### 2) `Sh` (Bourne Shell)
- Very minimal
- Portable
- Lacks modern features
### 3) `Zsh` (Z shell)
- Advanced auto-completion
- Themes and plugins
- Highly Customizable
### 4) `Fish` (Friendly interactive shell)
- User-friendly syntax
- Built-in suggestions
- No config needed
### 5) `Ksh` (Korn Shell)
- Powerful scripting
- Faster than older shells
### 6) `Csh` / `Tcsh`
- C-like syntax
- Command history improvements
- Not great for scripting
