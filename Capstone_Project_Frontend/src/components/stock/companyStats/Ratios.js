import {
  Box,
  Checkbox,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useTheme,
} from "@material-ui/core";
import { withStyles } from "@material-ui/styles";
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  Tooltip,
} from "recharts";
import { useMobileView } from "../../../common/utils";
import { CustomChartTooltip } from "../../elements/CustomChartTooltip";

const StyledRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

export const Ratios = ({ data: graphData }) => {
  const [data, setData] = useState([]);
  const isMobile = useMobileView();

  useEffect(() => {
    setData(graphData);
  }, []);

  const _handleCheckBoxChange = (checked, item) => {
    if (checked) {
      setData((data) => [...data, item]);
    } else {
      setData((data) => data.filter((dItm) => dItm.name !== item.name));
    }
  };

  return (
    <Box mt={4} mb={2}>
      <Typography variant="h6">Useful Ratios</Typography>
      <Box
        display="flex"
        mt={2}
        alignItems="center"
        flexDirection={isMobile ? "column" : "row"}
      >
        <Box
          flexGrow={1}
          height={400}
          mt={-9}
          mb={-5}
          width={isMobile ? "100%" : "unset"}
        >
          <ResponsiveContainer>
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart data={data} barSize={40}>
                <RadialBar
                  minAngle={15}
                  label={{ position: "insideStart", fill: "#fff" }}
                  background
                  clockWise
                  dataKey="value"
                  fontFamily={useTheme().typography.fontFamily}
                />
                <Tooltip content={<CustomChartTooltip />} />
              </RadialBarChart>
            </ResponsiveContainer>
          </ResponsiveContainer>
        </Box>

        <TableContainer
          component={Paper}
          style={{ width: isMobile ? "100%" : "60%" }}
        >
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>View</TableCell>
                <TableCell>Identifier</TableCell>
                <TableCell>Ratio</TableCell>
                <TableCell>Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {graphData.map((item) => (
                <StyledRow>
                  <TableCell>
                    <Checkbox
                      onChange={(e) =>
                        _handleCheckBoxChange(e.target.checked, item)
                      }
                      defaultChecked
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Box
                      width={15}
                      height={15}
                      borderRadius={50}
                      bgcolor={item.fill}
                    />
                  </TableCell>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>{item.value?.toFixed(3)}</TableCell>
                </StyledRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Box>
  );
};
