import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Legend, Tooltip, ComposedChart, Area, Bar } from 'recharts';

const data = [
    {
      name: 'Page A', uv: 4000, pv: 2400, amt: 2400,
    },
    {
      name: 'Page B', uv: 3000, pv: 1398, amt: 2210,
    },
    {
      name: 'Page C', uv: 2000, pv: 9800, amt: 2290,
    },
    {
      name: 'Page D', uv: 2780, pv: 3908, amt: 2000,
    },
    {
      name: 'Page E', uv: 1890, pv: 4800, amt: 2181,
    },
    {
      name: 'Page F', uv: 2390, pv: 3800, amt: 2500,
    },
    {
      name: 'Page G', uv: 3490, pv: 4300, amt: 2100,
    },
  ];


export default function App() {
  return (
    <Grid container spacing={1}>
        <Grid item xs={12} md={6}>
            <Paper>
                <Typography variant="h6" gutterBottom>
                    수익률
                </Typography>
                <LineChart
                    width={500}
                    height={300}
                    data={data}
                    margin={{
                    top: 5, right: 30, left: 20, bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
                    <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
                </LineChart>
            </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
            <Paper>    
                <Typography variant="h6" gutterBottom>
                    평가손익
                </Typography>
                <ComposedChart
                    width={500}
                    height={400}
                    data={data}
                    margin={{
                    top: 20, right: 20, bottom: 20, left: 20,
                    }}
                >
                    <CartesianGrid stroke="#f5f5f5" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="amt" fill="#8884d8" stroke="#8884d8" />
                    <Bar dataKey="pv" barSize={20} fill="#413ea0" />
                    <Line type="monotone" dataKey="uv" stroke="#ff7300" />
                    {/* <Scatter dataKey="cnt" fill="red" /> */}
                </ComposedChart>
            </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
            <Paper>
                <Typography variant="h6" gutterBottom>
                    알고리즘 평가
                </Typography>
                <LineChart
                    width={500}
                    height={300}
                    data={data}
                    margin={{
                    top: 5, right: 30, left: 20, bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
                    <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
                </LineChart>
            </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
            <Paper>
                <Typography variant="h6" gutterBottom>
                    N평가
                </Typography>
                <ComposedChart
                    width={500}
                    height={400}
                    data={data}
                    margin={{
                    top: 20, right: 20, bottom: 20, left: 20,
                    }}
                >
                    <CartesianGrid stroke="#f5f5f5" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="amt" fill="#8884d8" stroke="#8884d8" />
                    <Bar dataKey="pv" barSize={20} fill="#413ea0" />
                    <Line type="monotone" dataKey="uv" stroke="#ff7300" />
                    {/* <Scatter dataKey="cnt" fill="red" /> */}
                </ComposedChart>
            </Paper>
        </Grid>
    </Grid>
  );
}