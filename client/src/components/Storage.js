import { useState, useEffect, cloneElement } from 'react';
import axios from 'axios'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Input, Button  } from '@mui/material';

export default function Storage()
{


    const [ListStorage,setListStorage]=useState([]);
    const [storage, setStorage] = useState();

    const handleChangeOnStorage = (event) => {
        setStorage(event.target.value);
    };

    useEffect(()=>{
        // setListStorage(["Storage1", "Storage2","Storage3","Storage4"])

        axios.get('http://127.0.0.1:5000/liststorages').then(response => {
          console.log("SUCCESS", response.data.message)
          setListStorage(response.data.message.split(','))
        }).catch(error => {
          console.log(error)
        })
    },[]);

    
    useEffect(()=>{
        console.log(Storage)
    }, [Storage]);


    return (
        <div style={{ textAlign: "center", alignContent:"center", alignItems:"center" }}>
            <h1>Storage</h1>

            <div style={{alignItems:'center',justifyContent:'center', width:500, margin:'0px auto'}}>
                <Box justify = "center">
                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Storage</InputLabel>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={Storage}
                    label="Storage"
                    onChange={handleChangeOnStorage}
                    defaultValue=""
                    >
                    { ListStorage.map((record)=> <MenuItem value={record}>{record}</MenuItem>) }
                    </Select>
                </FormControl>
                </Box>
            </div>


            
        </div>
    )
}