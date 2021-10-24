# MolarDB frontend


## Install instructions
- Install [molar](https://github.com/aspuru-guzik-group/molar) client and backend. You can find the instructions [here](https://molar.readthedocs.io/en/latest/index.html) 
- Create a conda environment with the environment file in the folder. ```conda create -f environment.yml```
- Copy the `.py` files from `schema` folder to `migrations` in the the molar installation directory (default name is `molar_data_dir`).
- Edit the `config.py`. Add the admin email and password used during `molar` installation 
- Make migrations to the django project 
```sh
python manage.py makemigrations 
python manage.py migrate```

## Usage
- Start the backend `molar` sever.
- Run the django server. Do not forget to change the port. Django runs ar `8000` but `molar` uses `8000`
 
```sh
python manage.py runserver 127.0.0.1:8080```

## TODO
