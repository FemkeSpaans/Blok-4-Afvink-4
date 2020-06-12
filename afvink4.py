# Author: Femke Spaans
# Date: 18-05-2020
# Name: Afvink 4
# Version: 1

from Bio import BiopythonWarning
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import re


def input(seq):
    # Altijd weten WAT het is.
    # Als het DNA is, RNA en eiwit geven.
    # Als het een eiwit is, meerst waarschijnlijke gen geven.
    number = check(seq)
    info = ""
    if number == 0:
        type = ("dna", "This is DNA.")
        info = dna(seq)
    elif number == 1:
        type = ("rna", "This is RNA.")
        info = rna(seq)
    elif number == 2:
        type = ("protein", "This is a Protein.")
        info = protein(seq)
    else:
        print("This is not DNA, RNA or a protein")
    return type, info


def check(seq):
    """
    create regex to check whether it is dna, rna or a protein,
    return it to 0 if dna, 1 if rna, 2 for protein and 3 for none
    :param seq: str
    :return 0, 1, 2, 3:
    """
    check_dna = re.search("[^ATGC*$]", seq.upper())
    check_rna = re.search("[^AUGC*$]", seq.upper())
    check_protein = re.search("[^GPAVLIMCFYWHKRQNEDST*$]", seq.upper())
    if check_dna == None:
        print("This is DNA")
        return 0
    elif check_rna == None:
        print("This is RNA")
        return 1
    elif check_protein == None:
        print("This is a protein")
        return 2
    else:
        return 3


def dna(seq):
    """
    turn seq into mrna,
    turn seq into protein
    :param seq:
    :return:
    """
    try:
        coding_dna = Seq(seq, IUPAC.unambiguous_dna)
        rna = coding_dna.transcribe()
        print("The corresponding mRNA to this sequence is:", rna)
        # messenger_rna = Seq(seq, IUPAC.unambiguous_rna)
        # print(messenger_rna, "oke")
        protein = coding_dna.translate()
        print("The corresponding protein to this sequence is:", protein)
        return (rna, protein)
    except BiopythonWarning:
        pass


def rna(seq):
    """prints rna seq

    :param seq:
    """
    print("This is an RNA sequence:", seq)


def protein(seq):
    """blast a seq and put in xml file, 
    open xml file and iterate over it to get gene names
    :param seq:
    :return alignment.hit_def:
    """
    blast = NCBIWWW.qblast('tblastn', 'nr', seq)
    print(blast)
    with open("my_blast.xml", "w") as out_handle:
        out_handle.write(blast.read())
    with open("my_blast.xml", "r") as out_handle:
        blast_records = NCBIXML.parse(out_handle)
        for blast_record in blast_records:
            for alignment in blast_record.alignments:
                print("Gene that this protein most likely related to:"
                        "", alignment.hit_def)
    return alignment.hit_def
