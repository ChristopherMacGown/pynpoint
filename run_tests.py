import sys
import nose

if __name__ == '__main__':
    args = ['nosetests']
    sys.path.append('tests')

    nose.run('tests', argv=args)
