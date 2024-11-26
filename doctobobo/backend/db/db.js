const { Pool } = require("pg");

const config = {
  user: process.env.DB_USER || "your_db_user",
  host: process.env.DB_HOST || "localhost",
  database: process.env.DB_NAME || "doctobobo",
  password: process.env.DB_PASSWORD || "your_db_password",
  port: process.env.DB_PORT || 5432,
  idleTimeoutMillis: 30000, // Close idle connections after 30 seconds
  connectionTimeoutMillis: 60000 // Timeout for connecting to the database
};

const pool = new Pool(config);

const connectToDB = async () => {
  try {
    const client = await pool.connect();
    console.log("Connected to PostgreSQL database successfully!");
    // You can run queries here if needed
    return client; // Return the connected client
  } catch (error) {
    console.error("Error: Connection to PostgreSQL database failed!", error);
    throw error;
  }
};

module.exports = connectToDB;
