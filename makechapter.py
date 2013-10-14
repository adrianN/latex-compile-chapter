#!/usr/bin/env python
from argparse import ArgumentParser
import re
import subprocess as sub
from os import remove
from glob import iglob



def parse_runtime_parameters():
	parser = ArgumentParser(description='Chapterwise compilation.')
	parser.add_argument("-f", '--fast', dest='fast', action='store_const', const=True, default=False, help='add draft mode to graphicx, hyperref')
	parser.add_argument("-k", '--keep', dest='keep', action='store_const', const=True, default=False, help='keep intermediate files (aux and stuff like that). Default behaviour is to only keep the pdf')
	parser.add_argument("-o", '--output', dest='out', default="select_chapters", help="name of the pdf that we create. Default select_chapters.pdf")
	parser.add_argument('chapters', nargs='+', help='the chapter(s) you want to compile, either number (i.e. specifying "i" compiles the i\'th included file, starting with 0) or filename.')
	parser.add_argument('file', help='the tex masterfile that makes the whole pdf')
	options = parser.parse_args()
	return options

def all_inputs(masterfile):
	""" find the filenames appearing in \input or \include directives in the masterfile """
	inputs = []

	regexp = re.compile(r'\\include\{(?P<file>[^\}]*)\}')
	with open(masterfile,'r') as f:
		for line in f.readlines():
			for match in regexp.finditer(line):
				if match:
					inputs.append(match.group('file'))

	print "I found the following chapters in the master file:"
	print "\t", "\n\t".join(inputs)
	return inputs

def find_chapters(args):
	""" Change the chapters field in args to contain the filenames of the chapters we want to compile 
		as they appear in the \input (or \include) directives """
	#find the include/input directives in the master file
	inputs = all_inputs(args.file)
	#replace numbers by filenames, check that filenames appear in the masterfile
	for i, chap in enumerate(args.chapters):
		try:
			num = int(chap)
			args.chapters[i] = inputs[num]
		except ValueError:
			#maybe a filename
			if not chap in inputs:
				raise ValueError("I don't think \"" + chap + "\" is a valid chapter")
		except IndexError:
			raise IndexError("There are only "+str(len(inputs))+" inputs, there is no chapter "+chap)

	print "I'll compile the following files:"
	args.chapters = list(set(args.chapters))
	print "\t", "\n\t".join(args.chapters)

def clean_up(args):
	for f in iglob(args.out+'.*'):
		if not (f==args.out+'.pdf' or f==args.out+'.tex'):
			print "removing temporary file", f
			remove(f)


def main():
	args = parse_runtime_parameters()
	find_chapters(args)
	if args.fast:
		tex = r'"\PassOptionsToPackage{draft}{graphicx}\PassOptionsToPackage{draft}{graphicx}'
	else:
		tex = '"'
	tex += r'\includeonly{'+', '.join(args.chapters)+'}\input{'+args.file+'}"'
	sub.call(['pdflatex', "-jobname="+args.out, tex])
	if not args.keep:
		clean_up(args)
	

if __name__=="__main__":
	main()