const mysql = require("mysql2/promise");

const config = {
  host: process.env.DB_HOST || "mysql",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "Mysql12!",
  database: process.env.DB_NAME || "doctobobo",
  port: process.env.DB_PORT || 3306,
};

const connectToDB = async () => {
  try {
    const db = await mysql.createConnection(config);
    console.log("Connected to MySQL database successfully!");
    return db;
  } catch (error) {
    console.error("Error connecting to MySQL database:", error);
    throw error;
  }
};

module.exports = connectToDB;
