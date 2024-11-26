const express = require("express");
const router = express.Router();
const { db } = global;

router.get("/", async (req, res) => {
  try {
    const query = `SELECT * FROM Medecin`;
    const [medecins] = await db.query(query);
    console.log(`Fetched ${medecins.length} Medecin records`);
    res.status(200).json(medecins);
  } catch (error) {
    console.error("Error fetching Medecin records:", error);
    res.status(500).json({ message: "Internal server error" });
  }
});


module.exports = router;
