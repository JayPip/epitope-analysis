import json
import csv
import numpy
import Bio
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_sequences(data):
    sequences = []
    for item in data["Data"]:
        sequence = item.get("Epitope - Name", "")
        organism = item.get("Epitope - Source Organism", "")
        sequences.append((organism, sequence))
    return sequences

def compare_sequences(sequences_human, sequences_mouse):
    comparisons = []
    for seq1 in sequences_human:
        for seq2 in sequences_mouse:
            alignments = pairwise2.align.globalxx(seq1[1], seq2[1])
            #normalize data
            comparisons.append({(alignments[0].score / min(len(seq1[1]), len(seq2[1]))), seq1[1], seq2[1]})
    return comparisons

def perform_permutation(sequences_human, sequences_mouse, num_permutations=50):
    scores = []
    for seq1 in sequences_human:
        for seq2 in sequences_mouse:
            scores_list = []
            for _ in range(num_permutations):
                permuted_seq1 = permute_sequence(seq1[1])
                permuted_seq2 = permute_sequence(seq2[1])
                permuted_scores = pairwise2.align.globalxx(permuted_seq1, permuted_seq2)
                scores_list.append((permuted_scores[0].score/ min(len(seq1[1]), len(seq2[1]))))
            scores.append(scores_list)

    return scores

def print_comparisons(comparisons,x):
    f = open("output/" + x + "out.txt", "w")
    for comp in comparisons:
        seq1, seq2, alignement = comp
        f.write(f"Sequence 1: {seq1}\n")
        f.write(f"Sequence 2: {seq2}\n")
        f.write(f"Alignement:\n")
        f.write(f"{alignement}\n")
    f.close()

def createCsvFile(x, comparisons):
    with open("output/" + x + "out.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['scores'])
        writer.writerows(comparisons)

def permute_sequence(seq):
    return ''.join(numpy.random.permutation(list(seq)))

def main():
    print('Enter protein name:')
    x = input()
    human_file_path = "human/" + x + ".json"  # Update this path
    mouse_file_path = "mouse/" + x + ".json"
    data_human = load_json(human_file_path)
    data_mouse = load_json(mouse_file_path)
    sequences_human = extract_sequences(data_human)
    sequences_mouse = extract_sequences(data_mouse)

    comparisons_orignal = compare_sequences(sequences_human, sequences_mouse)
    # createCsvFile(x, comparisons_orignal)

    max_alignment = {}
    maxFloat = 0;
    for item in comparisons_orignal:
        for s in item:
            if isinstance(s, float):
                if s > maxFloat:
                    max_alignment = item
                    maxFloat = s


    print(max_alignment)

if __name__ == "__main__":
    main()