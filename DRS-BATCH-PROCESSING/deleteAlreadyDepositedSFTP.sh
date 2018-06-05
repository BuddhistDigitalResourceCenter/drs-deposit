#!/bin/bash
#
# Parses the output of 'parseMail.awk' looking for batches which are already deposited.
# See ./parseMail.awk for format

export ME=$(basename $0)
. ~/bin/setupErrorLog.sh

function usage() {
echo << USG
    Usage:  ${ME} errorDataFile buildListFileName
    Where:  errorDataFile is the output of parsemail.awk error data file
    Synposis: extracts the user and the batch directory number from errorDataFile (see parseMail.awk)
USG
}


dlSuffix=".UserBatchDir"
errDat=${1?"${ME}: Requires errorDataFile and buildList file names"}
buildList=${2?"${ME}: Requires buildList file names"}

targetErrRE="Object owner supplied name" #  .* already exists for owner code"
delBatDirSuffix="delSFTPCommands"
batList=".batList"

#
# parse each error line. When
awk -F'|' -v batList=${batList} /"${targetErrRE}"/'{

    u = $3;
    bDir = $4;
    errFile = u batList
    print bDir >> errFile;
}' $errDat

# Now that we have files, per user, of batch directories, build the batch remote commands
for bu in *${batList} ; do
    user=${bu%.*}
    BuildDeepDeleteList.sh -o ${user}DelList -p ddl -s $buildList $bu
done

