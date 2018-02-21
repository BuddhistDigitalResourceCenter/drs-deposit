#!/bin/bash
ME=$(basename $0)

usage() {
	cat << USAGE

	Usage: splitWorks.sh [OPTIONS] worksList 
	OPTIONS:
		-l (length)	split the source into files of 'n' length. (default)
		-w (width)  split the source into 'n' files, of as close to equal length as possible
		-n 				number of files/lines (default is 4)
		-p (prefix)		Prefix of output file names (default worksList)
		worksList		is a file containing lines of text which get put into output files

	splitWorks.sh splits worksList into files. If 


USAGE
exit 1;
}

declare -i worksPerRun
unitsPerList=3 

declare HFLAG="h"
declare VFLAG="v"
declare direction=$HFLAG
direction=
# do we have what we need?

while getopts n:hvp: opt ; do
	case $opt in
		h)
echo "H";
			direction=$HFLAG;
			;;
		v)
echo "V";
			direction=$VFLAG;
			;;
		n)
			unitsPerList=$OPTARG ;
echo "units per ${unitsPerList}";
			;;
		p)
			worksFn=$OPTARG ;
echo "worksFn ${worksFn}";
			;;

	esac
done

shift $((OPTIND-1))
echo "whats left :${@}:"
[ "x$1" == "x" ]  && usage

sourceFile=$1

[ -f $sourceFile ] || { echo "${ME}: source file \"$sourceFile\" does not exist or is not a file." ; exit 2 ; }


#
declare -i fileCount
fileCount=0

declare -i fileIndex
fileIndex=0

read -p "$(printf "direction=%s unitsPerList=%s file=%s" $direction $unitsPerList  $worksList )"
while IFS=',' read -ra  workLine ; do
	# This allows csv files to have their lines copied.
	# Could have just copied the raw line....
	# doublequoted "${x[*]}" shows IFS separated list of array elements
	IFS=',' # while's IFS setting is ex scope

	if [ $direction == $HFLAG ]  ; then 
		echo "${workLine[*]}"  >> ${worksFn}${fileCount}.txt
		[ $fileIndex  == 0 ]  && echo "Creating file ${fileCount}"	
	else	
		echo "${workLine[*]}"  >> ${worksFn}${fileIndex}.txt
		[ $fileIndex  == 0 ]  && echo "Wrapping back to file ${fileIndex}"		
	fi

	((fileIndex++))
	[ $fileIndex  == ${unitsPerList} ]  && ((fileCount++))
	[ $fileIndex  == ${unitsPerList} ]  && fileIndex=0

done < $sourceFile
