from SaveLoad import savegame
from SaveLoad import loadgame
print """
  _____         __                          .__    .___
  /  _  \_______|  | _______     ____   ____ |__| __| _/
 /  /_\  \_  __ \  |/ /\__  \   /    \ /  _ \|  |/ __ | 
/    |    \  | \/    <  / __ \_|   |  (  <_> )  / /_/ | 
\____|__  /__|  |__|_ \(____  /|___|  /\____/|__\____ | 
        \/           \/     \/      \/               \/ 
"""
print """
                                 ______________
  ____             _____ _      /___   ________)
 |  _ \       _   / ____(_)         | |____
 | |_) |_   _(_) | (___  _ _ __     | _____)
 |  _ <| | | |    \___ \| | '__|    | |
 | |_) | |_| |_   ____) | | |  __   | |
 |____/ \__, (_) |_____/|_|_| / /___| |
         __/ |                \______/
        |___/         
"""
print "Ciphering in progress"
#Ciphers all the levels in the Levels/Unciphered/ folder from 1 to 12
# also ciphers the highscores file
#this allows for level editing before distribution, the unciphered folder as well as this file is not distributed
for filename in range(1,16):
    print "Ciphering LVL %i" % (filename)
    filename = str(filename) + ".txt"
    savegame("Levels/" + filename, loadgame("Levels/Unciphered/" + filename, tocipher = False))
    
print "Ciphering Highscores"
filename = "Highscore.txt"
savegame("Levels/" + filename, loadgame("Levels/Unciphered/" + filename, tocipher = False))
print "Done"