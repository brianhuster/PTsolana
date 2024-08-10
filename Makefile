build:
	@templ generate
	@go build -o bin/server.exe cmd/*.go

run: build
	bin/server.exe
	
css-watch:
	@tailwindcss -i css/input.css -o static/css/output.css --watch

setup-py-linux:
	@python3 -m venv venv
	@venv/bin/pip install -r requirements.txt

py-run:
	@venv/bin/python blockchain/client/main.py