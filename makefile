foo:

clean_preprocess: clean preprocess

clean:
	rm data/01*/*.gz || echo ok
	rm test || echo ok

merge: data/01_preprocessed_data/*gz
	echo "the merge process has begun, it can take some time to complete"
	env python3 code_python/files_merge.py

preprocess:
	bash code_bash/mass_preprocess.bash
	@ echo "preprocess completed, now all converted files must be in data/01_preprocessed_data/"

data/01_preprocessed_data/%.csv.vcf.gz: data/00_data_ingestion/%.csv
	bash code_bash/preprocessing.bash $<
	#vcf-validator $@ >> test

data/01_preprocessed_data/%.vcf.gz: data/00_data_ingestion/%.vcf.gz
	bash code_bash/preprocessing.bash $<
	#vcf-validator $@ >> test

test:
	@command -v bash && echo "Bash installed correctly\n" || echo "Bash is not installed and we need it to continue"
	@command -v bash >/dev/null
	@bash code_bash/command_test.bash awk awk
	@bash code_bash/command_test.bash env env
	@bash code_bash/command_test.bash file "'file' command"
	@bash code_bash/command_test.bash ln ln
	@bash code_bash/command_test.bash python3 Python3
	@bash code_bash/command_test.bash sed sed
	@bash code_bash/command_test.bash sort sort
	@echo "At this point all the required programs are installed"
	@echo "testing required python libraries..."
	@env python3 code_python/libraries.py
