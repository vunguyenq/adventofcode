.SILENT: help

test_param:
	echo $(param)

help:
	echo Run make on a BASH shell
	echo Create new day code: make create dayname="01 day1_title"
	echo Delete day: make delete day=01

create:
	touch input/input$(word 1, $(dayname)).txt
	touch input/input_test$(word 1, $(dayname)).txt
	cp code-template.py $(word 1, $(dayname)).$(word 2, $(dayname)).py
	sed -i 's/INPUT_TEST_FILE/input_test$(word 1, $(dayname))/g' $(word 1, $(dayname)).$(word 2, $(dayname)).py
	sed -i 's/INPUT_REAL_FILE/input$(word 1, $(dayname))/g' $(word 1, $(dayname)).$(word 2, $(dayname)).py

delete:
	echo Removing the following files: $(day)*.py ./input/input_test$(day).txt ./input/input$(day).txt 
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} == y ]
	rm ./input/input$(day)*.txt
	rm ./input/input_test$(day)*.txt
	rm $(day)*.py
