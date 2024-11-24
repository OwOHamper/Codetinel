Create virtual environemnt

python -m venv ./venv

activate it 

./venv/scripts/activate


install requirements if not install
pytohn -m pip install -r ./requirements.txt

// you may need to resolve some depencey issue, removce them, istall some microsoft build tools... (sorry)


cd datas
git clone https://github.com/juice-shop/juice-shop
NOTE: you have to clone the repo manually on the server, because of the poor connection here, it can't clone it automatically

run
fastapi dev main.py #for now developer
fastapi run main.py #production

You also need to have mongodb installed

