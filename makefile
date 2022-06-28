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