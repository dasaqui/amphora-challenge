foo:

clean_preprocess: clean preprocess

clean:
	rm model/preprocess  || echo ok
	rm data/01*/*.gz || echo ok
	rm test || echo ok

run: evaluate

evaluate: data/02_merged_data/merged_file.vcf.gz
	@echo ""
	@echo "   The train process has begun..."
	@env python3 code_python/continent_prediction.py

merge: data/02_merged_data/merged_file.vcf.gz

data/02_merged_data/merged_file.vcf.gz: model/preprocess data/01_preprocessed_data/*gz
	@echo ""
	@echo "   The merge process has begun, it can take some time to complete"
	@env python3 code_python/files_merge.py

preprocess: model/preprocess

model/preprocess: data/00_data_ingestion/*
	@echo ""
	@echo "   Preprocessing the input files"
	@bash code_bash/mass_preprocess.bash
	@ echo "preprocess completed, now all converted files must be in data/01_preprocessed_data/"
	@echo "this file is for workflow control, you can ignore it" > model/preprocess
	@date >> model/preprocess

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
	@echo "At this point all the required programs are installed, now we are"
	@echo "testing required python libraries..."
	@echo ""
	@env python3 code_python/libraries.py
