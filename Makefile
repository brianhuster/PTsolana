seahorse:
	@cd blockchain && seahorse build

anchor-fix:
	@python ./tools/anchor_fix.py blockchain/programs/blockchain/src

solana: seahorse anchor-fix
	
setup:
	@python3 -m venv venv
	@venv/bin/pip install -r backend/requirements.txt
	@cd frontend && npm install

run-backend:
	@venv/bin/python ./backend/main.py

run-frontend:
	@cd frontend && npm run dev


