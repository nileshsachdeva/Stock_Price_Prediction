import { Box, Typography } from "@material-ui/core";

export const CustomChartTooltip = ({ active, payload, label }) =>
  active && (
    <Box
      bgcolor="#fff"
      borderRadius={10}
      border="1px solid #dedede"
      boxShadow="0 2px 8px -1px #bababa"
      px={1.5}
      py={1}
    >
      <Box display="flex" flexDirection="column">
        {/* {payload.map(entry => <Typography variant='caption' >{entry.name}: {entry.value.toFixed(2)}</Typography>)} */}
        {payload.map((entry) => (
          <Typography variant="caption">
            <b>{entry.name}</b>: {entry.value?.toFixed(3)}
          </Typography>
        ))}
      </Box>
    </Box>
  );
