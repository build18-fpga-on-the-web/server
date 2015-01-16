echo 'foo.sh called with'
for var in "$@"
do
    echo "$var"
done
