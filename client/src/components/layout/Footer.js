import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';


export default function StickyFooter() {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '50vh'
      }}
    >
      <Box
        component="footer"
        sx={{
          py: 2,
          px: 2,
          mt: 'auto',
          position: "fixed",
          left: 0,
          bottom: 0,
          right: 0,
          backgroundColor: (theme) =>
            theme.palette.mode === 'dark'
              ? theme.palette.grey[200]
              : theme.palette.grey[800],
        }}
      >
        <Container maxWidth="xl">
          

          <Typography variant="body2" align='center' color="#FFFFFF">Made with &nbsp;<span style={{color:"red"}}>❤</span> &nbsp; by HPE CTY team, PES University</Typography>
        </Container>
        
      </Box>
    </Box>
  );
}
