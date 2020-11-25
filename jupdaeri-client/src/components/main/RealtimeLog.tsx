import React, { useEffect, useState, useRef } from 'react';
import {
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  paper: {
    height: '100%',
  },
  card: {
    height: '92%',
  },
  cardContent: {
    height: '315px',
    overflow: 'auto',
    whiteSpace: 'pre-line',
  },
});

export default function RealtimeLog({ log }: any) {
  const classes = useStyles();

  const [logs, setLogs] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef!.current!.scrollIntoView(false);
  };

  useEffect(() => {
    if (log) {
      setLogs(`${logs} \n ${log}`);
      scrollToBottom();
    }
  }, [log]);

  return (
    <Paper className={classes.paper}>
      <Typography variant="h6" gutterBottom>
        실시간 로그
      </Typography>
      <Card variant="outlined" className={classes.card}>
        <CardContent className={classes.cardContent}>
          {logs}
          <div ref={messagesEndRef} />
        </CardContent>
        <CardActions>
          <Button size="small">중지</Button>
          <Button size="small">재개</Button>
        </CardActions>
      </Card>
    </Paper>
  );
}
