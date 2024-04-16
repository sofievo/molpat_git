import json
from tqdm import tqdm


# Filepaths
NM_path = "/mnt/work/workbench/sofievor/scratch/Research/Database/data/resources/ncbi_func_domains/canonical_NM_accessions.tsv"  # filepath to list of NM_accessions
file_path = "/mnt/work/workbench/sofievor/scratch/Research/Database/data/resources/gene_length/ncbi_dataset/data/product_report.jsonl" # filepath to ncbi product_report.jsonl
out_path = '/mnt/work/workbench/sofievor/scratch/Research/Database/data/resources/gene_length/gene_length_store.tsv'



def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip().split('.')[0] for line in file]
    return lines

# Returns dictionary length = {'NM_*': len, 'NM_*': len, ... }
def find_protein_lengths(file_path, accession_versions):
    # Store protein lengths in a dictionary
    protein_lengths = {version: None for version in accession_versions}

    print('Opening jsonl file')
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Processing lines"):
            gene_record = json.loads(line)
            #gene_symbol = gene_record.get("symbol", "Symbol not found")
            for transcript in gene_record.get('transcripts', []):
                acc_version = transcript.get('accessionVersion')
                # Check if this transcript's accession version is one we're looking for
                if acc_version.split('.')[0] in accession_versions:
                    # Access the protein length
                    protein = transcript.get('protein', {})
                    protein_lengths[acc_version.split('.')[0]] = protein.get('length')
    return protein_lengths



# Get length dictionary
accession_versions = read_file_to_list(NM_path) # read accessions
length = find_protein_lengths(file_path, accession_versions) # read length of protein for given accession

# Write results to file
with open(out_path, 'w') as file:
    for key, value in length.items():
        if value:
            file.write(f"{key}\t{value}\n")