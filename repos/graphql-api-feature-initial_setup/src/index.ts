import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import express from 'express';
import http from 'http';
import pkg from 'body-parser';
const { json } = pkg;
import cors from 'cors';
import { typeDefs } from './schema.js';
import { makeExecutableSchema } from '@graphql-tools/schema'
import {keys} from './modules/secrets.js';
import DataLoader from "dataloader";
import {getdynamodbloaders} from "./modules/database/dynamodb.js"
import {resolvers} from "./resolvers.js"
import cookieParser from 'cookie-parser';
import fetch from "node-fetch";
// const django_url = process.env.DJANGO_SERVER_URL;
// const react_url = process.env.REACT_SERVER_URL;
// console.log("Django url", django_url)
// console.log("React url", react_url)
// const resolvers = [
//   {
//   GraphQLJSON: GraphQLJSON,
//   Query: {
//   },
// }];

const schema = makeExecutableSchema({ typeDefs, resolvers })

const app = express();
app.use(cookieParser());

const httpServer = http.createServer(app);

interface MyContext {
  keys?: DataLoader<unknown, String, unknown>;
  dynamodbdatabaseloaders?: DataLoader<unknown, String, unknown>;
}

const server = new ApolloServer<MyContext>({
  schema,
  plugins: [ApolloServerPluginDrainHttpServer({ httpServer })],
});


await server.start();


app.use(
  '/graphql',
  // https://app.datalabz.re
  cors<cors.CorsRequest>({ origin: ['http://localhost:3000'], credentials: true, allowedHeaders: ['Content-Type', 'Authorization']}),
  // cors<cors.CorsRequest>(),  
  json(),
  expressMiddleware(server, {
    context: async ({ req, res }) => {
      
      let team_id;
      if (req.headers.authorization_token == '72c0231a-d275-4524-9700-3ae89eda9ae4') {
        team_id = req.headers.team_id;
      }
      else if (req.cookies){
        console.log(req.cookies.sessionid)
        console.log(req.cookies.csrftoken)
        console.log("Making request to website")
        // https://datalabz.re/user/get_user/
        // make request to locahost:8000/users/get_user with csrftoken and sessionid
        await fetch('http://localhost:8000/user/get_user/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': req.cookies.csrftoken,
            'Cookie': 'sessionid=' + req.cookies.sessionid + '; csrftoken=' + req.cookies.csrftoken
          },
        })
          .then(res => {console.log(res);  return res.json()})
          .then(json => {
            console.log("Response from website")
            console.log(json)
            team_id = (json as any).team_id;
          })
          .catch(err => console.log(err));
        console.log("Finished making request to website")
      }
      else{
        team_id = "DataHelp"
      }
      console.log("team_id", team_id)
      // console.log("------------------")
      const dynamodbdatabaseloaders = getdynamodbloaders();
      // const token = req.headers.authorization || '';
      // const user = await keysloader.load("DataHelp");
      return { "keys": keys, "dynamodbdatabaseloaders": dynamodbdatabaseloaders, "team_id": team_id };
    }
  }),


);


await new Promise<void>((resolve) => httpServer.listen({ port: 4000 }, resolve));
console.log(process.env);
console.log(`🚀 Server ready at http://localhost:4000/graphql`);
// keysloader.load("DataHelp");
// keysloader.load("DataHelp");