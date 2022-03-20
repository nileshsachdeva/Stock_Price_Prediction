import { Box, Card, CardActionArea, CardContent, makeStyles, Typography } from "@material-ui/core";
import clsx from "clsx";
import { useHistory } from "react-router-dom";
import { ROUTES } from "../../constants/common";

const useStyles = makeStyles(theme => ({
  card: {
    width: 260,
    minWidth: 230,
    borderRadius: 15,
  },
  green: {
    background: 'rgb(255, 255, 255)',
    background: 'linear-gradient(130deg, #fff 47%, #c8f5bf 100%)',
    color: '#64a564ba'
  },
  red: {
    background: 'rgb(255, 255, 255)',
    background: 'linear-gradient(130deg, #fff 47%, #ffc3bc 100%)',
    color: '#b1353580'
  },
  subTxt: {
    fontWeight: 700,
    textTransform: 'uppercase'
  }
}))

export const StockListItem = ({item}) => {
  const classes = useStyles()
  const isRise = item.prediction === 1

  const getClassName =  isRise ? classes.green : classes.red
  const getSubtitle = isRise ? 'Potential Rise' : 'Potential Fall'

  const history = useHistory()

  return (
    <Card className={clsx(classes.card, getClassName)} onClick={() => history.push(`${ROUTES.stock}/${item.symbol}`)}>
      <CardActionArea style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start', padding: '6px 5px' }}>
        <CardContent style={{width: '100%'}}>
          <Box display='flex' alignItems='center' alignSelf='flex-start'>
            <img src={`/assets/${item.logo}`} alt='logo' height='30px' style={{ marginRight: 8 }} />
            <Typography variant='h6' color='secondary'>{item.name}</Typography>
          </Box>
          <Box mt={3} display='flex' justifyContent='flex-end' mb={-0.5}>
            <Typography variant='body1' className={classes.subTxt}>{getSubtitle}</Typography>
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}
