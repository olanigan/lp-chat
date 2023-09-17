install:
	python3 -m pip install --upgrade pip && pip install -q -r requirements.txt

run:
	streamlit run app.py