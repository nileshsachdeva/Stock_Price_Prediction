import { Button as MuiButton, makeStyles } from "@material-ui/core"
import clsx from "clsx"
import { Colors } from "../../constants/colors"

const useStyles = makeStyles({
    root: {
        color: Colors.WHITE,
        textTransform: 'unset',
        fontWeight: '700',
        fontSize: 17,
        borderRadius: 8,
        padding: '7px 20px',
        width: '100%',
        letterSpacing: 0.2
    },
    red: {
        backgroundColor: Colors.RED_1,
        '&:hover': {
            backgroundColor: Colors.RED_2,
        }
    },
    green: {
        backgroundColor: Colors.GREEN_1,
        '&:hover': {
            backgroundColor: Colors.GREEN_2,
        }
    }
})

export const Button = ({children, red, green, onClick}) => {
    const classes = useStyles()

    return (
    <MuiButton
        variant='contained'
        className={clsx(classes.root, red && classes.red, green && classes.green)}
        disableElevation
        onClick={onClick}
    >{children}</MuiButton>
)}