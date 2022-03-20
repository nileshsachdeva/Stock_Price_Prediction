import { createTheme } from "@material-ui/core";

export const theme = createTheme({
    palette: {
        primary: {
            main: '#3d3d3d'
        },
        secondary: {
            main: '#000',
            light: '#0ecb81'
        },
        common: {
            red: '#f6465d',
            green: '#0ecb81'
        },
        success: {
            main: '#0ecb81'
        }
    },
    typography: {
        fontFamily: ["-apple-system", "BlinkMacSystemFont", "Segoe UI","Roboto","Helvetica","Arial","sans-serif","Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"],
        // fontFamily: ['Roboto', 'sans-serif'],
        h3: {
            fontSize: 28,
            fontWeight: '700'
        },
        h4: {
            fontSize: 23,
            fontWeight: '600'
        },
        h5: {
            fontSize: 21,
            fontWeight: '700'
        },
        h6: {
            fontWeight: '700'
        }
    }
})