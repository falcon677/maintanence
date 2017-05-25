#!/usr/bin/env bash
# email: leidong@kingsoft.com

source ./backuprc

dbname=${dbname:='nova'}
dbuser=${dbuser:='root'}
dbpass=${dbpass:='openstack'}
dbhost=${dbhost:='localhost'}


function conn_db_test {
    # test conn to targget mysql server
    mysql -h$dbhost -u$dbuser -p$dbpass -e "use $dbname;" &>/dev/null
    if [[ $? -ne 0 ]] ; then
        echo "Fail to conn mysql"
        return 1
    else
        return 0
    fi
}

# exec to mysql
function exec_sql_cmd {
    sql=$@
    mysql -h$dbhost -u$dbuser -p$dbpass -N -e "use $dbname; $sql;"
    return $?
}


# select  storage type 
function  select_backup_storage_type {
    uuid=$1
    sql_cmd="select storage_type from ephemeral_backup where backup_uuid = '$uuid' and deleted = 0"
    printf "$sql_cmd"
}

# set sql cmd
function alter_backup_storage_type {
    uuid=$1
    sql_cmd="update ephemeral_backup set  storage_type = 1, updated_at = now()  where backup_uuid = '$uuid' and deleted = 0"
    echo "$sql_cmd"
}


# alter  sql cmd
function alter_db {
    backuplistfile=$1
    conn_db_test

    [[ $? -eq 1 ]] && return 1

    if [[ -f $backuplistfile ]]; then
        uuids=`cat $backuplistfile`
    else
        uuids=$backuplistfile
    fi

    for uuid in `echo $uuids`
    do
        select_sql_cmd=`select_backup_storage_type $uuid`
        select_result=`exec_sql_cmd  $select_sql_cmd`
        if [[ $? -eq 0 ]]; then
            printf "Begin\tbackup: $uuid\tstorage_type: $select_result\n"
        else
            echo "Fail exec sql $sql_cmd"
            return 1
        fi

        sql_cmd=`alter_backup_storage_type $uuid`
        exec_sql_cmd  $sql_cmd
        if [[ $? -eq 0 ]]; then
            echo "succeed to change backup uuid $uuid storage type to ks3"
            select_result=`exec_sql_cmd  $select_sql_cmd`
            if [[ $? -eq 0 ]]; then
                printf "End\tbackup: $uuid\tstorage_type: $select_result\n"
            else
                echo "Fail exec sql $select_sql_cmd"
                return 1
            fi
        else
            echo "Failure to change backup uuid $uuid storage type to ks3"
        fi
    done

}

# help info
function usage {
    printf "Usage:\n %s  <options>
    \t-F backup uuid list file             eg: -F <backup.list>
    \t-u backup uuid                       eg: -u <backup_uuid>
    \t-H or -h or -? Output hellp info \n" $(basename $0 | cut -d'.' -f1) >&2
    exit 1
}


Fflag=0
fflag=0
iflag=0
aflag=0
uflag=0
vflag=0

## get commond args
while getopts 'F:u:hH' OPTION
do
    case $OPTION in
        F)  Fflag=1
            backuplistfile="$OPTARG"
            ;;

        u)  uflag=1
            backupuuid="$OPTARG"
            ;;

        h)  usage
            ;;

        H)  usage
            ;;

        ?)  usage
            ;;

    esac
done

[[ $Fflag -eq 0 && $uflag -eq 0 ]] && usage 

if [[ $Fflag -eq 1 ]]; then
    alter_db $backuplistfile
fi

if [[ $uflag -eq 1 ]]; then
    alter_db $backupuuid
fi
