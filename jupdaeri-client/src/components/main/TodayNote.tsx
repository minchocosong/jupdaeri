import React, { useEffect, useState } from 'react';
import {
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

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

export default function TodayNote() {
  const classes = useStyles();

  return (
    <Paper>
      <Typography variant="h6" gutterBottom>
        매매일지
      </Typography>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center">종목</TableCell>
              <TableCell align="right">매매구분</TableCell>
              <TableCell align="right">수량</TableCell>
              <TableCell align="right">미체결수량</TableCell>
              <TableCell align="right">체결수량</TableCell>
              <TableCell align="right">주문단가</TableCell>
              <TableCell align="right">체결단가</TableCell>
              <TableCell align="right">주문번호</TableCell>
              <TableCell align="right">주문시각</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map(row => (
              <TableRow key={row.name}>
                <TableCell component="th">{row.name}</TableCell>
                <TableCell align="right">{row.calories}</TableCell>
                <TableCell align="right">{row.fat}</TableCell>
                <TableCell align="right">{row.protein}</TableCell>
                <TableCell align="right">{row.calories}</TableCell>
                <TableCell align="right">{row.fat}</TableCell>
                <TableCell align="right">{row.protein}</TableCell>
                <TableCell align="right">{row.calories}</TableCell>
                <TableCell align="right">{row.fat}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
