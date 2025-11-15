import pkg from 'pg';
const { Pool } = pkg;

const PG_USER = process.env.PG_USER
const PG_HOST = process.env.PG_HOST
const PG_DATABASE = process.env.PG_DATABASE
const PG_PASSWORD = process.env.PG_PASSWORD
const PG_PORT = process.env.PG_PORT

// const PG_USER = 'postgres_user'
// const PG_HOST = 'dev-database-2.cmbltiirvdvj.us-west-2.rds.amazonaws.com'
// const PG_DATABASE = 'postgres'
// const PG_PASSWORD = 'Dev#test#23'
// const PG_PORT = 5432

export const pool = new Pool({
  user: PG_USER,
  host: PG_HOST,
  database: PG_DATABASE,
  password: PG_PASSWORD,
  port: PG_PORT,
  max: 80,
  // idleTimeoutMillis: 30000,
})
