#----------------------------------------------------------------------------
# File          : check.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 31.1.2023
# Last Updated  : 21.11.2024
# ---------------------------------------------------------------------------


import sys
import os
import json
from theses_checker.document_info_advanced import DocumentInfoAdvanced
from theses_checker.theses_checker import Checker
import argparse

# ---------------------------------------------- MAIN --------------------------------------------------------

parser = argparse.ArgumentParser(description="Makes a new pdf file called '*_annotated.pdf' in the folder, where this program is saved. If no check flag is given, everything will be checked.") # TODO:
parser.add_argument('in_files', nargs='+', help="path to files to be checked; only '*.pdf' are supported")
parser.add_argument('--embedded_PDF', action='store_false', help="if used, embedded PDF files will be treated as part of the PDF; otherwise, they will be considered as images")
parser.add_argument('-o', '--overflow', action='store_true', help="overflow check")
parser.add_argument('-i', '--image_width', action='store_true', help="image width check")
parser.add_argument('-H', '--Hyphen', action='store_true', help="hyphen check")
parser.add_argument('-t', '--TOC', action='store_true', help="table of content section check")
parser.add_argument('-s', '--space_bracket', action='store_true', help="space before left bracket check")
parser.add_argument('-e', '--empty_chapter', action='store_true', help="text between titles check")
parser.add_argument('-b', '--bad_reference', action='store_true', help=" '??' -> bad reference check")
#parser.add_argument('--out_file', default="annotated.pdf", help="name of created annotated file, default name is 'annotated.pdf'; usable with only one IN_FILES otherwise ignored")
args = parser.parse_args(sys.argv[1:])



if(not (args.overflow or args.image_width or args.Hyphen or args.TOC or args.space_bracket or args.empty_chapter or args.bad_reference)):
    args.overflow = True
    args.image_width = True
    args.Hyphen = True
    args.TOC = True
    args.space_bracket = True
    args.empty_chapter = True
    args.bad_reference = True

for file in args.in_files:
    if(not os.path.exists(file)):
        print("File '" + file + "' does not exist.")
        continue
    if(file[-4:] != ".pdf"):
        print("File '" + file + "' is not supported.")
        continue

    checker = Checker(file)

    base = os.path.realpath(file)[:-4]

    annotated_file = base + "_annotated.pdf"
    info_json = base + "_info.json"
    typos_json = base + "_typography.json"

    checker.annotate(annotated_file, args.embedded_PDF, args.overflow, args.Hyphen, args.image_width, args.TOC, args.space_bracket, args.empty_chapter, args.bad_reference)

    doc_info = DocumentInfoAdvanced(checker.chaptersInfo[0], checker.chaptersInfo[1], checker.chaptersInfo[2]).toDict()
    typo_info = checker.typographyMistakes.toDict()

    with open(info_json, "w", encoding="utf-8") as f:
        json.dump(doc_info, f, ensure_ascii=False, indent=2)
    with open(typos_json, "w", encoding="utf-8") as f:
        json.dump(typo_info, f, ensure_ascii=False, indent=2)