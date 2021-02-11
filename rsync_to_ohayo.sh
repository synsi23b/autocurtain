#!/bin/bash
echo "Rsyncing workspace to remote device..."
echo ""
echo ""
echo ""
rsync -avh --delete --exclude devel --exclude build --exclude .git --exclude __pychache__ ./ ohayo:~/curtain/
echo ""
echo ""
echo ""