const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 5000;

// PostgreSQL configuration
const pool = new Pool({
  user: 'postgres_user',
  host: 'dev-database-2.cmbltiirvdvj.us-west-2.rds.amazonaws.com',
  database: 'postgres',
  password: 'Dev#test#23',
  port: 5432,
});

// Middleware to authenticate users based on user id
app.use(async (req, res, next) => {
  try {
    // Assuming the user id is passed in the headers
    const userId = req.headers['Varad More'];

    // Query the database to check if the user exists
    const userQuery = await pool.query('SELECT * FROM opportunitytable');

    // const userQuery = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

    if (userQuery.rows.length === 0) {
      return res.status(401).json({ error: 'User not found' });
    }

    // Add the user object to the request for later use
    req.user = userQuery.rows[0];
    next();
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Route to get user-specific data from PostgreSQL
app.get('/user-data', async (req, res) => {
  try {
    // Use req.user to get the authenticated user
    const userId = req.user.id;

    // Query data for the authenticated user
    // const dataQuery = await pool.query('SELECT * FROM opportunitytable WHERE opp_isa = $1', [userId]);
    const dataQuery = await pool.query('SELECT * FROM opportunitytable');

    // const dataQuery = await pool.query('SELECT * FROM user_data WHERE user_id = $1', [userId]);

    res.json(dataQuery.rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
