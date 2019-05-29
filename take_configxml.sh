#!/bin/bash
BASEDIR=`dirname $0`
MYDIR=$1
INFILE=""
DATESTR=`date +%H:%M:%S`

INFILE=""

function readfiles()
{
#FILES=`find /opt/weblogic/domains/*/config/ -name "config.xml" 2>/dev/null`
#FILES=`locate "config/config.xml"|egrep -iv "samples|config.xml_|config.xml.|templates|WEB-INF"`
FILES=`find /opt/weblogic/domains -name "config.xml"|grep -i "config.xml"|egrep -v "samples|bkp|backup|.*\.[0-9]|.*\_[0-9]|.*\-[0-9]|domain_bak"|egrep "\/opt\/weblogic\/domains(\/[a-zA-Z]*\/config\/config.xml|\/[a-zA-Z]*\/config.xml|\/[a-zA-Z0-9&_\.-]*\/config\/config.xml|\/[a-zA-Z0-9&_\.-]*\/config.xml)"`


#echo "FILES FOUND: " $FILES

for INFILE in $FILES
do
        echo "DOMAIN FILE:"$INFILE
        LOGFILE_NAME="/tmp/"`echo $INFILE|sed 's/\// /g'|awk '{print $4}'`"_dumpxyz"
        DOMAIN=`echo $INFILE|sed 's/\// /g'|awk '{print $4}'`
        if [ -e $INFILE ]
        then
                echo "File is present"
                echo "Taking a Backup of the file"
                cp $INFILE $INFILE"_"$DATESTR
                ls -lrt $INFILE"_"$DATESTR
        else
                echo "File is not present"
                exit
        fi

        echo "Setting Domain Environment"
        tmp1=`dirname $INFILE`
        DOMAIN_DIR=`dirname $tmp1`

        . $DOMAIN_DIR/bin/setDomainEnv.sh
        echo "SHIFTING TO OLD DIRECTORY $MYDIR"
        cd $MYDIR
        hostout=`uname -n`.host
        uname -a|awk '{print "Machine Kernal Name:",$1,"\nHost Name:",$2 "\nKernal Version:",$3}' > $hostout 2>&1
        cpu=`cat /proc/cpuinfo|grep -i processor|tail -1|cut -d':' -f2|tr -d '[:space:]'`
        echo "cpu count: $cpu" >> $hostout 2>&1
        javaversion=`$JAVA_HOME/bin/java -version > /tmp/javaversion 2>&1 && sed -n '3p' /tmp/javaversion|tr -d '[:space:]'`
        $BASEDIR/consoleupdate.py $INFILE `hostname` $javaversion > $LOGFILE_NAME
done

#remove the files
echo " Removing /tmp/javaversion" `rm -rf /tmp/javaversion`
}

function configure()
{
BASEDIR=`dirname $0`

PID_LIST=`ps -feww|grep -i weblogic.Server|grep -v grep|awk '{ print $2}'`

echo "PID SERVERNAME HOSTNAME"|awk '{printf "%-20s%-30s%s\n",$1 , $2, $3}'
echo "----------------------------------------------------------------------------"
for PID in $PID_LIST
do
        SERVER=`ps -feww|grep -i $PID|grep -v grep|awk 'BEGIN {FS="-Dweblogic.Name"}; { print $2}'|awk '{print $1}'|cut -d= -f2`
        echo "$PID $SERVER `hostname`"|awk '{printf "%-20s%-30s%s\n",$1 , $2, $3}'
        JAVA_PATH=`ps -feww|grep -i weblogic.SErver|awk '{print $8}'|grep -v grep|uniq|head -1`
        #export JAVA_PATH


done
}

configure > /tmp/status_app.txt
readfiles
