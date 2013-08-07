      ___           ___           ___           ___           ___           ___                       ___     
     /\  \         /\  \         /\__\         /\  \         /\__\         /\  \          ___        /\  \    
    /::\  \       /::\  \       /:/  /        /::\  \       /::|  |       /::\  \        /\  \      /::\  \   
   /:/\:\  \     /:/\:\  \     /:/__/        /:/\:\  \     /:|:|  |      /:/\:\  \       \:\  \    /:/\:\  \  
  /::\~\:\  \   /::\~\:\  \   /::\__\____   /::\~\:\  \   /:/|:|  |__   /:/  \:\  \      /::\__\  /:/  \:\  \ 
 /:/\:\ \:\__\ /:/\:\ \:\__\ /:/\:::::\__\ /:/\:\ \:\__\ /:/ |:| /\__\ /:/__/ \:\__\  __/:/\/__/ /:/__/ \:\__\
 \/__\:\/:/  / \/_|::\/:/  / \/_/|:|~|     \/__\:\/:/  / \/__|:|/:/  / \:\  \ /:/  / /\/:/  /    \:\  \ /:/  /
      \::/  /     |:|::/  /      |:| |          \::/  /      |:/:/  /   \:\  /:/  /  \::/__/      \:\  /:/  / 
      /:/  /      |:|\/__/       |:| |          /:/  /       |::/  /     \:\/:/  /    \:\__\       \:\/:/  /  
     /:/  /       |:|  |         |:| |         /:/  /        |:/  /       \::/  /      \/__/        \::/__/   
     \/__/         \|__|          \|_|         \/__/         \/__/         \/__/                     ``       

ARKANOID:

Setup Instructions:  To setup game as a .exe file
    Run Cipher Levels.py
    Run cmd.exe
    Change Drive letter as appropriate
    Change Directory as appropriate
    type "python setup.py py2exe" when in the same directory as setup.py file
    Delete the build folder
    Move the following into the dist Folder
        Images Folder
        Levels Folder
        Sounds Folder
        cour.ttf
    Delete the from the dist Folder following:
        Any and all Photoshop files in the folders
            Images\Backgrounds\Background.psd
            Images\Backgrounds\Border\Border.psd
            Images\Sprites\Icons\Combo.psd
            Images\Sprites\Icons\icons.psd
            Images\Sprites\Paddles & Ammunition\Portal.psd
        Levels/Unciphered
        Images/Sprites/Paddles & Ammunition/Paddle ~ x0.75 - LASER(unused).bmp
        Images/Sprites/Paddles & Ammunition/Paddle ~ x1.0 - LASER(unused).bmp
        Images/Sprites/Paddles & Ammunition/Paddle ~ x1.5 - LASER(unused).bmp
        Images/Sprites/Paddles & Ammunition/Paddle ~ x2.0 - LASER(unused).bmp
    Change the Icon for the Main.exe file to Images/Icon.ico
    Change the name for the Main.exe file to ~Arkanoid.exe
    Rename the dist Folder to Arkanoid
