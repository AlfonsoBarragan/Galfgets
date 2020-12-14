# In $1 you should put the key that prompts the error in terminal

gpg --keyserver hkp://keys.gnupg.net --recv-key ${1:${#1}-8}
gpg -a --export $1 | sudo apt-key add -

