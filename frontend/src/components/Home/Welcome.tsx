import { Box, Typography, Grid } from "@mui/material";
import MainImage from "../../images/aarohi-about-us.jpeg";

const Welcome = (props: { location: { state: any } }) => {
  return (
    <div>
      <Grid
        container
        direction="row"
        justifyContent="center"
        alignItems="center"
      >
        <Box
          component="img"
          sx={{
            // height: 100,
            // width: 100,
            // maxHeight: { xs: 233, md: 167 },
            // maxWidth: { xs: 350, md: 250 },
            direction: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
          alt={MainImage}
          src={MainImage}
        />
      </Grid>
      <Box mt={2}>
        <Typography paragraph align="center">
          Ansible Network Collection for Enterprise SONiC Distribution by Dell
          Technologies
        </Typography>
      </Box>
    </div>
  );
};
export default Welcome;
