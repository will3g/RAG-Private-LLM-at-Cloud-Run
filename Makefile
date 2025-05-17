APP_PATH=app/app.py

# Alvo padrão
run: export PYTHONPATH=.
run:
	streamlit run $(APP_PATH)

install:
	pip install -r requirements.txt

format:
	black .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

# Ex: make <command>
