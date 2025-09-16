npm run build
ssh root@47.93.45.6 "rm -rf /server/mindnotes_stats/*"
scp -r backend root@47.93.45.6:/server/mindnotes_stats/
scp -r dist root@47.93.45.6:/server/mindnotes_stats/
scp start_server.py root@47.93.45.6:/server/mindnotes_stats/
scp Dockerfile root@47.93.45.6:/server/mindnotes_stats/

ssh root@47.93.45.6 "docker stop mindnotes_stats && docker rm mindnotes_stats"
ssh root@47.93.45.6 "cd /server/mindnotes_stats && docker build -t mindnotes_stats_app . && docker run -it -d --name mindnotes_stats -v /server/mindnotes_stats:/app --network=host mindnotes_stats_app"

