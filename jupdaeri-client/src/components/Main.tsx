import React, { useEffect, useState } from 'react';
import { Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import RealtimeLog from './main/RealtimeLog';
import TodayNote from './main/TodayNote';
import Balance from './main/Balance';

const useStyles = makeStyles({
  table: {
    minWidth: 300,
  },
});

function createData(
  name: string,
  calories: number,
  fat: number,
  carbs: number,
  protein: number,
) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('카카오', 159, 6.0, 24, 4.0),
  createData('sk', 237, 9.0, 37, 4.3),
  createData('삼성전자', 262, 16.0, 24, 6.0),
  createData('SK하이닉스', 305, 3.7, 67, 4.3),
  createData('LG생활건강', 356, 16.0, 49, 3.9),
];

export default function Main() {
  const classes = useStyles();
  const [webSocket, setWebSocket] = useState();
  const [realtimelog, setRealtimelog] = useState();

  useEffect(() => {
    const webSocket = new WebSocket('ws://localhost:9998');
    webSocket.onopen = () => {
      webSocket.send('javascript send to data here~');
    };
    webSocket.onmessage = (message: any) => {
      setRealtimelog(message.data);
    };
    webSocket.onmessage = (message: any) => {
        setRealtimelog(message.data);
      };
    setWebSocket(webSocket);
  }, []);

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} md={6}>
        <TodayNote />
      </Grid>
      <Grid item xs={12} md={6}>
        <RealtimeLog log={realtimelog} />
      </Grid>
      <Grid item xs={12} md={6}>
        <Balance />
      </Grid>
    </Grid>
  );
}
