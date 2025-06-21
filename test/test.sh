#!/bin/bash

set -e

FILE_SIZE=1048576  # 1MB
ORIGINAL_FILE="original.dat"
RECEIVED_FILE="received.dat"
HOST="127.0.0.1"
PORT=8080

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

test_tcp() {
  echo "Running TCP test..."

  SERVER_SCRIPT="src/tcp_server.py"
  CLIENT_SCRIPT="src/tcp_client.py"

  CHARS='A-Za-z0-9!"#$&''()*+,-./:;<=>?@[]^_`{|}~'
  head /dev/urandom | tr -dc "$CHARS" | head -c ${FILE_SIZE} > ${ORIGINAL_FILE}

  python src/tcp_server.py ${ORIGINAL_FILE} --host ${HOST} --port ${PORT} > server_tcp.log 2>&1 &
  SERVER_PID=$!
  sleep 1

  python src/tcp_client.py ${RECEIVED_FILE} --host ${HOST} --port ${PORT} > client_tcp.log 2>&1

  wait ${SERVER_PID}

  diff ${ORIGINAL_FILE} ${RECEIVED_FILE}
  DIFF_EXIT_CODE=$?

  if [ ${DIFF_EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}TCP тест пройден: файлы совпадают.${NC}"
    echo -e "${GREEN}SUCCESS${NC}"
    RESULT_STATUS="${GREEN}SUCCESS${NC}"
    RESULT_COLOR="${GREEN}"
    EXIT_CODE=0
  else
    echo -e "${RED}TCP тест не пройден: файлы отличаются.${NC}"
    echo -e "${RED}FILE${NC}"
    RESULT_STATUS="${RED}FAIL${NC}"
    RESULT_COLOR="${RED}"
    EXIT_CODE=1
  fi

  rm -f ${ORIGINAL_FILE} ${RECEIVED_FILE} server_tcp.log client_tcp.log

  return ${EXIT_CODE}
}


test_tcp
TCP_EXIT_CODE=$?

if [[ $TCP_EXIT_CODE -eq 0]]; then
    exit 0
else
    exit 1
fi
