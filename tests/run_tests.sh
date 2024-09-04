#!/bin/bash

cwd=$(pwd)
io_files_dir=""

if [[ ${cwd} == *"tests" ]]; then
	tests_dir="${cwd}"
else
	tests_dir="${cwd}/tests"
fi

curr_out="${tests_dir}/curr.out"

exit_dir="${tests_dir}/exit_tests"

diff <(python3 mysh.py < "${exit_dir}/exit.in") "${exit_dir}/exit.out" > ${curr_out}

if ${curr_test_diff}; then
	echo "Exit test (No args) passed"
else
	echo "Exit test (No args) failed, see diff:"
	diff <(python3 mysh.py < "${io_files_dir}/exit.in") "${io_files_dir}/exit.out"
fi
