"""This module is a wrapper that runs the scripts that generate figures using
PyFig.  If errors occur, full Tracebacks of the errors are sent to standard
out."""
from __future__ import print_function
from sys import stderr, stdout, version_info
from subprocess import Popen, PIPE
from os.path import sep, splitext

if version_info[0] < 3:
   py_vers='python'
else:
   py_vers='python3'

exampleList = [
    './00_helloworld.py',
    './01_singleplot.py',
    './02_multiplot.py',
    './03_simplesubclass.py',
    './04_classy.py',
    './05_colorplot.py',
    './06_logautoscale.py',
    './07_panels.py',
    './08_latexlabels.py',
    './09_datasets.py',
    './10_dataset_features.py',
    './11_network.py',
    './12_cheatsheet.py',
    './13_directed_network.py',
    './14_phylogenetic_tree.py',
    ]

if __name__ == '__main__':
    PYTHON_PATH = '/usr/bin/env '+py_vers 
    SHOW_DETAILED_ERROR_OUTPUT = True

    # output title message to shell
    print(('Running tests ' + '-' * 80)[:79], file=stderr)

    # initialize counters
    testNumber = 1
    nWork = 0
    nTests = len(exampleList)

    # run tests ---------------------------------------------------------------
    for scriptPath in exampleList:

        # extract script path
        print( '%3i) %-67s' % (testNumber, scriptPath), file=stderr)

        # try to make figure using pyfig script (execute in shell)
        command = '%s %s' % (PYTHON_PATH, scriptPath)
        childProcess = Popen(command, shell=True, stderr=PIPE)

        # write output of error stream
        errorOutput = childProcess.stderr.read()
        if errorOutput:
            root, ext = splitext(scriptPath)
            errorStream = open('%s.log' % root, 'w')
            errorStream.write(str(errorOutput))
            errorStream.close()
        
        # tell the shell whether the script successfully ran
        if childProcess.wait():
            print('failed', file=stderr)
        else:
            print('passed', file=stderr)
            nWork += 1

        testNumber += 1

    # print output to shell depending on results of tests ---------------------
    if nWork == nTests:
        allPassed = 'PASSED'
    else:
        allPassed = 'FAILED'

    message = '\nTests %s: %i of %i were successful.' % \
              (allPassed, nWork, nTests)
    print(message, file=stderr)

    if allPassed == 'FAILED' and SHOW_DETAILED_ERROR_OUTPUT:

        message = """
The output of standard error for each test script are stored in the same file
as the output with a .log extension."""
        print(message, file=stderr)

    if allPassed == 'PASSED':

        message = """
All of the test scripts successfully ran, but make sure to check the figures
that were created, as they may not look right even though the scripts did not
throw an error."""
        print(message, file=stderr)
