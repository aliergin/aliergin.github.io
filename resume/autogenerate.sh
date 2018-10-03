#!/bin/bash

PSTOIMG=/usr/bin/pstoimg
LATEXTOHTML=/usr/bin/latex2html

# Copy PS Version to OUTPUT

cp src/input.ps out/web_resume_mae.ps


# Generate PNG files from PS

$PSTOIMG  --aaliastext --multipage --density 100 --out  out/web_resume_mae.png src/input.ps
$PSTOIMG  --scale 0.2 --aaliastext --multipage --density 100 --out out/web_resume_mae_thumb.png src/input.ps

echo "<HTML><BODY><A HREF=\"../../personal_resume.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_back.png\"/></A><IMG SRC=\"web_resume_mae1.png\"/><A HREF=\"../out/web_resume_mae2.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_next.png\"/></A></BODY></HTML>" > out/web_resume_mae1.html
echo "<HTML><BODY><A HREF=\"../out/web_resume_mae1.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_back.png\"/></A><IMG SRC=\"web_resume_mae2.png\"/><A HREF=\"../out/web_resume_mae3.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_next.png\"/></A></BODY></HTML>" > out/web_resume_mae2.html
echo "<HTML><BODY><A HREF=\"../out/web_resume_mae2.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_back.png\"/></A><IMG SRC=\"web_resume_mae3.png\"/><A HREF=\"../out/web_resume_mae4.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_next.png\"/></A></BODY></HTML>" > out/web_resume_mae3.html
echo "<HTML><BODY><A HREF=\"../out/web_resume_mae3.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_back.png\"/></A><IMG SRC=\"web_resume_mae4.png\"/><A HREF=\"../../personal_resume.html\"><IMG style=\"border: 0px solid\;\" SRC=\"../../images/TEXT_end.png\"/></A></BODY></HTML>" > out/web_resume_mae4.html


# Generate HTML from LATEX
cat src/input.tex | sed -e s/begin\{CV\}/begin\{itemize\}/ | sed -e s/end\{CV\}/end\{itemize\}/ > src/index.tex
latex2html -t "Mesut Ali Ergin -- Resume" --unsegment --up_title "Back" --up_url "../../../" --info "" --no_navigation --no_math --antialias_text --split 0 --dir out/html src/index.tex
cat out/html/index.html | sed -e s/"H1>"/"H3>"/ | sed -e s/"<TH "/"<TD "/| sed -e s/"TH>"/"TD>"/ | sed -e s/"1#1"/"nd"/ |sed -e s/"2#2"/"rd"/ | sed -e s/"<BODY >"/"<BODY> <A HREF=\"..\/..\/..\/personal_resume.html\"><IMG style=\"border: 0px solid ;\" ALIGN=\"LEFT\" SRC=\"..\/..\/..\/images\/TEXT_back.png\"\/><\/A><BR>"/ > out/html/index2.html
mv out/html/index2.html out/html/index.html
rm -f src/index.tex


# Generate TXT from HTML
cat out/html/index.html | sed -e s/"<IMG .*>"// |sed -e s/"<A HREF.*>"// | sed -e s/"<A NAME.*>"// | sed -e s/"<\/A>"// | sed -e s/"<H3>"// | sed -e s/"<\/H3>"// >out/html/index.tmp.html
html2text -o out/web_resume_mae.txt.tmp -ascii -style pretty out/html/index.tmp.html
cat out/web_resume_mae.txt.tmp | sed -e s/MESUTALIERGIN/"MESUT ALI ERGIN"/  | sed -e s/Publications/Publications/ >out/web_resume_mae.txt
rm -f out/html/index.tmp.html out/web_resume_mae.txt.tmp

# Generate PDF from PS
ps2pdf src/input.ps out/web_resume_mae.pdf
