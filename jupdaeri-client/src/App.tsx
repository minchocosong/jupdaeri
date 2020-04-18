import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import { Grid, Paper } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Menu from './components/Menu';

const useStyles = makeStyles({
  header: {
    height: '20vh',
    position: 'relative',
  },
  headerText:{
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
  }
});
export default function App() {
  const classes = useStyles();

  return (
    <Container maxWidth="lg">
      <div className={classes.header} >
        <Typography variant="h3" component="h3" align="center" className={classes.headerText}>
          줍대리
        </Typography>
      </div>
      <Menu />
    </Container>
  );
}