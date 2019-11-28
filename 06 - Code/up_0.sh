# DBContainerName="my-postgres"
# DBPassword="y0uguysr0ck"
# DBUser="odin"
pypyContainterName="uniweb"
pypyImageName="medtech/uniweb" 

# docker run --name $DBContainerName -p 5432:5432 -e POSTGRES_PASSWORD=$DBPassword -e POSTGRES_USER=$DBUser -d postgres
# docker run --name uniweb-postgres -p 5432:5432 -e POSTGRES_PASSWORD=y0uguysr0ck -e POSTGRES_USER=uniwebv -d postgres
# docker run --name my-etcd -d -p 4001:4001 -p 7001:7001 -p 2379:2379 -p 2380:2380  -v /var/etcd/:/data elcolio/etcd:latest -name my-etcd
# docker run --name redis-cache  --restart=always -p 6379:6379 -d redis
docker build -t $pypyImageName .
docker run -it --name $pypyContainterName -p 4005:8080 -v "$PWD/Application":/usr/src/myapp -w /usr/src/myapp $pypyImageName
# -e 'ETCD_ENV={"host": "10.0.2.15","port": 4001}' \
# -e "UNIWEB_ENV=uniweb-local" \
# -v "$PWD/Application":/usr/src/myapp \
# -w /usr/src/myapp $pypyImageName