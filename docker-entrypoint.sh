#!/bin/sh

set -e
LOCUST_MODE=${LOCUST_MODE:-standalone}
LOCUST_MASTER_BIND_PORT=${LOCUST_MASTER_BIND_PORT:-5557}
LOCUST_FILE=${LOCUST_FILE:-locustfile.py}

if [ -z ${ATTACKED_HOST+x} ] ; then
    echo "You need to set the URL of the host to be tested (ATTACKED_HOST)."
    exit 1
fi

LOCUST_OPTS="-f ${LOCUST_FILE} --host=${ATTACKED_HOST} $LOCUST_OPTS"

cd /

case `echo ${LOCUST_MODE} | tr 'a-z' 'A-Z'` in
"MASTER")
    LOCUST_OPTS="--master --master-bind-port=${LOCUST_MASTER_BIND_PORT} $LOCUST_OPTS"
    ;;

"WORKER")
    locustMasterIP=$(python3 /test/findLocustMaster.py)
    echo "locust master ip received: "$locustMasterIP
    if [ -z ${locustMasterIP+x} ]; then
        echo "In the given namespace, no master pods are in running state.. exiting.."
        exit 1
    fi

    LOCUST_OPTS="--worker --master-host=$locustMasterIP --master-port=${LOCUST_MASTER_BIND_PORT} $LOCUST_OPTS"
    ;;
esac

cd /test
echo "starting locust"
echo $LOCUST_OPTS
locust ${LOCUST_OPTS}
