# This is the default behaviour
foo:
	@echo "called without arguments"
	@echo "   to make model trainning run make train"
	@echo "   to make prediction run make predict"

# Section for aliases
clean_preprocess: clean preprocess

train: evaluate

merge: data/02_merged_data/merged_file.vcf.gz

preprocess: model/preprocess

predict: 

# Command to remove output intermediate files
clean:
	rm model/preprocess_predict  || echo ok
	rm model/preprocess  || echo ok
	rm data/01*/*.gz || echo ok
	rm data/04*/*.gz || echo ok
	rm test || echo ok

# trainning pipeline
evaluate: data/02_merged_data/merged_file.vcf.gz
	@echo ""
	@echo "   The train process has begun..."
	@env python3 code_python/continent_train_predict.py

data/02_merged_data/merged_file.vcf.gz: model/preprocess data/01_preprocessed_data/*gz
	@echo ""
	@echo "   The merge process has begun, it can take some time to complete"
	@env python3 code_python/files_merge.py

model/preprocess: data/00_data_ingestion/*
	@echo ""
	@echo "   Preprocessing the input files"
	@bash code_bash/mass_preprocess.bash
	@echo "preprocess completed, now all converted files must be in data/01_preprocessed_data/"
	@echo "this file is for workflow control, you can ignore it" > model/preprocess
	@date >> model/preprocess

data/01_preprocessed_data/%.csv.vcf.gz: data/00_data_ingestion/%.csv
	bash code_bash/preprocessing.bash $<
	#vcf-validator $@ >> test

data/01_preprocessed_data/%.vcf.gz: data/00_data_ingestion/%.vcf.gz
	bash code_bash/preprocessing.bash $<
	#vcf-validator $@ >> test

# Command for sample.vcf.gz creation
data/04_prediction_preprocessed/00000000-sample.vcf.gz: data/02_merged_data/merged_file.vcf.gz
	bash code_bash/create_sample_vcf.bash

# Commands for data prediction
predict: data/05_merged_to_predict/merged_file.vcf.gz
	@env python3 code_python/continent_predict.py

data/05_merged_to_predict/merged_file.vcf.gz: data/04_prediction_preprocessed/00000000-sample.vcf.gz model/preprocess_predict data/04_prediction_preprocessed/*gz
	@echo ""
	@echo "   The merge process has begun, it can take some time to complete"
	@env python3 code_python/files_merge.py predict

model/preprocess_predict: data/03_data_to_predict/*
	@echo ""
	@echo "   Preprocessing the input prediction files"
	@bash code_bash/mass_preprocess.bash predict
	@echo "preprocess completed, now all converted files must be in data/04_prediction_preprocessed/"
	@echo "this file is for workflow control, you can ignore it" > model/preprocess_predict
	@date >> model/preprocess_predict

data/04_prediction_preprocessed/%.csv.vcf.gz: data/03_data_to_predict/%.csv
	bash code_bash/preprocessing.bash $< predict
	#vcf-validator $@ >> test

data/04_prediction_preprocessed/%.vcf.gz: data/03_data_to_predict/%.vcf.gz
	bash code_bash/preprocessing.bash $< predict
	#vcf-validator $@ >> test

# Command to test required dependencies
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
