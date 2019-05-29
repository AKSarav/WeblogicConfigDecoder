#!/bin/bash
set -x
BASEDIR=`dirname $0`
INFILE=""
DATESTR=`date +%H_%M_%S`
if [ $# -le 0 ]
then
        echo "Need some argument"
        exit
fi

INFILE=$1


#if [ -e $INFILE ]
#then
#       echo "File is present"
#       echo "Taking a Backup of the file"
#       cp $INFILE $INFILE"_"$DATESTR
#else
#       echo "File is not present"
#fi


for LINE in `cat $INFILE`
do
         echo "Processing Line $LINE"
        #sshpass -p.passwd ssh $LINE "uname -n"
        ssh-keygen -R $LINE
        DIRNAME="/var/tmp/inventory_data_"$DATESTR"/"
        sshpass -f.passwd ssh   -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no sthangar@$LINE "mkdir $DIRNAME && chmod -R 777 $DIRNAME & cd $DIRNAME"
        sshpass -f.passwd scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no proj.tar sthangar@$LINE:$DIRNAME.
        sshpass -f.passwd ssh   -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no sthangar@$LINE "cd $DIRNAME && tar -xvf proj.tar && sudo -u weblogic ./take_configxml.sh $DIRNAME"
        if [ ! -e inventory/$LINE ]
        then
                mkdir inventory/$LINE
        fi
        sshpass -f.passwd scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r sthangar@$LINE:$DIRNAME/*domain_dumps*  inventory/$LINE/
        sshpass -f.passwd scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r sthangar@$LINE:$DIRNAME/*.host inventory/$LINE/
        echo "REMOVING THE /var/tmp/inventory_data_* DIRECTORIES"
        sshpass -f.passwd ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no sthangar@$LINE "rm -rf /var/tmp/inventory_data_*"
        ## Python Script to take care of these files
        echo "Press enter to Proceed to next instance"
        read tmp
done

