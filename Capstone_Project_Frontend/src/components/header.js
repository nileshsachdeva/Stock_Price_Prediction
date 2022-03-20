import { AppBar, IconButton, Toolbar, Typography } from "@material-ui/core";
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { useHistory } from "react-router-dom"

export const Header = ({ title, withBackBtn }) => {
    const history = useHistory()

    return (
        <AppBar variant='outlined' color='default' style={{backgroundColor: '#fff'}}>
            <Toolbar>
                {withBackBtn && <IconButton color='secondary' onClick={() => history.goBack()} style={{marginRight: 10}} >
                    <ArrowBackIcon />
                </IconButton>}
                <Typography variant='h6' >{title}</Typography>
            </Toolbar>
        </AppBar>
    )
}