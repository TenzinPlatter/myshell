#!/bin/bash

cwd=$(pwd)
io_files_dir=""

if [[ ${cwd} == *"tests" ]]; then
	tests_dir="${cwd}"
else
	tests_dir="${cwd}/tests"
fi

mysh_path="${tests_dir}/../mysh.py"

last_diff="${tests_dir}/curr.out"


# BUILTIN SECTION
builtin_dir="${tests_dir}/builtin_tests"

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/exit.in") "${builtin_dir}/exit.out" > /dev/null; then
	echo "Exit test passed (No args)"
else
	echo "Exit test failed (No args), see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/exit.in") "${builtin_dir}/exit.out"
fi

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/which1.in") "${builtin_dir}/which1.out" > /dev/null; then
	echo "Which test 1 passed (1 arg)"
else
	echo "Which test 1 failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/which1.in") "${builtin_dir}/which1.out"
fi

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/which2.in") "${builtin_dir}/which2.out" > /dev/null; then
	echo "Which test 2 passed (2 arg)"
else
	echo "Which test 2 failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/which2.in") "${builtin_dir}/which2.out"
fi

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/pwd.in") "${builtin_dir}/pwd.out" > /dev/null; then
	echo "pwd test passed"
else
	echo "pwd test failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/pwd.in") "${builtin_dir}/pwd.out"
fi

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/cd.in") "${builtin_dir}/cd.out" > /dev/null; then
	echo "cd test passed"
else
	echo "cd test failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${builtin_dir}/cd.in") "${builtin_dir}/cd.out"
fi

echo


# EXECUTABLES SECTION
executable_dir="${tests_dir}/executable_tests"

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${executable_dir}/echo.in") "${executable_dir}/echo.out" > /dev/null; then
	echo "Echo test passed"
else
	echo "Echo test failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${executable_dir}/echo.in") "${executable_dir}/echo.out"
fi

echo

if diff --ignore-trailing-space <(python3 ${mysh_path} < "${executable_dir}/exec.in") "${executable_dir}/exec.out" > /dev/null; then
	echo "Executable test passed"
else
	echo "Try running testing script from root dir"
	echo "Executable test failed, see diff:"
	diff --ignore-trailing-space <(python3 ${mysh_path} < "${executable_dir}/exec.in") "${executable_dir}/exec.out"
fi

echo
