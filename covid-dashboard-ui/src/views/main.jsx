import React from 'react';
import RegionSelect from './regionSelect';
import RegionChip from './regionChip';
import Records from './records';
import Box from '@material-ui/core/Box';
import Container from "@material-ui/core/Container";

export default function JustifyContent() {
  return (
    <Container maxWidth="md">
      <div style={{ width: '100%' }}>
        <Box display="flex" justifyContent="center" m={1} p={1} bgcolor="background.paper">
          <Box p={1} bgcolor="grey.300">
              <RegionSelect/>
          </Box>
        </Box>
        <Box display="flex" justifyContent="center" m={1} p={1} bgcolor="background.paper">
          <Box p={1} bgcolor="grey.300">
            <RegionChip/>
          </Box>
        </Box>
        <Box display="flex" justifyContent="center" m={1} p={1} bgcolor="background.paper">
          <Box p={1} bgcolor="grey.300">
              <Records/>
          </Box>
        </Box>
      </div>
    </Container>
    );
  }