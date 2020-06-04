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
    number = check(seq)
    if number == 0:
        dna(seq)
    elif number == 1:
        rna(seq)
    elif number == 2:
        protein(seq)
    else:
        print("This is not DNA, RNA or a protein")


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
        template_dna = coding_dna.reverse_complement()
        print("The corresponding mRNA to this sequence is:", template_dna)
        # messenger_rna = Seq(seq, IUPAC.unambiguous_rna)
        # print(messenger_rna, "oke")
        protein = coding_dna.translate()
        print("The corresponding protein to this sequence is:", protein)
    except BiopythonWarning:
        pass


def rna(seq):
    """

    :param seq:
    :return:
    """
    print("This is an RNA sequence:", seq)


def protein(seq):
    """

    :param seq:
    :return:
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
