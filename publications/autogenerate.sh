#/bin/bash

bibtex2html -nobiblinks -r -d -charset Verdana  --nodoc --no-header -no-footer maePubs.bib

round=1
for lineNo in `grep  -n SCRIPTAUTODETECT ../professional_publications.html |cut -d":" -f1`
do
   if [ $round -eq 1 ];then
     head -n$lineNo ../professional_publications.html >tmp.html
     round=2
   else
     totalLines=`wc -l ../professional_publications.html |cut -d" " -f1`     
     last=`expr $totalLines - $lineNo`
     last=`expr $last + 2`
     cat maePubs.html >>tmp.html
     echo "">>tmp.html
     tail -n$last ../professional_publications.html >>tmp.html
   fi
done

cp -f maePubs_bib.html ..
mv tmp.html ../professional_publications.html
