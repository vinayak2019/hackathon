from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateDBForm, LoginForm
from molar import Client, ClientConfig
import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent


with open(BASE_DIR / "config.json", "r") as f:
    CONFIG = json.load(f)


# view for database creation
def create_db(request):
    if request.method == "POST":
        form = CreateDBForm(request.POST)
        if form.is_valid():
            try:
                # get form data
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                full_name = form.cleaned_data["full_name"]
                db_schema = form.cleaned_data["database_schema"]
                db_name = form.cleaned_data["database_name"]

                # create user and database
                user_cfg = ClientConfig(server_url=CONFIG["server_url"],
                                        email=email,
                                        password=password,
                                        database_name=db_name)
                global user_client
                user_client = Client(user_cfg)
                user_client.database_creation_request(
                    superuser_fullname=full_name,
                    alembic_revisions=["{}@head".format(db_schema)])

                # approve the database
                admin_cfg = ClientConfig(server_url=CONFIG["server_url"],
                                        email=CONFIG["admin_email"],
                                        password=CONFIG["admin_password"],
                                        database_name='main')
                admin_client = Client(admin_cfg)
                admin_client.test_token()
                admin_client.approve_database(db_name)
                msg = "Created database {}".format(db_name)
            except:
                msg = "Error creating the database. Try again"

    else:
        form = CreateDBForm()
        msg = ""
    return render(request=request, template_name="create_db.html", context={"form": form,"msg":msg})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            # get form data
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            db_name = form.cleaned_data["database"]

            # create user and database
            user_cfg = ClientConfig(server_url=CONFIG["server_url"],
                                    email=email,
                                    password=password,
                                    database_name=db_name)
            global user_client
            user_client = Client(user_cfg)

            try:
                user_client.test_token()
                request.session["is_authenticated"] = True
                return redirect("/add_data/")
            except:
                msg = "Login Error"
        else:
            msg ="Login Error"

    else:
        form = LoginForm()
        msg = ""

    return render(request=request, template_name="login.html", context={"form": form,"msg":msg})

def view_data(request):
    if request.session.get("is_authenticated",):
        try:
            types = user_client.get_database_information().table_name.to_list()
            table = user_client.query_database(types=types[0])
            table.fillna('',inplace=True)
            return render(request=request,template_name="data.html",
                          context={"table": json.dumps(table.to_dict('records')),
                                   "table_headers": table.columns.tolist()})
        except:
            return redirect("/login/")
    else:
        return redirect("/login/")

def add_data(request):

    if request.session.get("is_authenticated", ):
        try:
            table = user_client.get_database_information()
            return render(request, template_name="add.html",context={"table_headers": table.column_name.to_list()})
        except:
            return redirect("/login/")
    else:
        return redirect("/login/")

def insert_data(request):
    if request.is_ajax():
        d = pd.DataFrame(json.loads(request.POST.get("arr",))).astype(float).to_dict('records')
        types = user_client.get_database_information().table_name.to_list()
        print(d)
        for i in range(len(d)-1):
            print(types[0],d[i])
            user_client.create_entry(type=types[0],data=d[i])
        return redirect("/view_data/")
    else:
        return redirect("/add_data/")