import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Card, CardContent, Button, Typography, TextField, Grid } from '@mui/material';

const styles = {
  typo: {
    fontFamily: "'Poppins'",
    fontSize: "20px",
    color: "white",
  },
  appointBtn: {
    marginTop: "10px",
    width: "100%",
    fontFamily: "'Poppins'",
    background: "linear-gradient(90deg, rgba(5,117,230,1) 0%, rgba(2,41,138,1) 82%)",
    color: "white",
    fontSize: "15px",
  },
  absoluteBox: {
    background: "#02298A",
    width: "200px",
    height: "200px",
    borderRadius: "100%",
    position: "absolute",
    top: -50,
    right: -50,
    opacity: 0.5,
  },
};

export default function AppointmentCard({
  id,
  slot,
  question,
  answer,
  onUpdate,
  date,
  patientName,
  doctorName,
}) {
  const [prescription, setPrescription] = useState(answer);
  const [files, setFiles] = useState([]);


  return (
    <Card sx={{ borderRadius: "20px", boxShadow: 3, background: "#0572E2", position: "relative" }}>
      <Box sx={styles.absoluteBox}></Box>
      <CardContent>
        <Typography sx={[styles.typo, { fontWeight: 600 }]} gutterBottom>Date: {date}</Typography>
        <Typography sx={[styles.typo, { fontWeight: 600 }]} gutterBottom>Créneau: {`de ${slot.startTime} à ${slot.endTime}`}</Typography>
        <Typography sx={styles.typo} gutterBottom>Nom du patient: {patientName}</Typography>
        <Typography sx={styles.typo} gutterBottom>Nom du docteur: {doctorName}</Typography>
        <Typography sx={[styles.typo, { minHeight: "100px" }]} gutterBottom>Demande: {question}</Typography>
        <TextField
          fullWidth
          multiline
          rows={4}
          value={prescription}
          onChange={(e) => setPrescription(e.target.value)}
          variant="outlined"
          sx={{ background: "white", borderRadius: "20px" }}
        />
        <Button sx={styles.appointBtn} size="large" onClick={() => onUpdate(id, prescription)}>Envoyer la réponse</Button>
      </CardContent>
    </Card>
  );
}

