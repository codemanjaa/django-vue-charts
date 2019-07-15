#!/usr/bin/env bash

pg_dumpall -h jdfbots-db -c -U jdfuser > /backups/dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql
