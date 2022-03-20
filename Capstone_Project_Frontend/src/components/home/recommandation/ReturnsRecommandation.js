import { Box, Typography, useTheme } from "@material-ui/core";
import {
  Bar,
  BarChart,
  Cell,
  LabelList,
  ResponsiveContainer,
  XAxis,
  Tooltip,
} from "recharts";
import { Colors } from "../../../constants/colors";

const formatReturns = (data) =>
  Object.entries(data).map(([key, value]) => ({ name: key, value }));

const colors = [
  Colors.DARK_BLUE,
  Colors.BLUE,
  Colors.YELLOW,
  Colors.GREEN_1,
  Colors.ORANGE,
  Colors.RED_1,
];

const RenderCustomizedLabel = (props) => {
  const { x, y, width, height, value } = props;
  const radius = 10;
  return (
    <g>
      <text
        x={x + width / 2}
        y={y > 260 ? y + radius : y - radius}
        fontFamily={useTheme().typography.fontFamily}
        textAnchor="middle"
        dominantBaseline="middle"
      >
        {value}
      </text>
    </g>
  );
};

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

export const ReturnsRecommandation = ({ data: returnsData, isMobile }) => {
  const data = formatReturns(returnsData);

  return (
    <Box width={isMobile ? "100%" : 400} height={350}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          width={500}
          height={300}
          data={data}
          margin={{
            top: -30,
            bottom: -20,
          }}
        >
          <XAxis hide dataKey="name" />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="value" fill="#8884d8">
            <LabelList
              dataKey="name"
              position="insideEnd"
              content={RenderCustomizedLabel}
            />
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % 20]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};
