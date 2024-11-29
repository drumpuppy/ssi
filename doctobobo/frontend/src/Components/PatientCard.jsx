import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Card, CardContent, Button, Typography, Grid } from '@mui/material';

const styles = {
  typo: {
    fontFamily: "'Poppins'",
    fontSize: "20px",
    color: "white",
  },
  fileUploadBtn: {
    background: "#fff",
    color: "#0573E3",
    '&:hover': {
      background: "#ccc",
    }
  },
  fileDeleteBtn: {
    background: "red",
    color: "#fff",
    '&:hover': {
      background: "darkred",
    }
  },
  absoluteBox: {
    background: "#02298A",
    width: "200px",
    height: "200px",
    borderRadius: "100%",
    position: "absolute",
    bottom: -40,
    right: -40,
    opacity: 0.5,
  },
};

export default function PatientCard({
  id,
  slot,
  question,
  answer,
  date,
  patientName,
  doctorName
}) {
  

  if (slot && slot.startTime && slot.endTime) {

    return (
      <Card sx={{ position: "relative", borderRadius: "20px", boxShadow: 3, background: "#0573E3" }}>
        <Box sx={styles.absoluteBox}></Box>
        <CardContent>
          <Typography sx={[styles.typo, { fontWeight: 600 }]} gutterBottom>Date: {date}</Typography>
          <Typography sx={[styles.typo, { fontWeight: 600 }]} gutterBottom>Créneau: {slot && slot.startTime && slot.endTime ? `${slot.startTime} to ${slot.endTime}` : 'Time not available'}</Typography>
          <Typography sx={styles.typo} gutterBottom>Nom du patient: {patientName}</Typography>
          <Typography sx={styles.typo} gutterBottom>Nom du médecin: {doctorName}</Typography>
          <Typography sx={[styles.typo, { minHeight: "100px" }]} gutterBottom> Votre bobo : {question}</Typography>
          {answer === null ? (
            <Typography sx={[styles.typo, { color: "red" }]}>No response yet</Typography>
          ) : (
            <Typography sx={styles.typo}>{answer}</Typography>
          )}
        </CardContent>
      </Card>
    );
  }
}