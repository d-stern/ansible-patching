#!/bin/bash

NAME="do_stuff"


usage() {
  echo "Usage:"
  echo "$NAME (-r role)"
  echo ""
  echo "Options: "
  echo " -r --role=<role> role to search through chef to apply runbook to"
  exit 1
}



[[ -d .git ]] || { 
  echo "Unable to locate .git folder. Please invoke from the base checkout directory"
  usage
}



#need to caclue
