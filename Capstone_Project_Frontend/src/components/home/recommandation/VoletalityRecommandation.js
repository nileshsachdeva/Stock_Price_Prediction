import { Box, Typography, useTheme } from "@material-ui/core";
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  RadialBar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const CustomTooltip = ({ active, payload, label }) =>
  active && (
    <Box
      bgcolor="#fff"
      borderRadius={10}
      border="1px solid #dedede"
      boxShadow="0 2px 8px -1px #bababa"
      px={1.5}
      py={1}
    >
      <Typography variant="caption">{label}</Typography>
      <Box display="flex" flexDirection="column" alignItems="center">
        {payload.map((entry) => (
          <Typography variant="caption">
            <b>{entry.value?.toFixed(2)}</b>
          </Typography>
        ))}
      </Box>
    </Box>
  );

const formatVoletality = (data) =>
  Object.entries(data).map(([key, value]) => ({ name: key, value }));

export const VoletalityRecommandation = ({ data, isMobile }) => {
  return (
    <Box
      width={isMobile ? "100%" : 400}
      height={350}
      sx={{ fontFamily: useTheme().typography.fontFamily }}
    >
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart
          outerRadius={isMobile && "60%"}
          data={formatVoletality(data)}
        >
          <Tooltip content={<CustomTooltip />} />
          <PolarGrid />
          <PolarAngleAxis
            fontFamily={useTheme().typography.fontFamily}
            dataKey="name"
            tickSize={15}
          />
          <PolarRadiusAxis />
          <Radar
            name="Mike"
            dataKey="value"
            stroke="#8884d8"
            fill="#8884d8"
            fillOpacity={0.6}
          />
        </RadarChart>
      </ResponsiveContainer>
    </Box>
  );
};
