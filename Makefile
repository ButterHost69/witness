build:
	pyinstaller --specpath ./out/spec --distpath ./out/dist --workpath ./out/build --icon=../../assets/logo.ico  main.py --onefile