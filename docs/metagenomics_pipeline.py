# 1. eliminate sequences with N's (if one pair has an N, eliminate both pairs) and create two fasta files for each pairs.
#    ssh minnie
#    cd /storage-0/hiseq/20110912/Unaligned/HMP_metagen/merens_tmp
#    there you will find run scripts for this.
#
# 2. split first lane into smaller pieces.
#    examples are in /xraid2-2/g454/hmp/metagenomics
#    ./01_initialize_parts.sh 
#
# 3. search R1 against human genome
#
#    02_search_against_HUMAN.sh
# 
# 4. concatenate results into one b6 file and filter hits
#
#    03_finalize_HUMAN.sh
#
# 5. create four FASTA files from the resulting hits:
#    1. R1_human_hits
#    2. R2_human_hits (matching pairs)
#    3. R1 (everything that didn't have a hit to human genome)
#    4. R2 (mathing pairs of R1)
#
# 6. search R2 against human genome, concatenate results, and filter hits (what should happen to no hits?).
#
# 7. take 5.3 and 5.4 and perform 1-6 on those against refSSU, create a taxonomy list upload it to VAMPS.
#
# 8. take 7.3 and 7.4 and perform everything to those against bacterial genomes. concatenate results, and filter hits.
#
# 9. dynamically trim reads to elimnate not aligning pieces.
#
#
# 10. crete individual fasta files for matching genomes. perform assembly separately on each bin.
#
# 11. search individually assembled genomic bins against widely available protein databases.
#
#
#
