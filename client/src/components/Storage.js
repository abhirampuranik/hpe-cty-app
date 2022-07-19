import { useState, useEffect, cloneElement } from 'react';
import axios from 'axios'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
// import { Input, Button  } from '@mui/material';
import Chart from "react-google-charts";
import { Button } from '@mui/material';


export default function Storage()
{


    const [ListStorage,setListStorage]=useState([]);
    const [storage, setStorage] = useState();
    const [List, setList] = useState([]);


    
    const handleChangeOnStorage = (event) => {
        setStorage(event.target.value);
    };

    // useEffect(()=>{
    //     // setListStorage(["Storage1", "Storage2","Storage3","Storage4"])

    //     axios.get('http://127.0.0.1:5000/liststorages').then(response => {
    //       console.log("SUCCESS", response.data.message)
    //       setListStorage(response.data.message.split(','))
    //     }).catch(error => {
    //       console.log(error)
    //     })



    // },[]);



    useEffect(()=>{
        const sse =  new EventSource('http://127.0.0.1:5000/stream')
        
        function handleStream(e){
            console.log(e.data)
            var valueList = []
            
            e.data.split('$').map((record)=>(valueList.push([record.split(',')[0], record.split(',')[1]])));
            valueList.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}])
            setList(valueList);
            // List.push(valueList)
        }

        sse.onmessage = e => {handleStream(e)}

        sse.onerror = e => {
            sse.close()
        }

        return () => {
            sse.close()
        }
    },[]);


    useEffect(()=>{
        console.log("List",List);
    },[List])
    // useEffect(()=>{
    //     setoutputArray(predcsv.split('$'));
    // }, [predcsv]);

    // useEffect(()=>{
    //     console.log(outputArray.length)
    //     let valueList = []

    //     outputArray.map((record)=>(valueList.push([record.split(',')[0], record.split(',')[1]])));
    //     // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
    //     valueList.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}])
    //     setList(valueList);

    // },[outputArray])


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



            <Chart
                width={'100%'}
                height={'800px'}
                chartType="LineChart"
                loader={<div>Storage consumption Chart</div>}
                data={
                List
                }
                
                options={{
                    chartArea: {                        
                        innerWidth:'80%',
                        width: '70%'
                      },
                hAxis: {
                    title: 'Time',
                },
                backgroundColor: {
                    fill: '#c39ea0',//'#fbf6a7',
                    fillOpacity: 0.8},
                color:"white",
                vAxis: {
                    title: 'Storage consumption (in MB)',
                }
                }}
            />            
        </div>
    )
}