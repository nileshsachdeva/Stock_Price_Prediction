import {
  Bar,
  BarChart,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Box, Typography } from "@material-ui/core";

export const EarningBarChart = ({ data, title }) => (
  <Box
    display="flex"
    width="50%"
    height="100%"
    flexDirection="column"
    alignItems="center"
  >
    <Box width={"100%"} height={"100%"} fontSize="13px">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <ReferenceLine y={0} stroke="#000" />
          <Tooltip wrapperStyle={{ fontSize: 13 }} />
          <Bar dataKey="Revenue" fill="#0088FE" />
          <Bar dataKey="Earnings" fill="#FF8042" />
          <XAxis dataKey="year" style={{ fontSize: 13 }} hide />
          {/* <Legend style={{ fontSize: 13 }} iconType="circle" /> */}
        </BarChart>
      </ResponsiveContainer>
    </Box>
    <Typography
      variant="body2"
      style={{
        opacity: 0.7,
        fontWeight: 600,
        marginBottom: 20,
        textAlign: "center",
      }}
    >
      {title}
    </Typography>
  </Box>
);
