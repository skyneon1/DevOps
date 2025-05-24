import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  useTheme,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import SecurityIcon from '@mui/icons-material/Security';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TimelineIcon from '@mui/icons-material/Timeline';

const Dashboard = () => {
  const theme = useTheme();
  const [securityMetrics, setSecurityMetrics] = useState({
    threats: 0,
    vulnerabilities: 0,
    incidents: 0,
    compliance: 0,
  });

  const [threatData, setThreatData] = useState([]);
  const [vulnerabilityData, setVulnerabilityData] = useState([]);

  useEffect(() => {
    // Fetch real-time security metrics
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/security/metrics');
        const data = await response.json();
        setSecurityMetrics(data);
      } catch (error) {
        console.error('Error fetching metrics:', error);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  const MetricCard = ({ title, value, icon, color }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          {icon}
          <Typography variant="h6" ml={1}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" color={color}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Security Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Metric Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Threats"
            value={securityMetrics.threats}
            icon={<SecurityIcon color="error" />}
            color="error.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Vulnerabilities"
            value={securityMetrics.vulnerabilities}
            icon={<WarningIcon color="warning" />}
            color="warning.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Security Incidents"
            value={securityMetrics.incidents}
            icon={<TimelineIcon color="info" />}
            color="info.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Compliance Score"
            value={`${securityMetrics.compliance}%`}
            icon={<CheckCircleIcon color="success" />}
            color="success.main"
          />
        </Grid>

        {/* Threat Timeline Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Threat Timeline
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={threatData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="threats"
                  stroke={theme.palette.error.main}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Vulnerability Distribution */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Vulnerability Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={vulnerabilityData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {vulnerabilityData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={theme.palette.primary.main}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 