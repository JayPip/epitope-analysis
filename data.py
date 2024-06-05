import json
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

def compare_sequences(sequences1, sequences2):
    comparisons = []
    for seq1 in sequences1:
        for seq2 in sequences2:
            alignments = pairwise2.align.globalxx(seq1[1], seq2[1])
            comparisons.append((seq1, seq2, format_alignment(*alignments[0])))
    return comparisons

def print_comparisons(comparisons,x):
    f = open("output/" + x + "out.txt", "w")
    for comp in comparisons:
        seq1, seq2, alignement = comp
        f.write(f"Sequence 1: {seq1}\n")
        f.write(f"Sequence 2: {seq2}\n")
        f.write(f"Alignement:\n")
        f.write(f"{alignement}\n")
    f.close()

def main():
    print('Enter protein name:')
    x = input()
    human_file_path = "human/" + x + ".json"  # Update this path
    mouse_file_path = "mouse/" + x + ".json"
    data_human = load_json(human_file_path)
    data_mouse = load_json(mouse_file_path)
    sequences_human = extract_sequences(data_human)
    sequences_mouse = extract_sequences(data_mouse)
    comparisons = compare_sequences(sequences_human, sequences_mouse)
    print_comparisons(comparisons, x)

if __name__ == "__main__":
    main()