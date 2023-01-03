#!/bin/sh

LEN=4
RUNNING=true

if [ $# -lt 2 ]
    then
    echo "Usage ${0} <CHARS> <KEY> [STARTLENGTH]"
    exit 1
fi

if [ $# -gt 2 ]
    then
        LEN=${3}
fi

TEMPFILE=$(mktemp)

echo "Writing into file: ${TEMPFILE}"

while ${RUNNING}
do
    echo "Trying words with length ${LEN}, press enter to continue, enter STOP to stop."
    read CONT
    if [ "${CONT}" = "STOP" ]
        then
            break
    fi

    ./word_permutations.py ${1} ${LEN} | hunspell -d de_DE -G | sort -h | uniq | grep -i ${2} > ${TEMPFILE}
    echo "$(cat ${TEMPFILE} | wc -l) words found, press enter to send them."
    read _
    sleep 2
    while read WORD
    do 
        ./kbd.py ${WORD}
    done < ${TEMPFILE}
    LEN=$((LEN+1))
done

rm ${TEMPFILE}
