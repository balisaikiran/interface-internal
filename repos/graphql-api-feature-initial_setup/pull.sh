pm2 kill 
sudo git pull
npm run compile
pm2 start ~/test/graphql-api/dist/index.js 
sudo systemctl restart nginx
