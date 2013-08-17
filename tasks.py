from invoke import run, task


@task
def limpar():
    run('git clean -Xfd')


@task
def testar():
    commands = ['nosetests', 'flake8']
    for c in commands:
        run('{} raspador tests'.format(c))
