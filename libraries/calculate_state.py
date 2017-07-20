#! /usr/bin/python

from ansible.module_utils.basic import *
import re
import subprocess 



# Copied wholesale from python 2.7
def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    b'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    b'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return output


def calculate_state()
    #server-enabled-aws = command
    enabled = check_output(["server-enabled-aws"])
    finished = check_output(["/tmp/is_finished"])
    #figure out script location
    idle = check_output(["is_idle || true"], shell=True)
    is_enabled = re.compile(r'.*Status: enabled.*', re.DOTALL).match(enabled)
    is_finished = re.compile(r'.*finished.*', re.DOTALL).match(finished)
    is_idle = re.compile(r'.*(idle|overdrained).*', re.DOTALL).match(idle)

    state = 'unknown'
    if is_finished and is_enabled:
        state = 'fin'
    elif is_enabled and not is_finished:
        state = 'queued'
    elif not is_enabled and not is_idle and not is_finished:
        state = 'draining'
    elif not is_enabled and is_idle and not is_finished:
        state = 'ready'

    return { 'state': state }

def main():
    module = AnsibleModule(
        argument_spec = dict(
          finished_command = dict(default="", required=False),
        ),
        supports_check_mode = True,
    )
    try:
        state = calculate_state()['state']
    except Exception as err:
        module.fail_json(msg="Failed to calculate system patching state: " + err.__str__())
    else:
        module.exit_json(ansible_facts=dict(patching_state=state))

if __name__ == '__main__':
    main()
