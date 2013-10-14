latex-compile-chapter
=====================

Compiling large LaTeX documents can take quite some time. Typically they are organized into one `master.tex` file that `\include`s indivdual chapters or sections. Typically one only wants to see changes in the chapter one is currently editing, without having to recompile everything.

Based on [this tex.stackexchange answer](http://tex.stackexchange.com/questions/31334/how-to-create-individual-chapter-pdfs) this Python script provides chapterwise compilation, without having to add metainformation to your TeX files.

It looks at the `master.tex` file to find `\include`d files and extract the filenames. You can either use the file names (without `.tex`) or the number of the chapter to specify which chapters to compile. It provides a `--fast` mode that also adds draftmode to `graphicx` and `hyperref`.

Run it with `-h` to get more usage detailed information.