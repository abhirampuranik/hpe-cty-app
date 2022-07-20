// import { Home } from '@mui/icons-material';
import React, { useState, useEffect, cloneElement } from 'react';
import axios from 'axios'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Input, Button  } from '@mui/material';
import HourglassTopIcon from '@mui/icons-material/HourglassTop';
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormLabel from "@mui/material/FormLabel";
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Slide from '@mui/material/Slide';
import ChartGraph from './ChartGraph';

function TransitionRight(props) {
  return <Slide {...props} direction="right" />;
}

export default function HomePage() {


    // outputArray - Plot data
    // outputArray1 - predict data
    
    const [file, setFile] = useState();
    const [outputArray, setoutputArray] = useState([]);
    const [getMessage, setGetMessage] = useState({});
    const [getMessage1, setGetMessage1] = useState({});
    const [List,setList]=useState([]);
    
    const [model, setModel] = useState('');
    const [nextDays, setNextDays] = useState(0);
    const [nextHours, setNextHours] = useState(0);
    const [userID, setUserID] = useState('1');

    const [listDays, setListDays] = useState([]);
    const [listHours, setListHours] = useState([]);

    const [action, setAction] = useState('train');

    const [processed, setProcessed] = useState(false);
    const [processing, setProcessing] = useState(false);

    const [predcsv, setpredcsv] = useState("");
    const [r2, setR2] = useState("");

    const [outputArray1, setoutputArray1] = useState([]);
    const [List1,setList1]=useState([]);
    const [SnackbarString,setSnackbarString]=useState('');
    const fileReader = new FileReader();

    const [state, setOpen] = React.useState({
        open:false
    });

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpen({open:false});
    };

    const handleChangeOnModel = (event) => {
        setModel(event.target.value);
    };

    const {open} = state;

    const handleOnChange = (e) => {
        setFile(e.target.files[0]);        
    };

    function range(start, end) {
        return Array(end - start + 1).fill().map((_, idx) => start + idx)
    }

    useEffect(()=>{

        axios.get('http://127.0.0.1:5000/hello').then(response => {
          console.log("SUCCESS", response)
          setGetMessage1(response)
        }).catch(error => {
          console.log(error)
        })

        setListDays(range(0, 31));
        setListHours(range(0,24));  
      }, [])
    

    const handleOnSubmit = (e) => {
        e.preventDefault();
        
        let file1 = file;
        const formData = new FormData();
        formData.append("file", file1);
        formData.append("userID", userID)

        if(model === 'rnn' || model === 'linearregression'){
            axios.post('http://127.0.0.1:5000/datalinearreg', formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
            })
            .then(function (response) { 
                console.log(response.data);
                setoutputArray(response.data.split('\n'))
            })
        }else{
            axios.post('http://127.0.0.1:5000/data', formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
            })
            .then(function (response) { 
                console.log(response.data);
                setoutputArray(response.data.split('\n'))
            })
        }   
    };

    const handleChangeAction = (event) => {
        setAction(event.target.value);
      };

    useEffect(() => {
        console.log("output array",outputArray)
        let valueList=[];
        outputArray.map((record)=>{
                valueList.push([record.split(',')[0], record.split(',')[1]])
            });  
        valueList.unshift([{ type: 'string', label: 'Time' },{label:'Storage Consumption',type:'number'}])
        setList(valueList);
        console.log("List values",valueList)
     }, [outputArray]);

    // Prediction graph data

    useEffect(() => {
        console.log(List1)
    }, [List1]);

    useEffect(() => {
        let valueList1 = []
        outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1]])));
        valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}]);
        setList1(valueList1);   
    }, [outputArray1]);



    const sendCSV = (e) => {
        e.preventDefault();

        if(model !== ''){
            setProcessing(true);
        }
        

        let file1 = file;
        const formData = new FormData();

        formData.append("file", file1);
        formData.append("userID", userID)

        if(model === 'autoarima'){
            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/autoarima/train', formData, 
                    {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    body:{
                        'userID':userID
                    } 
                })
                .then(function (response) { 
                    console.log(response.data);
                    setR2(response.data.R2);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            } else if(action === 'predict') {
                axios.post('http://127.0.0.1:5000/autoarima/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setoutputArray1(response.data.split('\n'));
                    setProcessing(false);
                    setProcessed(true);
                })
            }else{
                axios.post('http://127.0.0.1:5000/autoarima/update', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setSnackbarString(response.data)
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }
        }else if(model === 'prophet'){
            if(action ==='train'){
                axios.post('http://127.0.0.1:5000/prophet/train', formData, {
            headers: {
                'Content-Type': 'application/json'
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setProcessing(false);
                setProcessed(true);
                setOpen({open:true});
            })
            }
            else{
            axios.post('http://127.0.0.1:5000/prophet/predict', {
            headers: {
              'Content-Type': 'application/json'
            },
            body:{
                "days": nextDays,
                "hours":nextHours,
                "userID": userID
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setoutputArray1(response.data.split('\n'));
                setProcessing(false);
                setProcessed(true);
                setOpen({open:true});
            })}
        }else if(model === 'rnn'){
            
            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/rnn/train', formData, 
                    {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    body:{
                        'userID':userID
                    } 
                })
                .then(function (response) { 
                    console.log(response.data);
                    setR2(response.data.R2);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }else if(action === 'predict'){
                axios.post('http://127.0.0.1:5000/rnn/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setoutputArray1(response.data.split('\n'));
                    setProcessing(false);
                    setProcessed(true);
                })
            }

        }else if(model === 'linearregression'){

            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/linearRegression/train', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setR2(response.data.R2);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }else if(action === 'predict'){
                axios.post('http://127.0.0.1:5000/linearRegression/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setoutputArray1(response.data.split('\n'));
                    setProcessing(false);
                    setProcessed(true);
                })
            }
        }
    }

    return (
        <div style={{ textAlign: "center", alignContent:"center", alignItems:"center" }}>
        <div style={{ textAlign: "center" , alignContent:'center'}}>
            <h1>Upload your data</h1>
            <div>{getMessage1.status === 200 ? 
                <h3>{getMessage1.data.message}</h3>
                :
                <h3>LOADING</h3>}
            </div>

            <div style={{alignItems:'center',justifyContent:'center', width:1000, margin:'0px auto'}}>
                <Box justify = "center">
                <FormControl sx={{ m: 1, minWidth: 250 }}>
                    <InputLabel id="demo-simple-select-label">Select Model</InputLabel>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={model}
                    label="Model"
                    onChange={handleChangeOnModel}
                    >
                    <MenuItem value={'autoarima'}>AutoArima</MenuItem>
                    <MenuItem value={'rnn'}>RNN</MenuItem>
                    <MenuItem value={'linearregression'}>Linear Regression</MenuItem>
                    </Select>
                </FormControl>
                

                <FormControl sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id="demo-simple-select-label">User ID</InputLabel>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={userID}
                    label="Model"
                    onChange={(event)=>{setUserID(event.target.value)}}
                    >
                    <MenuItem value={'1'}>1</MenuItem>
                    <MenuItem value={'2'}>2</MenuItem>
                    <MenuItem value={'3'}>3</MenuItem>
                    <MenuItem value={'4'}>4</MenuItem>

                    </Select>
                </FormControl>
                </Box>
            </div>
            <br/>  
            {model==='autoarima'?
                <FormControl>
                <FormLabel id="demo-row-radio-buttons-group-label">Action</FormLabel>
                <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                    value={action}
                    onChange={handleChangeAction}
                >
                    <FormControlLabel value="train" control={<Radio />} label="Train" />
                    <FormControlLabel value="predict" control={<Radio />} label="Predict" />
                    <FormControlLabel value="update" control={<Radio />} label="Update" />
                </RadioGroup>
                </FormControl>

                :model==='prophet' || model==='linearregression' || model === 'rnn'?
                <FormControl>
                <FormLabel id="demo-row-radio-buttons-group-label">Action</FormLabel>
                <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                    value={action}
                    onChange={handleChangeAction}
                >
                    <FormControlLabel value="train" control={<Radio />} label="Train" />
                    <FormControlLabel value="predict" control={<Radio />} label="Predict" />
                </RadioGroup>
                </FormControl>:<span></span>
            }

            {action === 'predict' ?

                    
                <div style={{alignItems:'center',justifyContent:'center', width:150, margin:'0px auto'}}>
                    <br/>
                        <Box justify = "center" sx={{margin:'15px auto'}}>
                        <FormControl fullWidth>
                            <InputLabel id="demo-simple-select-label">Days</InputLabel>
                            <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={nextDays}
                            label="Model"
                            onChange={(event)=>{setNextDays(event.target.value)}}
                            >
                            
                            {
                            listDays.map((row, index)=>(
                                <MenuItem key={index} value={row}>{row}</MenuItem>
                            ))}

                            </Select>
                        </FormControl>
                    </Box>
                    <Box justify = "center" sx={{margin:'15px auto'}}>
                        <FormControl fullWidth>
                            <InputLabel id="demo-simple-select-label">Hours</InputLabel>
                            <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={nextHours}
                            label="Model"
                            onChange={(event)=>{setNextHours(event.target.value)}}
                            >
                            {
                            listHours.map((row)=>(
                                <MenuItem value={row}>{row}</MenuItem>
                            ))}
                            </Select>
                        </FormControl>
                    </Box>
                    <br/>
                    <Button variant="contained"
                        onClick={(e) => {
                            sendCSV(e);
                        }}
                        >Predict</Button>
                </div>
                :
                model !== '' ?
                <div>
                    <Input 
                    type='file'
                    id='csvFileInput'
                    onChange={handleOnChange}/>
                    &nbsp;&nbsp;
                    <Button variant="contained"
                    onClick={(e) => {
                        handleOnSubmit(e);
                    }}
                    >Import CSV and Plot</Button>
                    <br/>
                    <Button variant="contained"
                        onClick={(e) => {
                            sendCSV(e);
                        }}
                        >Send File</Button>
                </div>:<span></span>
            }

            {processed && action === 'train' && model !== 'autoarima'? 
                <div>
                    <h3>R2 score of model: {r2}</h3>
                </div>:<span></span>
            }


            {/* {model === 'autoarima'?
                <div style={{alignItems:'center',justifyContent:'center', width:150, margin:'0px auto'}}>
                <br/>
                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">User ID</InputLabel>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={userID}
                    label="Model"
                    onChange={(event)=>{setUserID(event.target.value)}}
                    >
                    <MenuItem value={'1'}>1</MenuItem>
                    <MenuItem value={'2'}>2</MenuItem>
                    <MenuItem value={'3'}>3</MenuItem>
                    <MenuItem value={'3'}>4</MenuItem>
                    </Select>
                </FormControl>
                </div>:<span></span>
            } */}
              
            <Snackbar 
                anchorOrigin={{ "vertical" : "top" , "horizontal" : "right" }}
                open={open} 
                autoHideDuration={10000} 
                onClose={handleClose}
                TransitionComponent = {TransitionRight}
                >
                <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
                {
                    SnackbarString.length!==0? SnackbarString : ""
                }
                </Alert>
            </Snackbar>
                
            </div>  
            <br/>
            {processing? <div><h1>Processing</h1><HourglassTopIcon/></div>:<span></span>}
            <br/>
            
            {outputArray.length!==0?
                <ChartGraph List={List} color={"#c39ea0"} title={'Storage consumption (in MB)'}/>:<span></span>}

            <br/>
            
            {action === 'predict' && (model === 'autoarima' || model === 'linearregression' || model === 'rnn' || model === 'prophet') && processed?<div><h1>Predictions</h1></div>:<span></span>}
            
            
            {action === 'predict' && (model === 'autoarima' || model === 'linearregression' || model === 'rnn' || model === 'prophet') && processed?
                <div><ChartGraph List={List1} color={"#fbf6a7"} title={"Storage Forecast consumption (in MB)"}/></div>:<span></span>}

        </div>
    );
}