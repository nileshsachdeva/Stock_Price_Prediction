import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Divider,
  Typography,
} from "@material-ui/core";
import moment from "moment";
import { useMobileView } from "../../../common/utils";

export const NewsCard = ({ url, title, image, date }) => {
  const isMobile = useMobileView();

  return (
    <Card
      style={{
        borderRadius: 0,
        height: isMobile ? "max-content" : 90,
        textOverflow: "ellipsis",
        overflow: "hidden",
        backgroundColor: "#f9f9f9",
      }}
      onClick={() => window.open(url, "_blank")}
      elevation={0}
      // variant="outlined"
    >
      <CardActionArea style={{ height: "100%" }}>
        <Box display="flex">
          {/* <CardMedia
          style={{
            width: 130,
            height: 80,
            position: "relative!important",
            objectFit: "fill",
          }}
          image={image}
        /> */}
          <CardContent
            style={{
              padding: "14px 19px",
              display: "flex",
              alignItems: "center",
            }}
          >
            <img
              src={image}
              width={70}
              height={50}
              style={{ borderRadius: 5, marginRight: 15, marginLeft: 5 }}
              alt="news"
            />
            <Box
              height="100%"
              display="flex"
              flexDirection="column"
              justifyContent="space-between"
            >
              <Typography variant="body2" style={{ overflow: "hidden" }}>
                {title}
              </Typography>
              <Typography
                variant="caption"
                style={{ marginTop: 7, opacity: 0.4, fontWeight: 600 }}
              >
                {moment(date).format("DD MMM YYYY")}
              </Typography>
            </Box>
          </CardContent>
        </Box>
      </CardActionArea>
    </Card>
  );
};
// export const NewsCard = ({ url, title, image }) => (
//     <Card
//         style={{ borderRadius: 10, height: 80, textOverflow: 'ellipsis', overflow: 'hidden', backgroundColor: '#f9f9f9' }}
//         onClick={() => window.open(url, '_blank')} variant='outlined'
//     >
//         <CardActionArea >
//             <Box display='flex' >
//                 <CardMedia
//                     style={{ width: 130, height: 80, position: 'relative!important', objectFit: 'fill' }}
//                     image={image}
//                 />
//                 <CardContent>
//                     <Typography style={{height: 50, overflow: 'hidden'}} >{title}</Typography>
//                 </CardContent>
//             </Box>
//         </CardActionArea>
//     </Card>
// )
