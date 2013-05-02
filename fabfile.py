import os.path

from functools import wraps
from fabric.api import *
from fabric.contrib.files import exists


env['nbsap_target_defs'] = {
    'staging': {
        'host_string': 'edw@rom.edw.ro',
        'nbsap_repo':     '/var/local/nbsap-django',
        'nbsap_sandbox':  '/var/local/nbsap-django/sandbox',
        'nbsap_instance': '/var/local/nbsap-django',
        'nbsap_clients': [
            'burundi',
            'cameroun',
            'benin',
            'niger',
            'madagascar',
            'rdc',
            'burkinafaso',
            'cotedivoire',
            'comifac',
            'algerie',
            'cbd',
            'maroc',
            'training'
        ]

    },
}

env['nbsap_default_target'] = 'staging'

def choose_target(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.pop('target', None)
        if name is None and 'nbsap_target' not in env:
            name = env['nbsap_default_target']

        if name is None:
            target_env = {}
        else:
            target_env = env['nbsap_target_defs'][name]
            target_env['nbsap_target'] = name

        with settings(**target_env):
            return func(*args, **kwargs)

    return wrapper


@task
@choose_target
def install():
    if not exists("%(nbsap_repo)s/.git" % env):
        run("git init '%(nbsap_repo)s'" % env)

    local("git push -f '%(host_string)s:%(nbsap_repo)s' HEAD:incoming" % env)
    with cd(env['nbsap_repo']):
        run("git reset incoming --hard")

    if not exists(env['nbsap_sandbox']):
        run("virtualenv -p /var/local/python27/bin/python --no-site-packages '%(nbsap_sandbox)s'" % env)
        run("echo '*' > '%(nbsap_sandbox)s/.gitignore'" % env)

    run("%(nbsap_sandbox)s/bin/pip install -U distribute" % env)

    run("%(nbsap_sandbox)s/bin/pip install "
        "-r %(nbsap_repo)s/requirements.txt"
        % env)

    run("%(nbsap_sandbox)s/bin/pip install -e %(nbsap_repo)s" % env)


def supervisor(root, command):
    run('%s/sandbox/bin/supervisorctl %s' %
        (root, command))


@task
@choose_target
def restart():
    supervisor(env['nbsap_repo'], "restart nbsap")


@task
@choose_target
def restart_all():
    # restart main NBSAP machine
    execute('restart')
    for country in env['nbsap_clients']:
        supervisor(env['nbsap_repo'], "restart nbsap-%s" % country)


@task
@choose_target
def status():
    supervisor(env['nbsap_repo'],"status")
