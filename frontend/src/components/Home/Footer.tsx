import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import { Box } from "@mui/material";
const userCompany = "Dell";

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        position: "absolute",
        left: 0,
        bottom: 0,
        right: 0,
        backgroundColor: (theme) =>
          theme.palette.mode === "light"
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
        p: 2,
      }}
    >
      <Container maxWidth="lg" fixed>
        <Box mt={0}>
          <Typography variant="h6" noWrap component="div" align="center">
            <Link
              color="inherit"
              // href="https://aarohisolutions.com/"
              target="_blank"
            >
              {/* {userCompany}
            </Link>{" "}
            {new Date().getFullYear()}
            {"."} */}
              {userCompany} - All rights reserved {new Date().getFullYear()}.
            </Link>
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}
