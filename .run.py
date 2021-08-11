# run _test.py
# actually i use batch script instead

if __name__ == '__main__':
    from os import chdir, system

    chdir(__file__[:-11])
    system('python -m GB._test')

    # input('\a')
    input('done')
