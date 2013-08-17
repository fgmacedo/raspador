from invoke import run, task


@task
def clean():
    run('git clean -Xfd')


@task
def test():
    commands = ['nosetests', 'flake8']
    for c in commands:
        run('{} raspador tests'.format(c))
