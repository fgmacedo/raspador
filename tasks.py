from invoke import run, task


@task
def limpar():
    run('git clean -Xfd')


@task
def testar():
    test_cmd = 'nosetests'
    flake_cmd = 'flake8 --ignore=W801,E128,E501,W402'

    # run('{} raspador tests'.format(flake_cmd))
    run('{} tests'.format(test_cmd))
