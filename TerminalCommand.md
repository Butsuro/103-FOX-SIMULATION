pyinstaller --onefile --hidden-import=math \
--add-data="data.json:." \
--add-data="simoutput.json:." \
--add-data="assets/background.png:assets" \
--add-data="assets/enc1.png:assets" \
--add-data="assets/enc2.png:assets" \
--add-data="assets/enc3.png:assets" \
--add-data="assets/mainbackground.png:assets" \
--add-data="assets/smalltree.png:assets" \
Main.py
