# Readme sections

- [Clustering method:](#Clustering-method)

- [File structure](#File-structure)

- [Pipeline](#Pipeline)

- [Code](#Code)

# Clustering method

This is an overview of the clustering method used and the most relevant files involved in each stage. In a general landscape of the process, each file is sorted and converted to vcf format, then merged into a new vcf file to be then converted into a matrix where each column represents the original characteristics. The last stage of the clustering consists of a dimensional reduction using PCA and a final clustering using KMeans.

The data cleaning, sorting, and conversion are realized and described in [bash_code/preprocessing.bash](bash_code/preprocessing.bash) and have an auxiliary code in [bash_code/mass_preprocessing.bash](bash_code/mass_preprocessing.bash) which is used by the makefile and is the responsible for start the preprocessing of the input files which can be stored on [data/00_data_ingestion/](data/00_data_ingestion/) to be used to train the model or [data/03_data_to_predict/](data/03_data_to_predict/) to be used only for prediction of the continent. The complete [pipeline](#Pipeline) can be read on his section.

The process to merge all the input data is realized by [code_python/files_merge.py](code_python/files_merge.py) which starts the merging process using all the available cores in parallel to merge the input vcf files by pairs until all the data has been merged into a final vcf. This output file preserves only the SNPs which are common for all the input data.

The following stages are realized by [code_python/continent_train_predict.py](code_python/continent_train_predict.py) and described in the next sub-sections.

## Data matrix

At this point in the merged vcf, the first 9 columns store information to identify each data retrieved from the genetic code, and the rest of the columns represent the specific allele shown for a certain individual for each copy of the genetic code. For a specific individual, all this information can be seen as a vector with entries which are strings, this string can't be used directly but can be converted into new 2-dimensional data using a modified one-hot encoding described in [data_python/helpers/encoder.py](data_python/helpers/encoder.py).

In this way, each individual can be represented by a vector of numbers between 0 and 1 which represents how strong is the presence of a specific allele for a specific position (0 if this allele is absent, 0.5 if there is only one copy, and 1 if there are two copies of this allele). The final data matrix represents with each column one of these individuals.

## PCA

The resulting matrix has a very high dimension, so to reduce the clustering complexity an intermediate stage of PCA was applied. This process reduces the dimensions from around 4000 to 500 keeping the most important information to understand the data behavior.

## KMeans

KMeans is a clustering technique by similarity, this machine learning method makes partitions on the space in an unsupervised way which means that we know the number of partitions but don't know the meaning of each partition, so we should decide the meaning by studying the final results.

This process is realized by [data_python/helpers/kmeans.py](data_python/helpers/kmeans.py) dividing the space into seven groups which are compared with the labeled data to decide the meaning of each partition.

The best result is obtained when the space is divided into eight groups, but most of the time this process generates an ethnical group not represented in the labeled data sometimes in Africa and sometimes in East Asia.

# Pipeline

# File structure

# Code
