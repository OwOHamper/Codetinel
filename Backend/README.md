Create virtual environemnt

python -m venv ./venv

activate it 

./venv/scripts/activate


install requirements if not install
pytohn -m pip install -r ./requirements.txt

run
fastapi dev main.py #for now developer
fastapi run main.py #production

You also need to have mongodb installed