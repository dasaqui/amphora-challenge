foo:

clean_preprocess: clean preprocess

clean:
	rm data/01*/*.gz || echo ok
	rm test || echo ok

preprocess:
	bash code_bash/mass_preprocess.bash

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
	@bash code_bash/command_test.bash file "'file' command"
	@bash code_bash/command_test.bash ln ln
	@bash code_bash/command_test.bash python3 Python3
	@bash code_bash/command_test.bash sed sed
	@bash code_bash/command_test.bash sort sort
	@echo "At this point all the required programs are installed and ready to use"
