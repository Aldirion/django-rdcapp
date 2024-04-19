#!/bin/bash

pg_restore -j $(nproc) \
  -d $POSTGRES_DB \
  -U $POSTGRES_USER \
  "/dumps/$1"
