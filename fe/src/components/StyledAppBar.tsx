import {
  AppBar, Toolbar, Button,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { NavLink, useLocation } from 'react-router-dom';

import { BoldDiv } from './BoldBox';

interface LinkedButtonProp {
  title: string;
  path: string;
}

const LinkedButton = ({ title, path }: LinkedButtonProp) => {
  return (
    <Button>
        <NavLink to={path} style={({isActive}) =>  (
            {
                color: isActive ? '#FFA000' : 'white',  
                    textDecoration: 'none' ,
            }
        )}>
        <BoldDiv bold>
          {title}
        </BoldDiv>
      </NavLink>
    </Button>
  );
};

interface ILink {
  path: string;
  label: string;
}

interface StyledAppBarProp {
  links: ILink[];
}

const StyledAppBarBase = styled(AppBar)({
  marginBottom: 20,
});
const StyledAppBar = ({ links } : StyledAppBarProp) => {
  return (
    <StyledAppBarBase position="static">
      <Toolbar>
        {links.map((link) => (
          <LinkedButton
            key={link.label}
            title={link.label}
            path={link.path}
          />
        ))}
      </Toolbar>
    </StyledAppBarBase>
  );
};

export default StyledAppBar;
