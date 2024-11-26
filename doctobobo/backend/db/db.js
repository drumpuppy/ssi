const { Pool } = require("pg");

const config = {
  host: process.env.DB_HOST || "mysql",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "Mysql12!",
  database: process.env.DB_NAME || "doctobobo",
  port: process.env.DB_PORT || 3306,
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
