#build in venv activate for low file size
build:
	pyinstaller --specpath ./out/spec --distpath ./out/dist --workpath ./out/build --icon=../../assets/logo.ico  main.py --onefile
	