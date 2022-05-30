import { Outlet } from "react-router-dom";
// import Sidebar from "../sidebar/Sidebar";
import FooterComponent from './Footer'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import React from 'react';
// import './AppLayout.scss';
import { useNavigate } from 'react-router-dom'


// import getWeb3 from "../../getWeb3";
// import { useState, useEffect } from 'react';
// import manufacturer from "../../contracts/Manufacturer.json";
// import distributor from "../../contracts/Distributor.json";
// import transporter from "../../contracts/Transporter.json";
// import regional from "../../contracts/Regional.json";

export default function AppLayout() {
    const [auth, setAuth] = React.useState(true);
    const [sidebarOn, setsidebarOn] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);

    // const [account,setAccount]=useState('');
    // const [mContract,setMContract]=useState(null);
    // const [dContract,setDContract]=useState(null);
    // const [tContract,setTContract]=useState(null);
    // const [rContract,setRContract]=useState(null);

    // const navigate = useNavigate()

    // useEffect(()=>{
    //   const loadContract= async()=>{
    //   const web3 = await getWeb3();
    //   const accounts = await web3.eth.getAccounts()
    //   console.log(accounts)
    //   setAccount(accounts[0])

    //   const networkId = await web3.eth.net.getId()

    //   const MnetworkData = manufacturer.networks[networkId]
    //     if(MnetworkData){            
    //         const Mabi = manufacturer.abi
    //         const Maddress = MnetworkData.address
    //         const Mcontract = new web3.eth.Contract(Mabi, Maddress)
    //         setMContract(Mcontract)
    //     }else{
    //         window.alert('Smart Contract not deployed to detected network')
    //     }

    //   const DnetworkData = distributor.networks[networkId]
    //     if(DnetworkData){            
    //         const Dabi = distributor.abi
    //         const Daddress = DnetworkData.address
    //         const Dcontract = new web3.eth.Contract(Dabi, Daddress)
    //         setDContract(Dcontract)
    //     }else{
    //         window.alert('Smart Contract not deployed to detected network')
    //     }

    //   const TnetworkData = transporter.networks[networkId]
    //     if(TnetworkData){            
    //         const Tabi = transporter.abi
    //         const Taddress = TnetworkData.address
    //         const Tcontract = new web3.eth.Contract(Tabi, Taddress)
    //         setTContract(Tcontract)
    //     }else{
    //         window.alert('Smart Contract not deployed to detected network')
    //     }

    //   const RnetworkData = regional.networks[networkId]
    //     if(RnetworkData){            
    //         const Rabi = regional.abi
    //         const Raddress = RnetworkData.address
    //         const Rcontract = new web3.eth.Contract(Rabi, Raddress)
    //         setRContract(Rcontract)
    //     }else{
    //         window.alert('Smart Contract not deployed to detected network')
    //     }
        
        
        
    // }

    //   const contract=loadContract();
    // },[]);

    

    // var Mexists = mContract.methods.Exists(account).call();
    // console.log("account = " + account)
    // var Rexists = rContract.methods.Exists(account).call();
    // var Texists = tContract.methods.Exists(account).call();
    // var Dexists = dContract.methods.Exists(account).call();

    // if(Mexists)
    // {
    //   navigate('/mdashboard');
    // }else if(Rexists){
    //   navigate('/rdashboard');
    // }else if(Texists){
    //   navigate('/tdashboard');
    // }else if(Dexists){
    //   navigate('/ddashboard');
    // }else{

    // }

    







    const handleChange = (event) => {
      setAuth(event.target.checked);
    };
  
    const handleMenu = (event) => {
      setAnchorEl(event.currentTarget);
    };
  
    const handleClose = () => {
      setAnchorEl(null);
    };

    const handleSideBar = (event) => {
        setsidebarOn(!sidebarOn);
    }
    let SideBar;
    // if(sidebarOn)
    // {
    //     SideBar = <Sidebar />;
    // }





    return (
      <Box sx={{ flexGrow: 1 }}>

        {/* {if(something)}   */}
        
        {/* {SideBar} */}
        <AppBar position="static" style={{ background: '' }} >
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
              onClick={handleSideBar}
            >
              <MenuIcon />
            </IconButton>
            
            <Typography component="div" sx={{ flexGrow: 1 }}>
                <div ><h3>Storage Pro</h3></div>
            </Typography>
            {auth && (
              <div>
                <IconButton
                  size="large"
                  aria-label="account of current user"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  onClick={handleMenu}
                  color="inherit"
                >
                  <AccountCircle />
                </IconButton>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={handleClose}>Profile</MenuItem>
                  <MenuItem onClick={handleClose}>My account</MenuItem>
                </Menu>
              </div>
            )}
          </Toolbar>
        </AppBar>
        
      <Outlet />
      <FooterComponent/>
      </Box>
      
    );
  }





// const AppLayout = () => {
//     return <div style={{
//         padding: '50px 0px 0px 370px'
//     }}>
       
//         <Sidebar />
//         <Outlet />
//     </div>;
// };

// export default AppLayout;