import React, { useEffect, useState, useRef } from 'react';
import {
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
} from '@material-ui/core';

export default function RealtimeLog({ log }: any) {
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
    <Paper>
      <Typography variant="h6" gutterBottom>
        실시간 로그
      </Typography>
      <Card variant="outlined">
        <CardContent
          style={{ height: '100px', overflow: 'auto', whiteSpace: 'pre-line' }}
        >
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
