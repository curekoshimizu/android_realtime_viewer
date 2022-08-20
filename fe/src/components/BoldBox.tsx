import { Box, BoxProps } from '@mui/material';
import { ReactNode } from 'react';

export interface BoldBoxProp extends BoxProps {
  bold?: boolean,
  children?: ReactNode
}

const BoldBox = ({
  bold = true, children, component,
}: BoldBoxProp) => {
  const fontWeight = bold ? 'fontWeightBold' : 'normal';
  return (
    <Box fontWeight={fontWeight} component={component}>
      {children}
    </Box>
  );
};

export const BoldSpan = ({ bold = true, children } : BoldBoxProp) => (
  <BoldBox bold={bold} component="span">{children}</BoldBox>
);

export const BoldDiv = ({ bold = true, children } : BoldBoxProp) => (
  <BoldBox bold={bold} component="div">{children}</BoldBox>
);

export default BoldBox;
