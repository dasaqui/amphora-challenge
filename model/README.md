# Readme sections

- [Clustering method:](#Clustering-method)

- [Pipeline](#Pipeline)

- [File structure](#File-structure)

# Clustering method

This is an overview of the clustering method used and the most relevant files involved in each stage. In a general landscape of the process, each file is sorted and converted to vcf format, then merged into a new vcf file to be then converted into a matrix where each column represents the original characteristics. The last stage of the clustering consists of a dimensional reduction using PCA and a final clustering using KMeans.

The data cleaning, sorting, and conversion are realized and described in [code_bash/preprocessing.bash](../code_bash/preprocessing.bash) and have an auxiliary code in [code_bash/mass_preprocessing.bash](../code_bash/mass_preprocessing.bash) which is used by the makefile and is the responsible for start the preprocessing of the input files which can be stored on [data/00_data_ingestion/](../data/00_data_ingestion/) to be used to train the model or [data/03_data_to_predict/](../data/03_data_to_predict/) to be used only for prediction of the continent. The complete [pipeline](#Pipeline) can be read on his section.

The process to merge all the input data is realized by [code_python/files_merge.py](../code_python/files_merge.py) which starts the merging process using all the available cores in parallel to merge the input vcf files by pairs until all the data has been merged into a final vcf. This output file preserves only the SNPs which are common for all the input data.

The following stages are realized by [code_python/continent_train_predict.py](../code_python/continent_train_predict.py) and described in the next sub-sections. To predict only this process is realized by [code_python/continent_predict.py](../code_python/continent_predict.py).

## Data matrix

At this point in the merged vcf, the first 9 columns store information to identify each data retrieved from the genetic code, and the rest of the columns represent the specific allele shown for a certain individual for each copy of the genetic code. For a specific individual, all this information can be seen as a vector with entries which are strings, this string can't be used directly but can be converted into new 2-dimensional data using a modified one-hot encoding described in [code_python/helpers/encoder.py](../code_python/helpers/encoder.py).

In this way, each individual can be represented by a vector of numbers between 0 and 1 which represents how strong is the presence of a specific allele for a specific position (0 if this allele is absent, 0.5 if there is only one copy, and 1 if there are two copies of this allele). The final data matrix represents with each column one of these individuals.

## PCA

The resulting matrix has a very high dimension, so to reduce the clustering complexity an intermediate stage of PCA was applied. This process reduces the dimensions from around 4000 to 500 keeping the most important information to understand the data behavior.

## KMeans

KMeans is a clustering technique by similarity, this machine learning method makes partitions on the space in an unsupervised way which means that we know the number of partitions but don't know the meaning of each partition, so we should decide the meaning by studying the final results.

This process is realized by [code_python/helpers/kmeans.py](../code_python/helpers/kmeans.py) dividing the space into seven groups which are compared with the labeled data to decide the meaning of each partition.

The best result is obtained when the space is divided into eight groups, but most of the time this process generates an ethnical group not represented in the labeled data sometimes in Africa and sometimes in East Asia.

# Pipeline

In general terms, there are two pipelines as can be seen in the next image. The first pipeline is to train the model with the provided data stored on [data/00_data_ingestion/](../data/00_data_ingestion/) and ends whit the creation of the model files and a sample vcf which stores the information of the SNPs used to predict data. The second pipeline requires the model files, the sample vcf, and the provided vcf files to predict which must be stored on [data/03_data_to_predict/](../03_data_to_predict/), this pipeline ends by describing as an output text the prediction for each input file.

![](reported/pipeline.png)

In the previous image, we see in purple the input files which the user must provide to change the training or predictions, the file [data/coordination.txt](../coordination.txt) contains the labels for the evaluation while the folders contain the data to train the model or the data to predict. The arrows indicate how the input data travels between folders and codes to the end of the pipeline at the bottom. Each folder represents how the information is stored in intermediate files (inside this folder) and the code files (inside file_'programming language'/ folder) show the file that starts the processing of the respective stage.

# File structure

In the main folder, there are only two files README.md which gives an overview of the project, and makefile which stores instructions for the command 'make' to start each pipeline correctly and try to reduce redundancy (don't repeat an action if the input files are not changed).

## data

This folder stores all the input data and the intermediate stages of the pipeline

- coordinates.txt stores the labels to be used in training, evaluation, and label inference
- 00_data_ingestion/ stores the input files to be used in the training
- 01_preprocessed_data/
- 02_merged_data/ stores the merged data and is the last intermediate stage in the 'train' pipeline
- 03_data_to_predict/ stores the input files to be predicted in the 'predict' pipeline
- 04_prediction_preprocessed/
- 05_merged_to_predict/ stores the merged data and is the last intermediate stage in the 'predict' pipeline

## model

This folder contains this README the trained model files with extension pkl and 'preprocess' flags which are required by makefile to control the code execution, erase these files (except for the README) will force make to run the complete pipeline to train or predict data on the next execution.

- out/ stores the images generated by the last 'train' pipeline execution
- reported/ stores the images and auxiliary files reported for this challenge

## code_awk

AWK is a programming language designed for text processing line by line in sequential order.

- csv2vcf.awk reads an input vcf to convert it into a valid vcf file
- vcf2sample.awk reads the merged vcf file generated by the 'train' pipeline to convert it into a sample vcf which indicates to the next stage which SNPs should be preserved

## code_bash

This folder contains code to control the command line using the programming language bash. The contained files and folders can be divided into three categories pipeline, auxiliary pipeline, and makefile.

- pipeline
-- create_sample_vcf.bash is used to call cvf2sample.awk unzipping and zipping files as required to create the sample vcf
-- preprocessing.bash reads the input arguments to decide which auxiliary file should take care of the input to preprocess it

- auxiliary pipeline
-- preprocess/ folder has to files to make the preprocessing of the input files according to the input format, this task involves creating a valid compressed and sorted vcf.
-- error_flag.bash used by other scripts to log that there was a problem while processing some file

- makefile
-- command_test.bash used by 'make' to check if a command ready to be used in the command line
-- mass_preprocess.bash is used by 'make' to start the preprocessing of the input files one by one using preprocessing.bash

## code_python

This folder contains three groups of codes, so it can be divided into pipeline, modules, auxiliary, and makefile

- pipeline
-- continent_predict.py  reads the 'predict' merged file and the trained model to predict the continent of each sample and show it in the display
-- continent_train_predict.py reads the 'train' merged file to train the model (if it has not been trained before) and evaluates the model performance showing it in a PyPlot graph and saving it in [model/out/](../model/out/)
-- files_merge.py is in charge of the vcf merging process

- modules
-- helpers/ has several tasks in different files which involves encoding (one-hot encode), kmeans training and evaluation, data plotting, and F1 score evaluation. 
-- vcf/ involves tasks to read, write and merge vcf files using pandas to store the information as the internal python representation.

- auxiliary
-- my_constants.py stores some constants needed for different codes involved in the pipeline
-- test_code1.py created to debug the non-parallel merge process
-- test_code2.py created to debug the parallel merge process

- makefile
--libraries.py check for each library needed to run the code and inform if one of them should be installed
