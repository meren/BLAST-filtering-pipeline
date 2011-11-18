README
======

This code base contains a very early draft of what it promises. So, it might be a good idea to ignore this project for now.


Aim
___

Well. One of the problems I was dealing with while I was working with shotgun metagenomics data obtained from Illumina was to filter out certain things from millions of sequences to get them to a point where I can start analyzing them. For instance, in the context of metagenomics, what a researcher might want to do right after quality control and right before assembling longer contigs from her sequences is to filter out reads that are coming from other sources such as human genome, or viral genomes. Moreover, she might like to filter out 16S rRNA genes from this collection of reads in order to analyze taxonomy separately and/or simply to reduce the size of reads.

Basically in my work-flow what happens to my metagenomic data is that it gets more and more refined by being searched against a database. For instance all reads are being searched against Human genome, good hits are being collected from the original file, remaining sequences are being searched against a collection of Viral DNAs, etc. Obviously it is possible to generalize these steps and implement a layer of abstraction to have computer deal with the input and output files, as well as pesky intermediate steps; and this is the intention of this small project.

It is absoultely not there yet, but my aim is to develop this pipeline to a point where running it would be as easy as calling it like this (for a paired-end illumina run):

    $ python bpline.py --r1 /path/to/pair_1.fa --r2 /path/to/pair_2.fa -o /path/to/output -s filters-config.ini


Filters Configuration
_____________________

Filters are going to be defined in a configuration file. Here is a sample:

    [/path/to/a/search/database/human_genome.wdb]
    filter_name = Human
    cmdline="usearch -query %(query)s -blast6out %(blast6out)s -wdb %(db)s"
    
    [/path/to/another/search/database/reference_SSU.db]
    filter_name = rRNA
    cmdline="blastall -i %(query)s -d %(db)s -o %(blast.out) -m 8"
    
    [/path/to/a/search/database/viral_genomes.wdb]
    filter_name = Viral
    cmdline="usearch -query %(query)s -blast6out %(blast6out)s -wdb %(db)s"


More explanation about the structure of the configuration file will be here.


Flow
____

Basically this is what is going to be happening when someone runs the pipeline:

1. Parse `filters-config.ini` to generate a chain of filters.
2. For the first filter, input is `--r1` and `--r2`.
3. Search every sequence in the input against the `database` defined in the `filters-config.ini` for this filter and create a tabular output of hits (it is the output you get when you run blastall with `-m 8`)
4. Analyze input files in respect to the tabular search output, and according to the criteria defined in config, separate sequences that have _good hits_ and store them in their own files.
5. If there is another filter, send sequences that _didn not result a good hit to the current filter_ as the input to the next filter: Go to 3.
6. Else, report everything.


Contact
_______

You can reach [me](http://meren.org) via `meren / mbl.edu`. All suggestions and critiques are most welcome.

Thanks.
