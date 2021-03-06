Product owner:
-------
    * Franz Daffner
    * franz.daffner@eea.europa.eu

Min. hardware resources
-------

    * [CPU] Single Core >= 2.5 GHz
    * [RAM] 1024 MB
    * [Hard disc] current necessary < 1 GB
    * [Hard disc] 6 months forecast <= 20 GB
    * [NIC] 100 Mbit

About
-------
National Biodiversity Strategies and Action Plan (or simply NBSAP)
is a platform for organizing the implementation of a country's
national biodiversity strategy after AICHI (and by case after EU Strategy).
It consists of two panels each corresponding an operation: viewing and editing.

The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its
own strategy in terms of objectives and actions) and its implementation.

The second panel(Admin), authentication-available only, allows an user to actually define
the national strategy. (e.g. add/modify/delete an objective, action or even
elements from AICHI) in the purpose of building it.



NBSAP Quick Installation Guide
=====
0. Prerequisites packages if missing::

    python-setuptools python-dev mysql-server libmysqlclient-dev virtualenv
    Python 2.7.3 - compiled or by native system


1. Clone the repository::

    git clone git@github.com:eea/nbsap.git nbsap
    cd nbsap


2. Create & activate a virtual environment (with Pyhon 2.7.3)::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    . sandbox/bin/activate


3. Install dependecies & others::

    pip install -U distribute
    pip install -r requirements.txt
    pip install -e .


4. Setup local-settings.py::
   Assuming the root of your project is ROOT_PROJECT, copy the following file ROOT_PROJECT/instance/local_settings.py.example to ROOT_PROJECT/instance/local_settings.py


5. Setup database - see section below::


6. Run the tests to check the validity of your installation::
    ./instance/manage.py test nbsap




7. Run a test server(see http://127.0.0.1:8000 afterwards)::
    ./instance/manage.py runserver



MySQL Database deployment
=====
0. To set the database, check prerequisites and dependecies::


1. Then create and configure database as follows::
    create database nbsap DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    grant all on nbsap.* to nbsap@localhost identified by 'nbsap';


2.  Allow Django to automatically create all tables by doing the following::
    ./instance/manage.py syncdb
    ./instance/manage.py load_fixtures



Production deployment
=====
0. Copy and adjust env dict in fabfile.py.sample::

1.1. Deploy code on remote host::
    fab install

1.2. Login on remote machine and activate the sandbox::


1.3 Setup the database as above

2. Configure supervisord.conf (see sample) in root::


3. Start supervisor daemon(make sure to have its conf file in path - e.g. place it in sandbox)::
    supervisord

4. Use supervisor controller to control the application::
    supervisorctl


i18n deployment
=====
0. For translations there are two methods.

1. Manual translation
1.1 Run over the entire source tree and pull out all strings marked for translation::
    cd src/nbsap
    django-admin.py makemessages -a


1.2 Edit <msgstr> for each <msgid> in nbsap/locale/_LANGUAGE_/LC_MESSAGE/django.po


1.3 Compile .po file created with previous command::
    cd src/nbsap
    django-admin.py compilemessages


1.4 Restart testing server::
    ./instance/manage.py runserver

2. Automatic translation::
2.1 Make sure 'DEBUG = True' in the instance/local_settings.py - to automatically generate an admin user

2.1 Surf over http://127.0.0.1:8000/translate to use Rosetta tool for translation

2.2 Complete the forms within the correct translations

2.3 Restart testing server::
    ./instance/manage.py runserver


Create new nbsap instance
=========================

1. Create instance folder::
    sudo su - edw
    cd /var/local/nbsap-django/
    mkdir instance_<country>

2. Copy config files::
    cp /var/local/nbsap-django/local_settings.py.example /var/local/nbsap-django/instance_<country>/local_settings.py
    cp /var/local/nbsap-django/manage.py /var/local/nbsap-django/instance_<country>/manage.py
    # edit database info in local_settings.py
    vim /var/local/nbsap-django/instance_<country>/local_settings.py

3. Create database::
    mysql -u root -p
    mysql> create database nbsap_<country> DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    mysql> grant all on nbsap_<country>.* to nbsap@localhost identified by 'nbsap';

4. Create tables::
    # activate virtualenv
    . /var/local/nbsap-django/sandbox/bin/activate
    ./var/local/nbsap-django/instance_<country>/manage.py syncdb
    ./var/local/nbsap-django/instance_<country>/manage.py load_fixtures

5. Start process using supervisor::
    # edit supervisord.conf based on /var/local/nbsap-django/supervisord.conf.sample
    vim /var/local/nbsap-django/sandbox/supervisord.conf
    supervisord
    supervisorctl
    supervisorctl> reread
    supervisorctl> update

6. Configure apache::
    # edit apache conf file as root
    vim /etc/httpd/conf.d/nbsap.conf
