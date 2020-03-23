import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';
import Paper from '@material-ui/core/Paper';
import * as Actions from "../actions/action";

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    flexWrap: 'wrap',
    padding: theme.spacing(0.5),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
}));

export default function ChipsArray(regions) {

  console.log(regions);

  const classes = useStyles();
  const [chipData, setChipData] = React.useState(regions.chips);

  const handleDelete = regionToDelete => () => {
    Actions.deleteRegion(regionToDelete);
    Actions.removeChip(regionToDelete);
    setChipData(chips => chips.filter(chip => chip.id !== regionToDelete.id));
  };

  return (
    <Paper className={classes.root}>
      {chipData.map(data => {
        let icon;

        return (
          <Chip
            key={data.id}
            icon={icon}
            label={data.name}
            onDelete={data.name === 'Global' ? undefined : handleDelete(data)}
            className={classes.chip}
          />
        );
      })}
    </Paper>
  );
}